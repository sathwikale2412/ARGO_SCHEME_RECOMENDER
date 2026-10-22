import { API_BASE, supabase } from './supabase';

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

export const recommendSchemes = (form) => callApi('get_schemes', form);

export const askAboutSchemes = (message) => callApi('chat', { message });

export async function getSchemes() {
  if (supabase) {
    const { data, error } = await supabase.from('schemes').select('*').order('name');
    if (!error && data?.length) return { schemes: data, source: 'database' };
    if (error) console.error('Failed to load scheme catalogue', error.message);
  }

  // No database attached, or it is still unseeded: the API serves the sample catalogue
  // bundled with it, so the filters have something to offer instead of nothing.
  try {
    const response = await fetch(`${API_BASE}/schemes`);
    const body = await response.json();
    if (response.ok && Array.isArray(body.schemes)) {
      return { schemes: body.schemes, source: body.catalogue || 'sample' };
    }
  } catch {
    /* left empty; the page says the catalogue could not be loaded */
  }
  return { schemes: [], source: 'none' };
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
  if (error) console.error('Failed to save eligibility check', error.message);
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
