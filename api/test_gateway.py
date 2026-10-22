"""Checks the ARGO API's own decisions, with no live Supabase.

fetch_schemes and is_configured are replaced, so what is under test is input validation,
the rate limit, the bundled sample catalogue, and what a caller is told when the
catalogue read fails.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('SUPABASE_URL', 'https://fake.supabase.co')
os.environ.setdefault('SUPABASE_ANON_KEY', 'anon-key-not-real')

import catalogue  # noqa: E402
import index  # noqa: E402

results = []


def check(label, ok, detail=''):
    print(f'{"PASS" if ok else "FAIL"}  {label} {detail}')
    results.append(ok)


client = index.app.test_client()

health = client.get('/api/health').get_json()
check('health reports config without the URL', 'fake.supabase.co' not in str(health), health)

incomplete = client.post('/api/get_schemes', json={'state': '', 'crop': 'wheat', 'land': 'x'})
check('incomplete search refused', incomplete.status_code == 400, incomplete.get_json()['message'])

check('blank chat refused', client.post('/api/chat', json={'message': '  '}).status_code == 400)
check('oversized chat refused',
      client.post('/api/chat', json={'message': 'a' * 600}).status_code == 400)
check('non-string chat refused',
      client.post('/api/chat', json={'message': {'nested': True}}).status_code == 400)
check('adding a scheme over the API is refused',
      client.post('/api/schemes', json={}).status_code == 405)
check('unknown endpoint is 404', client.get('/api/nonsense').status_code == 404)

# --- the bundled sample catalogue, i.e. a deployment with no Supabase env ---------------
configured = index.is_configured
index.is_configured = lambda: False
index._hits.clear()

check('health says which catalogue is serving',
      client.get('/api/health').get_json()['catalogue'] == 'sample')
listing = client.get('/api/schemes').get_json()
check('a deployment with no database still gets rows, not 503',
      listing['count'] == len(catalogue.SCHEMES) and listing['catalogue'] == 'sample',
      f"{listing['count']} rows")
needed = {'name', 'state', 'min_land', 'max_land', 'crop',
          'category', 'income_limit', 'subsidy', 'documents', 'deadline'}
check('every sample row has the columns the matcher reads',
      all(needed <= set(row) for row in listing['schemes']))
check('the sample set spans several categories',
      len({row['category'] for row in listing['schemes']}) >= 8,
      len({row['category'] for row in listing['schemes']}))
check('the sample set spans several states',
      len({row['state'] for row in listing['schemes']}) >= 12,
      len({row['state'] for row in listing['schemes']}))

hit = client.post('/api/get_schemes', json={
    'state': 'Telangana', 'crop': 'rice', 'category': 'General',
    'land': '4', 'income': '150000',
}).get_json()
check('an eligibility check matches against the sample rows',
      hit['status'] == 'ok' and len(hit['results']) >= 1 and hit['catalogue'] == 'sample',
      hit['results'])
chat = client.post('/api/chat', json={'message': 'organic'}).get_json()
check('keyword search covers the sample rows', len(chat['schemes']) >= 1, chat['schemes'])
index._hits.clear()
index.is_configured = configured


db_row = {'name': 'From Postgres', 'state': 'Telangana', 'min_land': 0, 'max_land': 10,
          'crop': 'Rice', 'category': 'General', 'income_limit': 999999,
          'subsidy': 1, 'documents': '', 'deadline': ''}
index.fetch_schemes = lambda: [db_row]
served = client.get('/api/schemes').get_json()
check('the database wins once env is set',
      served['catalogue'] == 'database' and served['schemes'] == [db_row])


def explode():
    raise RuntimeError('relation "schemes" does not exist; SQL from ../supabase_client.py')


index.fetch_schemes = explode
failure = client.get('/api/schemes').get_json()
check('catalogue failure is one generic sentence',
      failure['message'] == 'The scheme catalogue could not be searched. Try again shortly.')
check('failure carries a ref', len(failure.get('ref', '')) == 8)
for phrase in ('RuntimeError', 'relation', 'SQL', 'supabase_client', 'fake.supabase.co', 'anon-key'):
    check(f'failure does not leak {phrase!r}', phrase not in str(failure))

index._hits.clear()
codes = [client.get('/api/schemes').status_code for _ in range(index.RATE_MAX_REQUESTS + 2)]
tripped = client.get('/api/schemes').get_json()
check('rate limit trips after the window budget',
      codes.count(500) == index.RATE_MAX_REQUESTS and codes.count(429) == 2,
      f'{codes.count(500)} served, {codes.count(429)} refused')
check('refusal names no internals', 'RuntimeError' not in str(tripped) and 'ref' in tripped)

print(f'\n{sum(results)}/{len(results)} checks passed')
sys.exit(0 if all(results) else 1)
