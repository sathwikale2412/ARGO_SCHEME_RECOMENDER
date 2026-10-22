# ARGO Scheme Recommender

Farmers enter their state, crop, category, land holding and income; the API returns the
government schemes they are eligible for, and the catalogue itself lives in a database so
any signed-in user can add to it.

**Live URL:** https://argo-scheme-recommender.vercel.app (see "Deploy" below — the URL is
created by the first `vercel deploy`.)

## What is real and what is sample

| Part | Status |
| --- | --- |
| Eligibility predicate (`api/recommender.py`) | Real logic, kept verbatim from the original `backend/recommender.py`. |
| Scheme catalogue | Supabase table `schemes` is the live one. Until it is attached and seeded, `api/catalogue.py` ships 36 sample schemes (8 categories, 15 states) so the filters still have something to match; every answer says which source served it. |
| Login / signup | Real — Supabase GoTrue, email + password. |
| Sign-in audit trail | Real — table `argo_logins`, written on every `SIGNED_IN`. |
| Eligibility-check history | Real — table `argo_checks`. |
| `backend/ai_extractor.py` | **Not functional.** `extract_schemes_with_ai()` always returns one hardcoded mock scheme and is not wired to any route. It is left in the repo untouched for reference. |
| `backend/app.py`, `backend/models.py`, `backend/schemes.db` | Original SQLite prototype, kept for reference. The deployed app does not use them. |

## Architecture

```
Browser (React + Vite)  ──▶  /api/*  (Vercel Python function)  ──▶  Supabase PostgREST  ──▶  Postgres
        │                                                                        ▲
        └────────── Supabase JS client (auth only) ─────────────────────────────┘
```

- **Frontend** — `src/`, built by Vite into `dist/`.
- **API** — `api/index.py`, a Flask WSGI app running as one Vercel Python function. A
  catch-all route dispatches on the trailing path segment, so `http://127.0.0.1:5001/get_schemes`
  locally and `https://<host>/api/get_schemes` on Vercel hit the same handler.
- **Database** — Supabase. The function talks to PostgREST over HTTPS with the anon key,
  so every query is subject to Row Level Security. There is no service-role key anywhere.

### Endpoints

| Endpoint | Method | Body | Returns |
| --- | --- | --- | --- |
| `/api/health` | GET | — | `{ status, service, catalogue: "database" \| "sample" }` |
| `/api/schemes` | GET | — | `{ count, schemes, catalogue }` — every scheme in the catalogue |
| `/api/schemes` | POST | — | `405` by design; see "Writes" below |
| `/api/get_schemes` | POST | `{state, crop, category, land, income}` | `{ status, results, catalogue }` |
| `/api/chat` | POST | `{ message }` | `{ reply, schemes, catalogue }` — keyword search over state/crop/category |

Every answer carries `catalogue`, so a caller can tell a live register from demo data:

* `"database"` — `SUPABASE_URL` / `SUPABASE_ANON_KEY` are set, rows come from Postgres.
* `"sample"` — they are not, so `api/catalogue.py` serves its bundled schemes. Without that
  the site answered 503 and every dropdown was empty, which is not a usable deployment.

A database that *is* configured but read fails (missing table, network) is a 500, never a
silent swap to sample rows: demo figures must not appear under a "live" label.

`/api/get_schemes` validates every field before touching the database: a missing state, a
non-numeric `land` or a negative `income` answers `400` with the reason, because reading
garbage as 0 acres would come back as a confident, wrong eligibility answer. `/api/chat`
accepts only a 1-500 character string.

Any other failure answers with one sentence and a `ref` — `"ref": "8f3c21d0"`, for example.
The exception itself (table names, the PostgREST body, the project URL) goes to the Vercel
function log instead of the visitor. A rate-limit `429` carries the same shape.

Catalogue reads are limited to **30 per minute per address**. The counter lives inside one
warm instance, so it is a brake rather than a guarantee: a stateless function cannot share
a single global count.

```bash
python api/test_gateway.py   # 25 checks — validation, sample catalogue, generic errors, rate limit
```

### Reads

The browser asks Supabase for the catalogue first (`src/lib/cloud.js:getSchemes`) and, when
there is no client or the table is still empty, falls back to `GET /api/schemes`.

### Writes

Adding a scheme, recording a sign-in and saving an eligibility check all go **directly
from the browser to Supabase** with the user's own JWT (`src/lib/cloud.js`). The serverless
function only ever holds the anon key, so it has no user identity — an insert attempted
through it would be rejected by RLS. That is why `POST /api/schemes` returns `405`.

## Setup

### 1. Supabase

1. Create (or reuse) a project. **Use the same project as your other apps** — they then
   share one user pool, so a single account works everywhere.
2. In the SQL editor, run `supabase/schema.sql`, then `supabase/seed.sql`. The seed holds the
   same 36 rows as `api/catalogue.py` and is generated from it — change the sample data there
   and regenerate rather than editing the SQL.
3. Copy the Project URL and the **anon** public key. Never use the `service_role` key in
   this project — the client and the function both run as anonymous, guarded by RLS.

### 2. Local

```bash
cp .env.example .env         # fill in the four values
npm install
pip install -r api/requirements.txt
npm run dev                  # frontend on :5173
cd backend && python app.py  # NOT used by the new UI — see api/index.py instead
```

To run the API locally the same way the frontend calls it:

```bash
cd api && flask --app index run --port 5001
```

`vite.config.js` proxies `/api/*` to `http://127.0.0.1:5001`, so the browser code is
identical locally and in production.

### 3. Deploy (Vercel)

```bash
vercel link
vercel env add VITE_SUPABASE_URL            # type: Config
vercel env add VITE_SUPABASE_ANON_KEY       # type: Config
vercel env add SUPABASE_URL                 # type: Env Variable (function runtime)
vercel env add SUPABASE_ANON_KEY            # type: Env Variable (function runtime)
vercel deploy --prod
```

`VITE_`-prefixed variables are inlined into the bundle **at build time** — set them as
Config (not Secret) and redeploy after changing them. The unprefixed pair is what the
Python function reads.

## Authentication behaviour

- `src/context/AuthContext.jsx` gates the app on Supabase session. Without
  `VITE_SUPABASE_URL` / `VITE_SUPABASE_ANON_KEY` the gate is skipped and the app runs
  device-only, exactly as a static build would.
- Sign-up sends a confirmation email; the app tells the user to confirm before signing in.
- "Continue as guest" stores `argo_guest_v1` in localStorage and disables the
  add-scheme form and the account panel.
- Each sign-in appends a row to `argo_logins`; the account panel shows the user's own
  recent sign-ins and eligibility checks.

## Row Level Security

| Table | Policy |
| --- | --- |
| `schemes` | `SELECT` — anyone (public catalogue). `INSERT` — authenticated users only, row tagged `added_by`. |
| `argo_logins` | `SELECT` / `INSERT` — own `user_id` only. |
| `argo_checks` | `SELECT` / `INSERT` — own `user_id` only. |

## Authorship

This repository is a fork; the original commits (`Initial commit`) and everything under
`backend/` belong to the original team (`Immortal-coder2351`, `azmeeratharun`). The
React frontend in `src/`, the Vercel API in `api/`, and the Supabase files in `supabase/`
were added on top of their work. The recommendation predicate was preserved line-for-line;
`_to_float()` was added so values like `"5 acres"` cannot raise `ValueError`.

The `front_end` path was removed from the index — it was a broken gitlink (mode `160000`
with no `.gitmodules` entry) in this fork *and* upstream, so `git submodule update --init`
fails and its contents were never recoverable. That is why the UI was rebuilt.
