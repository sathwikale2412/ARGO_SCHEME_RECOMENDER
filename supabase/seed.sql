-- ARGO seed catalogue — 36 schemes, generated from api/catalogue.py.
-- Change the sample data there and regenerate this file; do not hand-edit the rows here.
-- Re-running is safe: the guard inserts nothing once the table already holds a row.

insert into public.schemes (name, state, min_land, max_land, crop, category, income_limit, subsidy, documents, deadline)
select * from (
  values
    ('PM-KISAN Income Support', 'Telangana', 0, 10, 'Rice, Cotton, Maize', 'General', 200000, 6000, 'Aadhar, Land Records, Bank Passbook', '2027-03-31'),
    ('PM-KISAN Income Support', 'Maharashtra', 0, 10, 'Sugarcane, Cotton, Onion', 'General', 200000, 6000, 'Aadhar, Land Records, Bank Passbook', '2027-03-31'),
    ('Rythu Bharosa Kitchen Garden', 'Telangana', 0, 2, 'Tomato, Brinjal, Leafy', 'Small & Marginal', 150000, 12000, 'Aadhar, Patta, Ration Card', '2026-12-15'),
    ('Andhra Smallholder Input Grant', 'Andhra Pradesh', 0, 3, 'Paddy, Groundnut', 'Small & Marginal', 180000, 9000, 'Aadhar, Land Records', '2027-01-31'),
    ('Kisan Credit Card at Subsidised Rate', 'Punjab', 0, 25, 'Wheat, Rice, Maize', 'General', 600000, 20000, 'Aadhar, Land Records, Bank Passbook, Caste Proof', '2027-06-30'),
    ('Crop Insurance Premium Waiver', 'Karnataka', 0, 20, 'Ragi, Maize, Tur', 'General', 400000, 15000, 'Aadhar, Land Records, Sowing Certificate', '2026-11-30'),
    ('Drought Crop Loss Compensation', 'Rajasthan', 1, 30, 'Bajra, Guar, Mustard', 'General', 500000, 22000, 'Aadhar, Land Records, Damage Report', '2026-12-31'),
    ('Drip Irrigation Subsidy', 'Maharashtra', 1, 15, 'Sugarcane, Onion, Grape', 'OBC', 600000, 25000, 'Land Records, Caste Certificate, Quotation', '2026-11-15'),
    ('Solar Pump Installation Grant', 'Gujarat', 0, 12, 'Cotton, Groundnut, Castor', 'General', 450000, 60000, 'Aadhar, Land Records, Electricity Bill', '2027-02-28'),
    ('Micro Sprinkler Support', 'Telangana', 0, 5, 'Chilli, Turmeric, Maize', 'Small & Marginal', 250000, 18000, 'Aadhar, Patta, Vendor Bill', '2027-01-15'),
    ('Custom Hiring Centre Membership', 'Uttar Pradesh', 0, 8, 'Wheat, Rice, Potato', 'Youth', 300000, 35000, 'Aadhar, Land Records, Age Proof', '2027-04-30'),
    ('Horticulture Mission Plantation Aid', 'Andhra Pradesh', 1, 10, 'Banana, Mango, Chilli', 'General', 500000, 30000, 'Aadhar, Land Records, Nursery Bill', '2027-03-15'),
    ('Protected Cultivation Structure Subsidy', 'Karnataka', 0, 5, 'Tomato, Capsicum, Flower', 'Youth', 350000, 75000, 'Aadhar, Land Records, Technical Plan', '2026-12-31'),
    ('Floriculture Export Support', 'Tamil Nadu', 1, 15, 'Rose, Jasmine, Tuberose', 'General', 700000, 40000, 'Aadhar, Land Records, FPO Registration', '2027-05-31'),
    ('Turmeric Processing Unit Grant', 'Telangana', 0, 6, 'Turmeric, Ginger', 'SC/ST', 300000, 50000, 'Aadhar, Caste Certificate, Land Records', '2027-02-15'),
    ('Natural Farming Transition Support', 'Andhra Pradesh', 0, 8, 'Paddy, Groundnut, Pulses', 'Organic', 400000, 15000, 'Aadhar, Land Records, Farm Plan', '2027-06-30'),
    ('Certified Organic Input Reimbursement', 'Kerala', 0, 6, 'Pepper, Coconut, Banana', 'Organic', 350000, 20000, 'Aadhar, Land Records, Organic Certificate', '2027-01-31'),
    ('Dairy Animal Purchase Assistance', 'Uttar Pradesh', 0, 5, 'Fodder, Maize', 'Women', 250000, 50000, 'Aadhar, Bank Passbook, Shelter Proof', '2026-12-20'),
    ('Backyard Poultry Shed Grant', 'Bihar', 0, 3, 'Maize, Rice', 'Women', 200000, 12000, 'Aadhar, Land Records, Vendor Bill', '2027-03-31'),
    ('Fodder Seed Distribution', 'Madhya Pradesh', 1, 12, 'Fodder, Bajra', 'General', 400000, 6000, 'Aadhar, Land Records', '2026-11-30'),
    ('Dairy Cold Chain Membership', 'Gujarat', 0, 10, 'Fodder, Maize, Wheat', 'General', 550000, 28000, 'Aadhar, Land Records, Cooperative Card', '2027-04-15'),
    ('SC/ST Farm Mechanisation Grant', 'Telangana', 0, 8, 'Rice, Cotton, Maize', 'SC/ST', 300000, 45000, 'Aadhar, Caste Certificate, Land Records, Quotation', '2027-02-28'),
    ('Tribal Horticulture Development Aid', 'Odisha', 0, 10, 'Mango, Cashew, Banana', 'SC/ST', 250000, 32000, 'Aadhar, Caste Certificate, Land Records', '2027-05-31'),
    ('OBC Farmer Interest Subvention', 'Andhra Pradesh', 1, 15, 'Paddy, Chilli, Tobacco', 'OBC', 500000, 18000, 'Aadhar, Caste Certificate, Loan Sanction Letter', '2027-01-31'),
    ('OBC Group Farming Support', 'Tamil Nadu', 2, 20, 'Sugarcane, Rice, Turmeric', 'OBC', 600000, 26000, 'Aadhar, Caste Certificate, Group Registration', '2027-03-31'),
    ('Women Farmer Self-Help Group Seed Capital', 'Karnataka', 0, 5, 'Tomato, Onion, Flower', 'Women', 200000, 20000, 'Aadhar, SHG Registration, Bank Passbook', '2026-12-31'),
    ('Women-led Vermicompost Unit', 'Maharashtra', 0, 6, 'Sugarcane, Banana, Cotton', 'Women', 300000, 15000, 'Aadhar, Land Records, Unit Plan', '2027-02-15'),
    ('Youth Agri-Entrepreneurship Grant', 'Punjab', 0, 12, 'Maize, Potato, Mushroom', 'Youth', 350000, 80000, 'Aadhar, Land Records, Project Report, Age Proof', '2027-06-30'),
    ('Graduate Farmer Startup Support', 'Telangana', 0, 8, 'Chilli, Turmeric, Organic Veg', 'Youth', 400000, 60000, 'Aadhar, Degree Certificate, Land Records', '2027-04-30'),
    ('Tenant Farmer Seed Subsidy', 'West Bengal', 0, 6, 'Rice, Jute, Potato', 'Tenant Farmer', 220000, 8000, 'Aadhar, Tenancy Deed, Bank Passbook', '2026-12-31'),
    ('Shifting Cultivation Stabilisation Aid', 'Assam', 0, 4, 'Rice, Bamboo, Ginger', 'SC/ST', 180000, 14000, 'Aadhar, Caste Certificate, Village Certificate', '2027-03-31'),
    ('Seed Village Producer Support', 'Madhya Pradesh', 1, 15, 'Wheat, Soybean, Chickpea', 'General', 500000, 24000, 'Aadhar, Land Records, FPO Registration', '2027-05-15'),
    ('PM-KISAN', 'Karnataka', 0, 10, 'Rice', 'General', 500000, 6000, 'Aadhar, Land Records', '2026-03-31'),
    ('Rice Support Scheme', 'Karnataka', 1, 12, 'Rice', 'OBC', 600000, 8000, 'Aadhar, Caste Certificate', '2026-05-01'),
    ('Small Farmer Rice Grant', 'Karnataka', 0, 8, 'Rice', 'General', 400000, 5000, 'Land Records', '2026-06-15'),
    ('Crop Insurance Yojana', 'Karnataka', 0, 20, 'Wheat', 'General', 800000, 10000, 'Aadhar, Bank Passbook', '2026-02-15')
) as seed(name, state, min_land, max_land, crop, category, income_limit, subsidy, documents, deadline)
where not exists (select 1 from public.schemes);
