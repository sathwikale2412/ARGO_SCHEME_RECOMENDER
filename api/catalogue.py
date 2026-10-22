"""Sample scheme catalogue, bundled with the API.

Why this exists: the live catalogue lives in Postgres, and until the deployment has
SUPABASE_URL / SUPABASE_ANON_KEY the recommender has nothing to match against, so the
site answers 503 and every dropdown is empty. A reference catalogue that ships with the
code keeps the service usable on its own; when the database is attached it wins, and this
file is only the fallback.

These rows are illustrative sample data for demos and tests — subsidy figures, bands and
deadlines are not an official register and must not be quoted to a farmer.

The shape matches `schemes` column for column, because `recommender.recommend` reads
these keys directly. Two rules from that matcher shaped the data:

*   `state` and `crop` are **substring** matches against the *user's* input, so a scheme
    covering several crops lists them together ("Rice, Maize") and a blank state would
    match nothing at all — every row names one state, and a national scheme is repeated
    per state instead.
*   `category` is folded before it is compared (punctuation, spaces and "and" removed, then
    a synonym table), so the spellings below are the canonical ones the frontend offers and
    a visitor typing `SC`, `Small and Marginal` or `women farmer` still lands on the right
    group. Keeping one consistent spelling per row is what makes that work.
"""

SCHEMES = [
    # ---------------------------------------------------------------- income support
    {
        "name": "PM-KISAN Income Support",
        "state": "Telangana", "min_land": 0, "max_land": 10, "crop": "Rice, Cotton, Maize",
        "category": "General", "income_limit": 200000, "subsidy": 6000,
        "documents": "Aadhar, Land Records, Bank Passbook", "deadline": "2027-03-31",
    },
    {
        "name": "PM-KISAN Income Support",
        "state": "Maharashtra", "min_land": 0, "max_land": 10, "crop": "Sugarcane, Cotton, Onion",
        "category": "General", "income_limit": 200000, "subsidy": 6000,
        "documents": "Aadhar, Land Records, Bank Passbook", "deadline": "2027-03-31",
    },
    {
        "name": "Rythu Bharosa Kitchen Garden",
        "state": "Telangana", "min_land": 0, "max_land": 2, "crop": "Tomato, Brinjal, Leafy",
        "category": "Small & Marginal", "income_limit": 150000, "subsidy": 12000,
        "documents": "Aadhar, Patta, Ration Card", "deadline": "2026-12-15",
    },
    {
        "name": "Andhra Smallholder Input Grant",
        "state": "Andhra Pradesh", "min_land": 0, "max_land": 3, "crop": "Paddy, Groundnut",
        "category": "Small & Marginal", "income_limit": 180000, "subsidy": 9000,
        "documents": "Aadhar, Land Records", "deadline": "2027-01-31",
    },

    # ---------------------------------------------------------------- credit and insurance
    {
        "name": "Kisan Credit Card at Subsidised Rate",
        "state": "Punjab", "min_land": 0, "max_land": 25, "crop": "Wheat, Rice, Maize",
        "category": "General", "income_limit": 600000, "subsidy": 20000,
        "documents": "Aadhar, Land Records, Bank Passbook, Caste Proof", "deadline": "2027-06-30",
    },
    {
        "name": "Crop Insurance Premium Waiver",
        "state": "Karnataka", "min_land": 0, "max_land": 20, "crop": "Ragi, Maize, Tur",
        "category": "General", "income_limit": 400000, "subsidy": 15000,
        "documents": "Aadhar, Land Records, Sowing Certificate", "deadline": "2026-11-30",
    },
    {
        "name": "Drought Crop Loss Compensation",
        "state": "Rajasthan", "min_land": 1, "max_land": 30, "crop": "Bajra, Guar, Mustard",
        "category": "General", "income_limit": 500000, "subsidy": 22000,
        "documents": "Aadhar, Land Records, Damage Report", "deadline": "2026-12-31",
    },

    # ---------------------------------------------------------------- irrigation and equipment
    {
        "name": "Drip Irrigation Subsidy",
        "state": "Maharashtra", "min_land": 1, "max_land": 15, "crop": "Sugarcane, Onion, Grape",
        "category": "OBC", "income_limit": 600000, "subsidy": 25000,
        "documents": "Land Records, Caste Certificate, Quotation", "deadline": "2026-11-15",
    },
    {
        "name": "Solar Pump Installation Grant",
        "state": "Gujarat", "min_land": 0, "max_land": 12, "crop": "Cotton, Groundnut, Castor",
        "category": "General", "income_limit": 450000, "subsidy": 60000,
        "documents": "Aadhar, Land Records, Electricity Bill", "deadline": "2027-02-28",
    },
    {
        "name": "Micro Sprinkler Support",
        "state": "Telangana", "min_land": 0, "max_land": 5, "crop": "Chilli, Turmeric, Maize",
        "category": "Small & Marginal", "income_limit": 250000, "subsidy": 18000,
        "documents": "Aadhar, Patta, Vendor Bill", "deadline": "2027-01-15",
    },
    {
        "name": "Custom Hiring Centre Membership",
        "state": "Uttar Pradesh", "min_land": 0, "max_land": 8, "crop": "Wheat, Rice, Potato",
        "category": "Youth", "income_limit": 300000, "subsidy": 35000,
        "documents": "Aadhar, Land Records, Age Proof", "deadline": "2027-04-30",
    },

    # ---------------------------------------------------------------- horticulture
    {
        "name": "Horticulture Mission Plantation Aid",
        "state": "Andhra Pradesh", "min_land": 1, "max_land": 10, "crop": "Banana, Mango, Chilli",
        "category": "General", "income_limit": 500000, "subsidy": 30000,
        "documents": "Aadhar, Land Records, Nursery Bill", "deadline": "2027-03-15",
    },
    {
        "name": "Protected Cultivation Structure Subsidy",
        "state": "Karnataka", "min_land": 0, "max_land": 5, "crop": "Tomato, Capsicum, Flower",
        "category": "Youth", "income_limit": 350000, "subsidy": 75000,
        "documents": "Aadhar, Land Records, Technical Plan", "deadline": "2026-12-31",
    },
    {
        "name": "Floriculture Export Support",
        "state": "Tamil Nadu", "min_land": 1, "max_land": 15, "crop": "Rose, Jasmine, Tuberose",
        "category": "General", "income_limit": 700000, "subsidy": 40000,
        "documents": "Aadhar, Land Records, FPO Registration", "deadline": "2027-05-31",
    },
    {
        "name": "Turmeric Processing Unit Grant",
        "state": "Telangana", "min_land": 0, "max_land": 6, "crop": "Turmeric, Ginger",
        "category": "SC/ST", "income_limit": 300000, "subsidy": 50000,
        "documents": "Aadhar, Caste Certificate, Land Records", "deadline": "2027-02-15",
    },

    # ---------------------------------------------------------------- organic
    {
        "name": "Natural Farming Transition Support",
        "state": "Andhra Pradesh", "min_land": 0, "max_land": 8, "crop": "Paddy, Groundnut, Pulses",
        "category": "Organic", "income_limit": 400000, "subsidy": 15000,
        "documents": "Aadhar, Land Records, Farm Plan", "deadline": "2027-06-30",
    },
    {
        "name": "Certified Organic Input Reimbursement",
        "state": "Kerala", "min_land": 0, "max_land": 6, "crop": "Pepper, Coconut, Banana",
        "category": "Organic", "income_limit": 350000, "subsidy": 20000,
        "documents": "Aadhar, Land Records, Organic Certificate", "deadline": "2027-01-31",
    },

    # ---------------------------------------------------------------- dairy and poultry
    {
        "name": "Dairy Animal Purchase Assistance",
        "state": "Uttar Pradesh", "min_land": 0, "max_land": 5, "crop": "Fodder, Maize",
        "category": "Women", "income_limit": 250000, "subsidy": 50000,
        "documents": "Aadhar, Bank Passbook, Shelter Proof", "deadline": "2026-12-20",
    },
    {
        "name": "Backyard Poultry Shed Grant",
        "state": "Bihar", "min_land": 0, "max_land": 3, "crop": "Maize, Rice",
        "category": "Women", "income_limit": 200000, "subsidy": 12000,
        "documents": "Aadhar, Land Records, Vendor Bill", "deadline": "2027-03-31",
    },
    {
        "name": "Fodder Seed Distribution",
        "state": "Madhya Pradesh", "min_land": 1, "max_land": 12, "crop": "Fodder, Bajra",
        "category": "General", "income_limit": 400000, "subsidy": 6000,
        "documents": "Aadhar, Land Records", "deadline": "2026-11-30",
    },
    {
        "name": "Dairy Cold Chain Membership",
        "state": "Gujarat", "min_land": 0, "max_land": 10, "crop": "Fodder, Maize, Wheat",
        "category": "General", "income_limit": 550000, "subsidy": 28000,
        "documents": "Aadhar, Land Records, Cooperative Card", "deadline": "2027-04-15",
    },

    # ---------------------------------------------------------------- reserved and welfare
    {
        "name": "SC/ST Farm Mechanisation Grant",
        "state": "Telangana", "min_land": 0, "max_land": 8, "crop": "Rice, Cotton, Maize",
        "category": "SC/ST", "income_limit": 300000, "subsidy": 45000,
        "documents": "Aadhar, Caste Certificate, Land Records, Quotation", "deadline": "2027-02-28",
    },
    {
        "name": "Tribal Horticulture Development Aid",
        "state": "Odisha", "min_land": 0, "max_land": 10, "crop": "Mango, Cashew, Banana",
        "category": "SC/ST", "income_limit": 250000, "subsidy": 32000,
        "documents": "Aadhar, Caste Certificate, Land Records", "deadline": "2027-05-31",
    },
    {
        "name": "OBC Farmer Interest Subvention",
        "state": "Andhra Pradesh", "min_land": 1, "max_land": 15, "crop": "Paddy, Chilli, Tobacco",
        "category": "OBC", "income_limit": 500000, "subsidy": 18000,
        "documents": "Aadhar, Caste Certificate, Loan Sanction Letter", "deadline": "2027-01-31",
    },
    {
        "name": "OBC Group Farming Support",
        "state": "Tamil Nadu", "min_land": 2, "max_land": 20, "crop": "Sugarcane, Rice, Turmeric",
        "category": "OBC", "income_limit": 600000, "subsidy": 26000,
        "documents": "Aadhar, Caste Certificate, Group Registration", "deadline": "2027-03-31",
    },

    # ---------------------------------------------------------------- women and youth
    {
        "name": "Women Farmer Self-Help Group Seed Capital",
        "state": "Karnataka", "min_land": 0, "max_land": 5, "crop": "Tomato, Onion, Flower",
        "category": "Women", "income_limit": 200000, "subsidy": 20000,
        "documents": "Aadhar, SHG Registration, Bank Passbook", "deadline": "2026-12-31",
    },
    {
        "name": "Women-led Vermicompost Unit",
        "state": "Maharashtra", "min_land": 0, "max_land": 6, "crop": "Sugarcane, Banana, Cotton",
        "category": "Women", "income_limit": 300000, "subsidy": 15000,
        "documents": "Aadhar, Land Records, Unit Plan", "deadline": "2027-02-15",
    },
    {
        "name": "Youth Agri-Entrepreneurship Grant",
        "state": "Punjab", "min_land": 0, "max_land": 12, "crop": "Maize, Potato, Mushroom",
        "category": "Youth", "income_limit": 350000, "subsidy": 80000,
        "documents": "Aadhar, Land Records, Project Report, Age Proof", "deadline": "2027-06-30",
    },
    {
        "name": "Graduate Farmer Startup Support",
        "state": "Telangana", "min_land": 0, "max_land": 8, "crop": "Chilli, Turmeric, Organic Veg",
        "category": "Youth", "income_limit": 400000, "subsidy": 60000,
        "documents": "Aadhar, Degree Certificate, Land Records", "deadline": "2027-04-30",
    },

    # ---------------------------------------------------------------- tenant and shift
    {
        "name": "Tenant Farmer Seed Subsidy",
        "state": "West Bengal", "min_land": 0, "max_land": 6, "crop": "Rice, Jute, Potato",
        "category": "Tenant Farmer", "income_limit": 220000, "subsidy": 8000,
        "documents": "Aadhar, Tenancy Deed, Bank Passbook", "deadline": "2026-12-31",
    },
    {
        "name": "Shifting Cultivation Stabilisation Aid",
        "state": "Assam", "min_land": 0, "max_land": 4, "crop": "Rice, Bamboo, Ginger",
        "category": "SC/ST", "income_limit": 180000, "subsidy": 14000,
        "documents": "Aadhar, Caste Certificate, Village Certificate", "deadline": "2027-03-31",
    },
    {
        "name": "Seed Village Producer Support",
        "state": "Madhya Pradesh", "min_land": 1, "max_land": 15, "crop": "Wheat, Soybean, Chickpea",
        "category": "General", "income_limit": 500000, "subsidy": 24000,
        "documents": "Aadhar, Land Records, FPO Registration", "deadline": "2027-05-15",
    },

    # ---------------------------------------------------------------- carried over from the
    # original backend/seed_data.py, which seeded only Karnataka and Maharashtra. Kept so a
    # deployment seeded from the earlier seed.sql does not lose rows.
    {
        "name": "PM-KISAN",
        "state": "Karnataka", "min_land": 0, "max_land": 10, "crop": "Rice",
        "category": "General", "income_limit": 500000, "subsidy": 6000,
        "documents": "Aadhar, Land Records", "deadline": "2026-03-31",
    },
    {
        "name": "Rice Support Scheme",
        "state": "Karnataka", "min_land": 1, "max_land": 12, "crop": "Rice",
        "category": "OBC", "income_limit": 600000, "subsidy": 8000,
        "documents": "Aadhar, Caste Certificate", "deadline": "2026-05-01",
    },
    {
        "name": "Small Farmer Rice Grant",
        "state": "Karnataka", "min_land": 0, "max_land": 8, "crop": "Rice",
        "category": "General", "income_limit": 400000, "subsidy": 5000,
        "documents": "Land Records", "deadline": "2026-06-15",
    },
    {
        "name": "Crop Insurance Yojana",
        "state": "Karnataka", "min_land": 0, "max_land": 20, "crop": "Wheat",
        "category": "General", "income_limit": 800000, "subsidy": 10000,
        "documents": "Aadhar, Bank Passbook", "deadline": "2026-02-15",
    },
]

# The columns PostgREST returns, so a fallback row and a database row are the same shape
# to everything downstream. `id` is generated by Postgres; the frontend only uses it as a
# list key, so the bundled rows number from one.
for _offset, _row in enumerate(SCHEMES, start=1):
    _row["id"] = _offset
