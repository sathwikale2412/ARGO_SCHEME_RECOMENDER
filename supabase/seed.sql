-- ARGO seed catalogue — the five rows from backend/seed_data.py, unchanged.
-- Re-running is safe: existing seed rows are skipped by name.

insert into public.schemes (name, state, min_land, max_land, crop, category, income_limit, subsidy, documents, deadline)
select * from (
  values
    ('PM-KISAN', 'Karnataka', 0, 10, 'Rice', 'General', 500000, 6000, 'Aadhar, Land Records', '2026-03-31'),
    ('Rice Support Scheme', 'Karnataka', 1, 12, 'Rice', 'OBC', 600000, 8000, 'Aadhar, Caste Certificate', '2026-05-01'),
    ('Small Farmer Rice Grant', 'Karnataka', 0, 8, 'Rice', 'General', 400000, 5000, 'Land Records', '2026-06-15'),
    ('Crop Insurance Yojana', 'Karnataka', 0, 20, 'Wheat', 'General', 800000, 10000, 'Aadhar, Bank Passbook', '2026-02-15'),
    ('Drip Irrigation Subsidy', 'Maharashtra', 1, 15, 'Sugarcane', 'OBC', 600000, 25000, 'Land Records, Caste Certificate', '2026-04-01')
) as seed(name, state, min_land, max_land, crop, category, income_limit, subsidy, documents, deadline)
where not exists (select 1 from public.schemes);
