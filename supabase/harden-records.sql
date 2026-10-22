-- ARGO Scheme Recommender — make eligibility checks permanent
-- Paste into Supabase -> SQL Editor for the shared project and run. Safe to re-run.
--
-- "own argo checks" is a `for all` policy, so a user can rewrite or delete their own
-- eligibility history. src/lib/cloud.js only inserts (recordCheck) and selects
-- (fetchRecentChecks), so nothing in the app needs update or delete.
--
-- The `schemes` catalogue is already correct and is left alone: readable by anyone
-- ("schemes are readable"), insertable only by a signed-in user for themselves
-- ("signed-in users add schemes" checks added_by = auth.uid()), and with no update or
-- delete policy at all, so an added scheme can never be edited from the browser.

drop policy if exists "own argo checks" on public.argo_checks;
drop policy if exists "own argo checks read" on public.argo_checks;
drop policy if exists "own argo checks insert" on public.argo_checks;

create policy "own argo checks read" on public.argo_checks
  for select using (auth.uid() = user_id);

create policy "own argo checks insert" on public.argo_checks
  for insert with check (auth.uid() = user_id);

-- Neither insert sends its timestamp, so the database can be the one to set it:
-- recordCheck (cloud.js:78) and recordLogin (cloud.js:57) leave those columns out.
create or replace function public.argo_force_login_time()
returns trigger
language plpgsql
as $$
begin
  new.logged_at := now();
  return new;
end;
$$;

create or replace function public.argo_force_check_time()
returns trigger
language plpgsql
as $$
begin
  new.checked_at := now();
  return new;
end;
$$;

drop trigger if exists argo_logins_force_time on public.argo_logins;
create trigger argo_logins_force_time
  before insert on public.argo_logins
  for each row execute function public.argo_force_login_time();

drop trigger if exists argo_checks_force_time on public.argo_checks;
create trigger argo_checks_force_time
  before insert on public.argo_checks
  for each row execute function public.argo_force_check_time();
