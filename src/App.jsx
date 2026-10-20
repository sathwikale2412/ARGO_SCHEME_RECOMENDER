import { useCallback, useEffect, useState } from 'react';
import { useAuth } from './context/AuthContext';
import {
  addScheme,
  askAboutSchemes,
  fetchLoginHistory,
  fetchRecentChecks,
  getSchemes,
  recommendSchemes,
  recordCheck
} from './lib/cloud';
import AuthScreen from './components/AuthScreen';

const EMPTY_FORM = { state: '', crop: '', category: '', land: '', income: '' };

const EMPTY_SCHEME = {
  name: '',
  state: '',
  crop: '',
  category: '',
  min_land: '',
  max_land: '',
  income_limit: '',
  subsidy: '',
  documents: '',
  deadline: ''
};

function distinct(values) {
  return Array.from(new Set(values.map((v) => String(v ?? '').trim()).filter(Boolean))).sort();
}

export default function App() {
  const { ready, cloudEnabled, userId, email, isGuest, signOut } = useAuth();

  const [schemes, setSchemes] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [results, setResults] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');

  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);

  const [showAccount, setShowAccount] = useState(false);
  const [logins, setLogins] = useState([]);
  const [checks, setChecks] = useState([]);

  const [schemeForm, setSchemeForm] = useState(EMPTY_SCHEME);

  const refreshSchemes = useCallback(() => {
    getSchemes().then(setSchemes);
  }, []);

  useEffect(() => {
    refreshSchemes();
  }, [refreshSchemes]);

  useEffect(() => {
    if (!userId) return undefined;
    let cancelled = false;
    Promise.all([fetchLoginHistory(userId), fetchRecentChecks(userId)]).then(([loginRows, checkRows]) => {
      if (!cancelled) {
        setLogins(loginRows);
        setChecks(checkRows);
      }
    });
    return () => {
      cancelled = true;
    };
  }, [userId]);

  const states = distinct(schemes.map((s) => s.state));
  const crops = distinct(schemes.map((s) => s.crop));
  const categories = distinct(schemes.map((s) => s.category));

  const setField = (key) => (event) => setForm((prev) => ({ ...prev, [key]: event.target.value }));

  const handleSearch = async (event) => {
    event.preventDefault();
    setBusy(true);
    setError('');
    setNotice('');
    try {
      const data = await recommendSchemes({
        state: form.state,
        crop: form.crop,
        category: form.category,
        land: form.land,
        income: form.income
      });
      setResults(data.results ?? []);
      if (userId) {
        await recordCheck(userId, form, (data.results ?? []).length);
        fetchRecentChecks(userId).then(setChecks);
      }
      if (!(data.results ?? []).length) {
        setNotice('No scheme matched those inputs. Widen the filters — the rules need an exact category, and land and income inside the band.');
      }
    } catch (err) {
      setResults(null);
      setError(err instanceof Error ? err.message : 'The recommendation service is unreachable.');
    } finally {
      setBusy(false);
    }
  };

  const handleAsk = async (event) => {
    event.preventDefault();
    setError('');
    try {
      const data = await askAboutSchemes(question.trim());
      setAnswer(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'The search service is unreachable.');
    }
  };

  const handleAddScheme = async (event) => {
    event.preventDefault();
    setError('');
    setNotice('');
    try {
      await addScheme({
        name: schemeForm.name.trim(),
        state: schemeForm.state.trim(),
        crop: schemeForm.crop.trim(),
        category: schemeForm.category.trim(),
        min_land: Number(schemeForm.min_land) || 0,
        max_land: Number(schemeForm.max_land) || 0,
        income_limit: Number(schemeForm.income_limit) || 0,
        subsidy: Number(schemeForm.subsidy) || 0,
        documents: schemeForm.documents.trim(),
        deadline: schemeForm.deadline.trim(),
        added_by: userId
      });
      setSchemeForm(EMPTY_SCHEME);
      setNotice('Scheme saved to the catalogue.');
      refreshSchemes();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not save the scheme.');
    }
  };

  if (!ready) {
    return (
      <div className="auth-wrap">
        <p style={{ color: '#052e16', fontSize: '0.8125rem' }}>Loading ARGO…</p>
      </div>
    );
  }

  if (cloudEnabled && !userId && !isGuest) {
    return <AuthScreen />;
  }

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <div className="brand-mark">A</div>
          <div>
            <h1>ARGO Scheme Recommender</h1>
            <p>Find the agricultural schemes a farmer actually qualifies for</p>
          </div>
        </div>

        <div className="account">
          <span className="badge">{schemes.length} schemes in catalogue</span>
          {cloudEnabled && (
            <button type="button" className="btn" onClick={() => setShowAccount((v) => !v)}>
              {userId ? 'Account' : 'Guest session'}
            </button>
          )}
        </div>
      </header>

      <main className="main">
        <div>
          <section className="panel">
            <h2>Eligibility check</h2>
            <p className="lede">
              Filters run against the live scheme catalogue. State and crop match on substring, category must match
              exactly, and land and income have to fall inside the band each scheme declares.
            </p>

            <form className="form-grid" onSubmit={handleSearch}>
              <div className="field">
                <label htmlFor="f-state">State</label>
                <input id="f-state" list="state-options" value={form.state} onChange={setField('state')} placeholder="Karnataka" />
                <datalist id="state-options">{states.map((s) => <option key={s} value={s} />)}</datalist>
              </div>

              <div className="field">
                <label htmlFor="f-crop">Crop</label>
                <input id="f-crop" list="crop-options" value={form.crop} onChange={setField('crop')} placeholder="Rice" />
                <datalist id="crop-options">{crops.map((c) => <option key={c} value={c} />)}</datalist>
              </div>

              <div className="field">
                <label htmlFor="f-category">Category</label>
                <select id="f-category" value={form.category} onChange={setField('category')}>
                  <option value="">Choose a category</option>
                  {categories.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>

              <div className="field">
                <label htmlFor="f-land">Landholding (acres)</label>
                <input id="f-land" type="number" min="0" step="0.1" value={form.land} onChange={setField('land')} placeholder="5" />
              </div>

              <div className="field">
                <label htmlFor="f-income">Annual income (₹)</label>
                <input id="f-income" type="number" min="0" step="1000" value={form.income} onChange={setField('income')} placeholder="400000" />
              </div>

              <div className="field">
                <label>&nbsp;</label>
                <button type="submit" className="btn btn-primary" disabled={busy}>
                  {busy ? 'Checking…' : 'Check eligibility'}
                </button>
              </div>
            </form>

            {error && <p className="error">{error}</p>}
            {notice && <p className="notice">{notice}</p>}

            {results && (
              <div style={{ marginTop: '1.25rem' }}>
                {results.length === 0 ? (
                  <p className="empty">No matches for this profile.</p>
                ) : (
                  results.map((scheme, index) => (
                    <article className="result" key={`${scheme.name}-${index}`}>
                      <h3>{scheme.name}</h3>
                      <dl>
                        <dt>Subsidy</dt>
                        <dd>₹{Number(scheme.subsidy).toLocaleString('en-IN')}</dd>
                        <dt>Documents</dt>
                        <dd>{scheme.documents || '—'}</dd>
                        <dt>Deadline</dt>
                        <dd>{scheme.deadline || '—'}</dd>
                      </dl>
                    </article>
                  ))
                )}
              </div>
            )}
          </section>

          <section className="panel">
            <h2>Ask in plain words</h2>
            <p className="lede">Keyword search across state, crop and category.</p>
            <form className="form-grid" style={{ gridTemplateColumns: 'minmax(0,1fr) auto' }} onSubmit={handleAsk}>
              <div className="field">
                <label htmlFor="f-question">Your question</label>
                <input id="f-question" value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="rice" required />
              </div>
              <div className="field">
                <label>&nbsp;</label>
                <button type="submit" className="btn">Search</button>
              </div>
            </form>

            {answer && (
              <div style={{ marginTop: '1rem' }}>
                <p className="lede">{answer.reply}</p>
                {(answer.schemes ?? []).map((scheme, index) => (
                  <article className="result" key={`${scheme.name}-${index}`}>
                    <h3>{scheme.name}</h3>
                    <dl>
                      <dt>Subsidy</dt>
                      <dd>₹{Number(scheme.subsidy).toLocaleString('en-IN')}</dd>
                      <dt>Deadline</dt>
                      <dd>{scheme.deadline || '—'}</dd>
                    </dl>
                  </article>
                ))}
              </div>
            )}
          </section>
        </div>

        <aside>
          {cloudEnabled && showAccount && (
            <section className="panel">
              <h2>Account</h2>
              <p className="lede">{userId ? email : 'Guest session — nothing is written to the database.'}</p>

              {userId && (
                <>
                  <h3 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.04em', color: '#5b6660', margin: '0.75rem 0 0.25rem' }}>
                    Sign-in history
                  </h3>
                  {logins.length === 0 ? (
                    <p className="empty">No sign-ins recorded yet.</p>
                  ) : (
                    <ul className="list">
                      {logins.map((row, i) => (
                        <li key={`${row.logged_at}-${i}`}>
                          <span>{new Date(row.logged_at).toLocaleString()}</span>
                          <span className="muted">{row.email}</span>
                        </li>
                      ))}
                    </ul>
                  )}

                  <h3 style={{ fontSize: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.04em', color: '#5b6660', margin: '1rem 0 0.25rem' }}>
                    Recent checks
                  </h3>
                  {checks.length === 0 ? (
                    <p className="empty">Run an eligibility check to see it saved here.</p>
                  ) : (
                    <ul className="list">
                      {checks.map((row, i) => (
                        <li key={`${row.checked_at}-${i}`}>
                          <span>{row.state || 'any'} · {row.crop || 'any'} · {row.category || 'any'}</span>
                          <span className="muted">{row.match_count} match{row.match_count === 1 ? '' : 'es'}</span>
                        </li>
                      ))}
                    </ul>
                  )}

                  <button type="button" className="btn btn-block" onClick={() => signOut()}>
                    Sign out
                  </button>
                </>
              )}
            </section>
          )}

          {userId ? (
            <section className="panel">
              <h2>Add a scheme</h2>
              <p className="lede">Field officers can extend the catalogue. Rows are tagged with your account.</p>
              <form className="stack" onSubmit={handleAddScheme}>
                <div className="field">
                  <label htmlFor="s-name">Scheme name</label>
                  <input id="s-name" required value={schemeForm.name} onChange={(e) => setSchemeForm({ ...schemeForm, name: e.target.value })} />
                </div>
                <div className="form-grid">
                  <div className="field">
                    <label htmlFor="s-state">State</label>
                    <input id="s-state" required value={schemeForm.state} onChange={(e) => setSchemeForm({ ...schemeForm, state: e.target.value })} />
                  </div>
                  <div className="field">
                    <label htmlFor="s-crop">Crop</label>
                    <input id="s-crop" required value={schemeForm.crop} onChange={(e) => setSchemeForm({ ...schemeForm, crop: e.target.value })} />
                  </div>
                  <div className="field">
                    <label htmlFor="s-category">Category</label>
                    <input id="s-category" required value={schemeForm.category} onChange={(e) => setSchemeForm({ ...schemeForm, category: e.target.value })} />
                  </div>
                  <div className="field">
                    <label htmlFor="s-deadline">Deadline</label>
                    <input id="s-deadline" value={schemeForm.deadline} onChange={(e) => setSchemeForm({ ...schemeForm, deadline: e.target.value })} placeholder="31 Mar 2027" />
                  </div>
                  <div className="field">
                    <label htmlFor="s-min">Min land (acres)</label>
                    <input id="s-min" type="number" step="0.1" value={schemeForm.min_land} onChange={(e) => setSchemeForm({ ...schemeForm, min_land: e.target.value })} />
                  </div>
                  <div className="field">
                    <label htmlFor="s-max">Max land (acres)</label>
                    <input id="s-max" type="number" step="0.1" value={schemeForm.max_land} onChange={(e) => setSchemeForm({ ...schemeForm, max_land: e.target.value })} />
                  </div>
                  <div className="field">
                    <label htmlFor="s-income">Income limit (₹)</label>
                    <input id="s-income" type="number" step="1000" value={schemeForm.income_limit} onChange={(e) => setSchemeForm({ ...schemeForm, income_limit: e.target.value })} />
                  </div>
                  <div className="field">
                    <label htmlFor="s-subsidy">Subsidy (₹)</label>
                    <input id="s-subsidy" type="number" step="1000" value={schemeForm.subsidy} onChange={(e) => setSchemeForm({ ...schemeForm, subsidy: e.target.value })} />
                  </div>
                </div>
                <div className="field">
                  <label htmlFor="s-docs">Documents required</label>
                  <input id="s-docs" value={schemeForm.documents} onChange={(e) => setSchemeForm({ ...schemeForm, documents: e.target.value })} placeholder="Aadhaar, land record, bank passbook" />
                </div>
                <button type="submit" className="btn btn-primary btn-block">Save scheme</button>
              </form>
            </section>
          ) : (
            <section className="panel">
              <h2>Catalogue</h2>
              <p className="lede">
                {schemes.length === 0
                  ? 'The scheme table is empty. Run supabase/seed.sql in the SQL editor, then reload this page.'
                  : 'Sign in to add or correct scheme entries. Guests can search but cannot write.'}
              </p>
              <ul className="list">
                {schemes.slice(0, 8).map((s) => (
                  <li key={s.id}>
                    <span>{s.name}</span>
                    <span className="muted">{s.state}</span>
                  </li>
                ))}
              </ul>
            </section>
          )}
        </aside>
      </main>

      <footer className="footer">
        Matching rules and the seed catalogue come from the original ARGO backend. Subsidy figures are the values
        stored in the database — verify them against the official scheme notice before advising a farmer.
      </footer>
    </div>
  );
}
