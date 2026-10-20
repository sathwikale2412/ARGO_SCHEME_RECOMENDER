-- ARGO Scheme Recommender — Supabase schema
-- Run this first, then supabase/seed.sql, in the Supabase SQL editor.
--
-- The catalogue moves out of the committed SQLite file (which cannot live on a
-- serverless filesystem) into Postgres. Columns match backend/models.py one-for-one.

create table if not exists public.schemes (
  id bigint generated always as identity primary key,
  name text not null,
  state text not null default '',
  min_land numeric not null default 0,
  max_land numeric not null default 0,
  crop text not null default '',
  category text not null default 'General',
  income_limit numeric not null default 0,
  subsidy numeric not null default 0,
  documents text not null default '',
  deadline text not null default '',
  added_by uuid default auth.uid() references auth.users on delete set null,
  created_at timestamptz not null default now()
);

-- Sign-in log for this app.
create table if not exists public.argo_logins (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users on delete cascade,
  email text not null default '',
  logged_at timestamptz not null default now()
);

-- Every eligibility check a signed-in user ran, with how many schemes matched.
create table if not exists public.argo_checks (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users on delete cascade,
  state text not null default '',
  crop text not null default '',
  category text not null default '',
  land numeric not null default 0,
  income numeric not null default 0,
  match_count int not null default 0,
  checked_at timestamptz not null default now()
);

create index if not exists argo_logins_user_idx on public.argo_logins (user_id, logged_at desc);
create index if not exists argo_checks_user_idx on public.argo_checks (user_id, checked_at desc);

alter table public.schemes enable row level security;
alter table public.argo_logins enable row level security;
alter table public.argo_checks enable row level security;

-- The catalogue is public information: anyone may read it, only signed-in users may add to it.
create policy "schemes are readable" on public.schemes
  for select using (true);

create policy "signed-in users add schemes" on public.schemes
  for insert with check (auth.uid() is not null and added_by = auth.uid());

create policy "own argo logins read" on public.argo_logins
  for select using (auth.uid() = user_id);

create policy "own argo logins insert" on public.argo_logins
  for insert with check (auth.uid() = user_id);

create policy "own argo checks" on public.argo_checks
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
