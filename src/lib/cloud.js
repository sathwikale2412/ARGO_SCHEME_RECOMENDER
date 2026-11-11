import { API_BASE, supabase } from './supabase';
import { DEFAULT_SCHEMES } from './defaultSchemes';

async function callApi(path, body) {
  const response = await fetch(`${API_BASE}/${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    throw new Error(`API responded ${response.status} with a non-JSON body.`);
  }

  if (!response.ok || data.status === 'error' || data.status === 'unavailable') {
    throw new Error(data.message || `API responded ${response.status}.`);
  }
  return data;
}

function matchLocal(form, list) {
  const stateNeedle = (form.state || '').trim().toLowerCase();
  const cropNeedle = (form.crop || '').trim().toLowerCase();
  const catNeedle = (form.category || '').trim().toLowerCase();
  const landVal = parseFloat(form.land);
  const incomeVal = parseFloat(form.income);

  return list.filter((s) => {
    if (stateNeedle && !s.state.toLowerCase().includes(stateNeedle)) return false;
    if (cropNeedle && !s.crop.toLowerCase().includes(cropNeedle)) return false;
    if (catNeedle) {
      const sCat = (s.category || '').toLowerCase();
      if (!sCat.includes(catNeedle) && !catNeedle.includes(sCat)) return false;
    }
    if (!isNaN(landVal)) {
      if (landVal < Number(s.min_land) || landVal > Number(s.max_land)) return false;
    }
    if (!isNaN(incomeVal)) {
      if (incomeVal > Number(s.income_limit)) return false;
    }
    return true;
  });
}

export async function recommendSchemes(form) {
  try {
    return await callApi('get_schemes', form);
  } catch (err) {
    console.warn('Backend recommendation error, falling back to local matcher:', err);
    const results = matchLocal(form, DEFAULT_SCHEMES);
    return { status: 'ok', results, catalogue: 'sample' };
  }
}

export async function askAboutSchemes(message) {
  try {
    return await callApi('chat', { message });
  } catch (err) {
    console.warn('Backend chat error, falling back to local search:', err);
    const needle = (message || '').toLowerCase();
    const hits = DEFAULT_SCHEMES.filter(
      (s) =>
        s.name.toLowerCase().includes(needle) ||
        s.crop.toLowerCase().includes(needle) ||
        s.state.toLowerCase().includes(needle)
    );
    return {
      reply: hits.length ? 'Here are matching schemes from our catalogue:' : 'No matching schemes found for your query.',
      schemes: hits.slice(0, 5),
      catalogue: 'sample'
    };
  }
}

export async function getSchemes() {
  if (supabase) {
    try {
      const { data, error } = await supabase.from('schemes').select('*').order('name');
      if (!error && data?.length) return { schemes: data, source: 'database' };
      if (error) {
        console.warn('Supabase schemes fetch warning:', error.message);
      }
    } catch (e) {
      console.warn('Supabase schemes exception:', e);
    }
  }

  // Fallback to API gateway
  try {
    const response = await fetch(`${API_BASE}/schemes`);
    const body = await response.json();
    if (response.ok && Array.isArray(body.schemes) && body.schemes.length > 0) {
      return { schemes: body.schemes, source: body.catalogue || 'sample' };
    }
  } catch (err) {
    console.warn('API /schemes fetch failed, falling back to bundled data:', err);
  }

  // Offline guaranteed fallback
  return { schemes: DEFAULT_SCHEMES, source: 'sample' };
}

export async function recordLogin(userId, email) {
  if (!supabase) return;
  const { error } = await supabase.from('argo_logins').insert({ user_id: userId, email });
  if (error) console.error('Failed to record sign-in', error.message);
}

export async function fetchLoginHistory(userId) {
  if (!supabase) return [];
  const { data, error } = await supabase
    .from('argo_logins')
    .select('email, logged_at')
    .eq('user_id', userId)
    .order('logged_at', { ascending: false })
    .limit(25);
  if (error) {
    console.error('Failed to load sign-in history', error.message);
    return [];
  }
  return data ?? [];
}

export async function recordCheck(userId, form, matchCount) {
  if (!supabase) return;
  const { error } = await supabase.from('argo_checks').insert({
    user_id: userId,
    state: form.state,
    crop: form.crop,
    category: form.category,
    land: form.land,
    income: form.income,
    match_count: matchCount
  });
  if (error) {
    console.error('Failed to save eligibility check', error.message);
    // Generic wording: the raw Postgres message names tables and policies.
    throw new Error('This check is shown, but it was not added to your saved history.');
  }
}

export async function fetchRecentChecks(userId) {
  if (!supabase) return [];
  const { data, error } = await supabase
    .from('argo_checks')
    .select('state, crop, category, land, income, match_count, checked_at')
    .eq('user_id', userId)
    .order('checked_at', { ascending: false })
    .limit(10);
  if (error) {
    console.error('Failed to load past checks', error.message);
    return [];
  }
  return data ?? [];
}

export async function addScheme(scheme) {
  if (!supabase) throw new Error('Sign in before adding a scheme.');
  const { error } = await supabase.from('schemes').insert(scheme);
  if (error) throw new Error(error.message);
}
