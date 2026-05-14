"""
Sample Data Generator — Entity-Level Client Family Model
=========================================================
~160 entities across 12 client families.  ~80% are served.
Revenue per entity is realistic for professional services:
  - Individuals (1040): $5K–$15K
  - Trusts/small entities: $10K–$30K
  - Partnerships/Corporations: $20K–$80K
  - No single entity exceeds $200K; most sit in the $10K–$50K band.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import random

np.random.seed(42)
random.seed(42)

# =============================================================================
# REFERENCE DATA
# =============================================================================

SERVICE_LINES = ["Assurance", "Tax", "Business Operations", "Digital"]

ENTITY_TYPES = ["1065 Partnership", "1120 Corporation", "1120S S-Corp", "1041 Trust", "Individual"]

GEOGRAPHY_HIERARCHY = {
    "Midwest": {
        "Upper Midwest": ["Minneapolis", "Greater Iowa", "Southern Minnesota", "Northern Minnesota"],
        "Wisconsin": ["Northern Wisconsin", "Southern Wisconsin", "Central Wisconsin"],
        "Heartland": ["Central Illinois", "Greater Missouri"],
        "Central": ["Western Ohio", "Eastern Ohio", "Greater Indiana"],
        "Greater Chicagoland": ["Northern Illinois"],
    },
    "West": {
        "Southern CA": ["Southern California"],
        "PacWest": ["Northern California", "Central California"],
        "Northwest": ["Pacific Northwest", "Inland Northwest"],
        "Mountain": ["Greater Southwest", "Rocky Mountains", "Greater Nevada"],
    },
    "Sunbelt": {
        "Texas": ["Northern Texas", "Central Texas", "Southern Texas"],
        "Florida": ["Southwest Florida", "Greater Tampa Bay", "Orlando"],
        "CaroLantAville": ["Greater Carolinas", "Atlanta", "Greater Tennessee"],
    },
    "Northeast": {
        "New England": ["Southern New England", "Greater New York", "Connecticut"],
        "Mid-Atlantic": ["Baltimore/Washington", "Greater Philadelphia", "Pittsburgh"],
    },
}

GEOGRAPHIES = [
    "Minneapolis", "Northern Wisconsin", "Southern Wisconsin", "Central Wisconsin",
    "Central Illinois", "Greater Missouri", "Western Ohio", "Greater Indiana",
    "Northern Illinois", "Southern California", "Northern California",
    "Pacific Northwest", "Greater Southwest", "Rocky Mountains",
    "Northern Texas", "Central Texas", "Southwest Florida", "Greater Tampa Bay",
    "Orlando", "Greater Carolinas", "Atlanta", "Greater New York",
    "Southern New England", "Baltimore/Washington", "Greater Philadelphia",
]

INDUSTRY_HIERARCHY = {
    "Financial Services": ["Banks", "Specialty Finance", "Insurance", "Credit Unions"],
    "Real Estate": ["Lessors & Operators", "Developers & Subdividers", "Investor", "Other Real Estate"],
    "Private Equity": ["Private Equity - Industry Segment"],
}

INDUSTRIES = [
    "Banks", "Specialty Finance", "Insurance", "Credit Unions",
    "Lessors & Operators", "Developers & Subdividers", "Investor",
    "Other Real Estate", "Private Equity - Industry Segment",
]

CRL_NAMES = [
    "Rypina, Katarzyna", "Juergensen, Joshua", "Carlson, Erica",
    "Mattson, Brad", "Wieland, Sylvia", "Sabo, Susan",
    "Meyer, Nicholas", "Holthaus, Corey", "McMillon, Jerry",
    "Powers, Harrison", "Estep, Dee", "Vance, Mark",
    "Solley, Caleb", "Leiter, Karen", "Strate, Brittany",
    "Carey, Edward", "Shelton, Kate", "Lounsbery, Tyler",
]

# =============================================================================
# ENTITY CLIENT FAMILIES
# Revenue is in THOUSANDS (e.g. 35.0 = $35,000/year)
# =============================================================================

ENTITY_CLUSTERS = [
    # --- Family 1: Real Estate Development (Midwest) ---
    {
        "cluster_name": "Thomson of Wisconsin Inc",
        "entities": [
            {"id": "E001", "name": "Thomson Management Inc", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_k": 72.0},
            {"id": "E002", "name": "Thomas Smits", "type": "Individual", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_k": 12.5},
            {"id": "E003", "name": "Sandra Vance", "type": "Individual", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_k": 11.0},
            {"id": "E004", "name": "Marcus Webb", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Northern Illinois", "revenue_k": 9.5},
            {"id": "E005", "name": "Diane Kowalski", "type": "Individual", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_k": 7.0},
            {"id": "E006", "name": "Smits Family Trust", "type": "1041 Trust", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_k": 18.0},
            {"id": "E007", "name": "Webb Construction LLC", "type": "1120S S-Corp", "industry": "Developers & Subdividers", "geography": "Northern Illinois", "revenue_k": 38.0},
            {"id": "E008", "name": "Thomson Property Mgmt LLC", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_k": 42.0},
            {"id": "E009", "name": "Alex Webb", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Northern Illinois", "revenue_k": 6.0},
            {"id": "E010", "name": "Vance Holdings LP", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_k": 55.0},
            {"id": "E011", "name": "Kowalski Family Trust", "type": "1041 Trust", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_k": 14.0},
            {"id": "E012", "name": "Thomson Retail Partners LP", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_k": 28.0},
            {"id": "E013", "name": "Laura Smits", "type": "Individual", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_k": 8.5},
        ],
        "relationships": [
            {"source": "E001", "target": "E002", "type": "partner_of", "ownership_pct": 35},
            {"source": "E001", "target": "E003", "type": "partner_of", "ownership_pct": 25},
            {"source": "E001", "target": "E004", "type": "partner_of", "ownership_pct": 20},
            {"source": "E001", "target": "E005", "type": "partner_of", "ownership_pct": 10},
            {"source": "E001", "target": "E006", "type": "partner_of", "ownership_pct": 10},
            {"source": "E006", "target": "E002", "type": "beneficiary_of"},
            {"source": "E004", "target": "E007", "type": "owner_of", "ownership_pct": 100},
            {"source": "E001", "target": "E008", "type": "working_partnership"},
            {"source": "E004", "target": "E009", "type": "dependent_of"},
            {"source": "E003", "target": "E010", "type": "partner_of", "ownership_pct": 50},
            {"source": "E001", "target": "E010", "type": "working_partnership"},
            {"source": "E005", "target": "E011", "type": "owner_of", "ownership_pct": 100},
            {"source": "E001", "target": "E012", "type": "owner_of", "ownership_pct": 80},
            {"source": "E002", "target": "E013", "type": "dependent_of"},
        ],
        "engagements": {
            "E001": ["Assurance", "Tax"],
            "E002": ["Tax"],
            "E003": ["Tax"],
            "E005": ["Tax"],
            "E006": ["Tax"],
            "E007": ["Tax", "Business Operations"],
            "E008": ["Tax", "Business Operations"],
            "E010": ["Assurance", "Tax"],
            "E011": ["Tax"],
            "E012": ["Tax"],
            "E013": ["Tax"],
        },
        "tenure_years": {"E001": 5, "E002": 5, "E003": 4, "E005": 4, "E006": 5, "E007": 2, "E008": 3, "E010": 2, "E011": 4, "E012": 1, "E013": 3},
    },
    # --- Family 2: Financial Services Group (Central) ---
    {
        "cluster_name": "Community Illinois Corporation",
        "entities": [
            {"id": "E014", "name": "CIC Capital Trust I", "type": "1065 Partnership", "industry": "Banks", "geography": "Central Illinois", "revenue_k": 85.0},
            {"id": "E015", "name": "Robert Scanlan", "type": "Individual", "industry": "Banks", "geography": "Central Illinois", "revenue_k": 14.0},
            {"id": "E016", "name": "Patricia Alvarez", "type": "Individual", "industry": "Banks", "geography": "Central Illinois", "revenue_k": 12.0},
            {"id": "E017", "name": "Merchants and Manufacturers Bank", "type": "1120 Corporation", "industry": "Banks", "geography": "Central Illinois", "revenue_k": 65.0},
            {"id": "E018", "name": "Busey Financial Corp", "type": "1120S S-Corp", "industry": "Banks", "geography": "Greater Missouri", "revenue_k": 45.0},
            {"id": "E019", "name": "Scanlan Family Foundation", "type": "1041 Trust", "industry": "Banks", "geography": "Central Illinois", "revenue_k": 22.0},
            {"id": "E020", "name": "David Scanlan", "type": "Individual", "industry": "Banks", "geography": "Central Illinois", "revenue_k": 8.0},
            {"id": "E021", "name": "Deere Credit Services Inc", "type": "1120 Corporation", "industry": "Specialty Finance", "geography": "Greater Iowa", "revenue_k": 48.0},
            {"id": "E022", "name": "Farmers State Bank & Trust", "type": "1065 Partnership", "industry": "Banks", "geography": "Central Illinois", "revenue_k": 32.0},
            {"id": "E023", "name": "Alvarez Consulting LLC", "type": "1120S S-Corp", "industry": "Banks", "geography": "Central Illinois", "revenue_k": 18.0},
            {"id": "E024", "name": "Scanlan Properties LP", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Central Illinois", "revenue_k": 25.0},
            {"id": "E025", "name": "Helen Scanlan", "type": "Individual", "industry": "Banks", "geography": "Central Illinois", "revenue_k": 9.0},
            {"id": "E026", "name": "CIC Mortgage Services Inc", "type": "1120S S-Corp", "industry": "Specialty Finance", "geography": "Central Illinois", "revenue_k": 35.0},
        ],
        "relationships": [
            {"source": "E014", "target": "E015", "type": "partner_of", "ownership_pct": 60},
            {"source": "E014", "target": "E016", "type": "partner_of", "ownership_pct": 40},
            {"source": "E014", "target": "E017", "type": "owner_of", "ownership_pct": 100},
            {"source": "E014", "target": "E018", "type": "owner_of", "ownership_pct": 100},
            {"source": "E015", "target": "E019", "type": "owner_of", "ownership_pct": 100},
            {"source": "E015", "target": "E020", "type": "dependent_of"},
            {"source": "E016", "target": "E021", "type": "owner_of", "ownership_pct": 100},
            {"source": "E014", "target": "E022", "type": "working_partnership"},
            {"source": "E016", "target": "E023", "type": "owner_of", "ownership_pct": 100},
            {"source": "E015", "target": "E024", "type": "owner_of", "ownership_pct": 75},
            {"source": "E015", "target": "E025", "type": "dependent_of"},
            {"source": "E014", "target": "E026", "type": "owner_of", "ownership_pct": 100},
        ],
        "engagements": {
            "E014": ["Assurance", "Tax", "Business Operations"],
            "E015": ["Tax"],
            "E016": ["Tax"],
            "E017": ["Assurance", "Tax"],
            "E018": ["Tax"],
            "E019": ["Tax"],
            "E022": ["Assurance"],
            "E023": ["Tax"],
            "E024": ["Tax"],
            "E025": ["Tax"],
            "E026": ["Tax", "Business Operations"],
        },
        "tenure_years": {"E014": 8, "E015": 7, "E016": 6, "E017": 6, "E018": 3, "E019": 7, "E022": 1, "E023": 4, "E024": 5, "E025": 7, "E026": 2},
    },
    # --- Family 3: Real Estate Investment (Florida) ---
    {
        "cluster_name": "Miromar Development Corporation",
        "entities": [
            {"id": "E027", "name": "Miromar Development Corporation", "type": "1065 Partnership", "industry": "Developers & Subdividers", "geography": "Greater Tampa Bay", "revenue_k": 78.0},
            {"id": "E028", "name": "Leonard Pratt", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Greater Tampa Bay", "revenue_k": 11.0},
            {"id": "E029", "name": "James Pomeroy", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Southwest Florida", "revenue_k": 13.0},
            {"id": "E030", "name": "Amy Costa", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Orlando", "revenue_k": 10.5},
            {"id": "E031", "name": "Costa Maggiore II HOA Inc", "type": "1120S S-Corp", "industry": "Developers & Subdividers", "geography": "Greater Tampa Bay", "revenue_k": 48.0},
            {"id": "E032", "name": "Miromar Outlet West LLC", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Greater Tampa Bay", "revenue_k": 35.0},
            {"id": "E033", "name": "Pratt Family Trust", "type": "1041 Trust", "industry": "Developers & Subdividers", "geography": "Greater Tampa Bay", "revenue_k": 16.0},
            {"id": "E034", "name": "Pomeroy Commercial Properties LP", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Southwest Florida", "revenue_k": 42.0},
            {"id": "E035", "name": "Liam Pratt", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Greater Tampa Bay", "revenue_k": 7.0},
            {"id": "E036", "name": "Costa Development Corp", "type": "1120S S-Corp", "industry": "Developers & Subdividers", "geography": "Orlando", "revenue_k": 28.0},
            {"id": "E037", "name": "Miromar Ventures Fund II", "type": "1065 Partnership", "industry": "Investor", "geography": "Greater Tampa Bay", "revenue_k": 55.0},
            {"id": "E038", "name": "Pratt Charitable Foundation", "type": "1041 Trust", "industry": "Developers & Subdividers", "geography": "Greater Tampa Bay", "revenue_k": 12.0},
            {"id": "E039", "name": "Gulf Coast Holdings LLC", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Southwest Florida", "revenue_k": 22.0},
        ],
        "relationships": [
            {"source": "E027", "target": "E028", "type": "partner_of", "ownership_pct": 40},
            {"source": "E027", "target": "E029", "type": "partner_of", "ownership_pct": 35},
            {"source": "E027", "target": "E030", "type": "partner_of", "ownership_pct": 25},
            {"source": "E027", "target": "E031", "type": "owner_of", "ownership_pct": 100},
            {"source": "E027", "target": "E032", "type": "owner_of", "ownership_pct": 100},
            {"source": "E028", "target": "E033", "type": "owner_of", "ownership_pct": 100},
            {"source": "E029", "target": "E034", "type": "partner_of", "ownership_pct": 50},
            {"source": "E028", "target": "E035", "type": "dependent_of"},
            {"source": "E030", "target": "E036", "type": "owner_of", "ownership_pct": 100},
            {"source": "E027", "target": "E037", "type": "owner_of", "ownership_pct": 80},
            {"source": "E028", "target": "E038", "type": "owner_of", "ownership_pct": 100},
            {"source": "E029", "target": "E039", "type": "owner_of", "ownership_pct": 60},
        ],
        "engagements": {
            "E027": ["Assurance", "Tax", "Digital"],
            "E028": ["Tax"],
            "E029": ["Tax"],
            "E031": ["Assurance", "Tax", "Business Operations"],
            "E032": ["Tax"],
            "E033": ["Tax"],
            "E034": ["Tax", "Assurance"],
            "E036": ["Tax"],
            "E037": ["Assurance", "Tax"],
            "E038": ["Tax"],
            "E039": ["Tax"],
        },
        "tenure_years": {"E027": 6, "E028": 6, "E029": 5, "E031": 4, "E032": 2, "E033": 6, "E034": 3, "E036": 2, "E037": 1, "E038": 5, "E039": 2},
    },
    # --- Family 4: Private Equity (West) ---
    {
        "cluster_name": "Pacific Assets Investment Corp",
        "entities": [
            {"id": "E040", "name": "Pacific Assets Investment Corporation", "type": "1065 Partnership", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_k": 95.0},
            {"id": "E041", "name": "Hae-Jeong Kim", "type": "Individual", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_k": 14.0},
            {"id": "E042", "name": "Samantha Reeves", "type": "Individual", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_k": 12.5},
            {"id": "E043", "name": "Meridian General Inc", "type": "1120 Corporation", "industry": "Lessors & Operators", "geography": "Southern California", "revenue_k": 62.0},
            {"id": "E044", "name": "Arlington Housing Corporation", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Southern California", "revenue_k": 38.0},
            {"id": "E045", "name": "Kim Family Office LP", "type": "1065 Partnership", "industry": "Specialty Finance", "geography": "Southern California", "revenue_k": 28.0},
            {"id": "E046", "name": "Reeves Capital Trust", "type": "1041 Trust", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_k": 19.0},
            {"id": "E047", "name": "Ethan Kim", "type": "Individual", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_k": 6.5},
            {"id": "E048", "name": "Catalina Island Camps Inc", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Southern California", "revenue_k": 32.0},
            {"id": "E049", "name": "Pacific Ventures Fund III LP", "type": "1065 Partnership", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_k": 55.0},
            {"id": "E050", "name": "Kim Charitable Trust", "type": "1041 Trust", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_k": 15.0},
            {"id": "E051", "name": "Reeves Advisory Group LLC", "type": "1120S S-Corp", "industry": "Specialty Finance", "geography": "Northern California", "revenue_k": 24.0},
            {"id": "E052", "name": "Harbor Point Properties Inc", "type": "1120 Corporation", "industry": "Lessors & Operators", "geography": "Southern California", "revenue_k": 45.0},
        ],
        "relationships": [
            {"source": "E040", "target": "E041", "type": "partner_of", "ownership_pct": 55},
            {"source": "E040", "target": "E042", "type": "partner_of", "ownership_pct": 45},
            {"source": "E040", "target": "E043", "type": "owner_of", "ownership_pct": 100},
            {"source": "E040", "target": "E044", "type": "owner_of", "ownership_pct": 100},
            {"source": "E041", "target": "E045", "type": "owner_of", "ownership_pct": 100},
            {"source": "E042", "target": "E046", "type": "owner_of", "ownership_pct": 100},
            {"source": "E041", "target": "E047", "type": "dependent_of"},
            {"source": "E040", "target": "E048", "type": "working_partnership"},
            {"source": "E040", "target": "E049", "type": "owner_of", "ownership_pct": 90},
            {"source": "E041", "target": "E050", "type": "owner_of", "ownership_pct": 100},
            {"source": "E042", "target": "E051", "type": "owner_of", "ownership_pct": 100},
            {"source": "E040", "target": "E052", "type": "owner_of", "ownership_pct": 75},
        ],
        "engagements": {
            "E040": ["Assurance", "Tax", "Digital"],
            "E041": ["Tax"],
            "E042": ["Tax"],
            "E043": ["Assurance", "Tax", "Business Operations", "Digital"],
            "E044": ["Tax", "Business Operations"],
            "E045": ["Tax"],
            "E046": ["Tax"],
            "E048": ["Tax"],
            "E049": ["Assurance", "Tax"],
            "E050": ["Tax"],
            "E052": ["Assurance", "Tax"],
        },
        "tenure_years": {"E040": 4, "E041": 4, "E042": 4, "E043": 7, "E044": 3, "E045": 2, "E046": 3, "E048": 2, "E049": 1, "E050": 3, "E052": 2},
    },
    # --- Family 5: Insurance & Finance (Northeast) ---
    {
        "cluster_name": "Intrum Corporation",
        "entities": [
            {"id": "E053", "name": "Intrum Corp", "type": "1065 Partnership", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_k": 110.0},
            {"id": "E054", "name": "William Graves", "type": "Individual", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_k": 15.0},
            {"id": "E055", "name": "Margaret Enverso", "type": "Individual", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_k": 13.5},
            {"id": "E056", "name": "Jonathan Fields", "type": "Individual", "industry": "Insurance", "geography": "Connecticut", "revenue_k": 12.0},
            {"id": "E057", "name": "ComProps Limited Partnership", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Southern New England", "revenue_k": 52.0},
            {"id": "E058", "name": "Tamid Reinsurance Ltd", "type": "1120 Corporation", "industry": "Insurance", "geography": "Connecticut", "revenue_k": 68.0},
            {"id": "E059", "name": "Graves Family Trust", "type": "1041 Trust", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_k": 20.0},
            {"id": "E060", "name": "Messina Commercial Properties LLC", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Southern New England", "revenue_k": 38.0},
            {"id": "E061", "name": "FXM Management Inc", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Southern New England", "revenue_k": 25.0},
            {"id": "E062", "name": "Caroline Graves", "type": "Individual", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_k": 7.5},
            {"id": "E063", "name": "Fields Insurance Agency LLC", "type": "1120S S-Corp", "industry": "Insurance", "geography": "Connecticut", "revenue_k": 30.0},
            {"id": "E064", "name": "Enverso Wealth Partners LP", "type": "1065 Partnership", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_k": 42.0},
            {"id": "E065", "name": "Graves Charitable Lead Trust", "type": "1041 Trust", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_k": 12.0},
        ],
        "relationships": [
            {"source": "E053", "target": "E054", "type": "partner_of", "ownership_pct": 40},
            {"source": "E053", "target": "E055", "type": "partner_of", "ownership_pct": 35},
            {"source": "E053", "target": "E056", "type": "partner_of", "ownership_pct": 25},
            {"source": "E053", "target": "E057", "type": "owner_of", "ownership_pct": 100},
            {"source": "E053", "target": "E058", "type": "owner_of", "ownership_pct": 100},
            {"source": "E054", "target": "E059", "type": "owner_of", "ownership_pct": 100},
            {"source": "E055", "target": "E060", "type": "owner_of", "ownership_pct": 50},
            {"source": "E056", "target": "E061", "type": "owner_of", "ownership_pct": 100},
            {"source": "E054", "target": "E062", "type": "dependent_of"},
            {"source": "E056", "target": "E063", "type": "owner_of", "ownership_pct": 100},
            {"source": "E055", "target": "E064", "type": "owner_of", "ownership_pct": 80},
            {"source": "E054", "target": "E065", "type": "owner_of", "ownership_pct": 100},
        ],
        "engagements": {
            "E053": ["Assurance", "Tax"],
            "E054": ["Tax"],
            "E055": ["Tax"],
            "E056": ["Tax"],
            "E057": ["Assurance", "Business Operations"],
            "E058": ["Assurance", "Tax"],
            "E059": ["Tax"],
            "E060": ["Tax"],
            "E061": ["Tax"],
            "E063": ["Tax", "Business Operations"],
            "E065": ["Tax"],
        },
        "tenure_years": {"E053": 10, "E054": 9, "E055": 8, "E056": 6, "E057": 5, "E058": 3, "E059": 9, "E060": 4, "E061": 3, "E063": 2, "E065": 8},
    },
    # --- Family 6: Banking (Upper Midwest) ---
    {
        "cluster_name": "Van Hoof Corporation & Subs",
        "entities": [
            {"id": "E066", "name": "Van Hoof Corporation", "type": "1065 Partnership", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_k": 58.0},
            {"id": "E067", "name": "Dale Behm", "type": "Individual", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_k": 11.0},
            {"id": "E068", "name": "Karen Yarrington", "type": "Individual", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_k": 10.0},
            {"id": "E069", "name": "Fulfillment Specialists Of America", "type": "1120 Corporation", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_k": 42.0},
            {"id": "E070", "name": "Oostburg State Bank", "type": "1120S S-Corp", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_k": 28.0},
            {"id": "E071", "name": "Androscoggin Bancshares LP", "type": "1065 Partnership", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_k": 35.0},
            {"id": "E072", "name": "Yarrington Land Trust", "type": "1041 Trust", "industry": "Banks", "geography": "Central Wisconsin", "revenue_k": 15.0},
            {"id": "E073", "name": "Tyler Behm", "type": "Individual", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_k": 6.0},
            {"id": "E074", "name": "Behm Capital Advisors LLC", "type": "1120S S-Corp", "industry": "Specialty Finance", "geography": "Northern Wisconsin", "revenue_k": 22.0},
            {"id": "E075", "name": "Northern Lakes Insurance Inc", "type": "1120 Corporation", "industry": "Insurance", "geography": "Central Wisconsin", "revenue_k": 30.0},
            {"id": "E076", "name": "Yarrington Holdings LP", "type": "1065 Partnership", "industry": "Banks", "geography": "Central Wisconsin", "revenue_k": 18.0},
            {"id": "E077", "name": "Behm Family Foundation", "type": "1041 Trust", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_k": 10.0},
        ],
        "relationships": [
            {"source": "E066", "target": "E067", "type": "partner_of", "ownership_pct": 50},
            {"source": "E066", "target": "E068", "type": "partner_of", "ownership_pct": 50},
            {"source": "E066", "target": "E069", "type": "owner_of", "ownership_pct": 100},
            {"source": "E066", "target": "E070", "type": "owner_of", "ownership_pct": 100},
            {"source": "E067", "target": "E071", "type": "owner_of", "ownership_pct": 70},
            {"source": "E068", "target": "E072", "type": "owner_of", "ownership_pct": 100},
            {"source": "E067", "target": "E073", "type": "dependent_of"},
            {"source": "E066", "target": "E071", "type": "working_partnership"},
            {"source": "E067", "target": "E074", "type": "owner_of", "ownership_pct": 100},
            {"source": "E066", "target": "E075", "type": "owner_of", "ownership_pct": 60},
            {"source": "E068", "target": "E076", "type": "owner_of", "ownership_pct": 100},
            {"source": "E067", "target": "E077", "type": "owner_of", "ownership_pct": 100},
        ],
        "engagements": {
            "E066": ["Assurance", "Tax"],
            "E067": ["Tax"],
            "E068": ["Tax"],
            "E069": ["Tax"],
            "E070": ["Tax", "Business Operations"],
            "E071": ["Tax", "Business Operations"],
            "E072": ["Tax"],
            "E074": ["Tax"],
            "E075": ["Assurance", "Tax"],
            "E076": ["Tax"],
            "E077": ["Tax"],
        },
        "tenure_years": {"E066": 12, "E067": 11, "E068": 10, "E069": 3, "E070": 4, "E071": 2, "E072": 9, "E074": 3, "E075": 5, "E076": 4, "E077": 10},
    },
    # --- Family 7: Real Estate Investment (Texas) ---
    {
        "cluster_name": "Conti Capital",
        "entities": [
            {"id": "E078", "name": "Conti Capital LP", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_k": 68.0},
            {"id": "E079", "name": "Angela Estep", "type": "Individual", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_k": 12.0},
            {"id": "E080", "name": "Brian Donnell", "type": "Individual", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_k": 10.5},
            {"id": "E081", "name": "Conti ROM Corp", "type": "1120 Corporation", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_k": 42.0},
            {"id": "E082", "name": "BIP Multifamily Fund I LP", "type": "1065 Partnership", "industry": "Investor", "geography": "Northern Texas", "revenue_k": 35.0},
            {"id": "E083", "name": "Estep Foundation", "type": "1041 Trust", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_k": 14.0},
            {"id": "E084", "name": "Sofia Estep", "type": "Individual", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_k": 6.5},
            {"id": "E085", "name": "Donnell Development LLC", "type": "1120S S-Corp", "industry": "Developers & Subdividers", "geography": "Northern Texas", "revenue_k": 28.0},
            {"id": "E086", "name": "Conti Senior Living Fund LP", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Central Texas", "revenue_k": 45.0},
            {"id": "E087", "name": "Estep Wealth Trust", "type": "1041 Trust", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_k": 18.0},
            {"id": "E088", "name": "DFW Property Services Inc", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_k": 22.0},
            {"id": "E089", "name": "Richard Estep", "type": "Individual", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_k": 9.0},
        ],
        "relationships": [
            {"source": "E078", "target": "E079", "type": "partner_of", "ownership_pct": 55},
            {"source": "E078", "target": "E080", "type": "partner_of", "ownership_pct": 45},
            {"source": "E078", "target": "E081", "type": "owner_of", "ownership_pct": 100},
            {"source": "E080", "target": "E082", "type": "owner_of", "ownership_pct": 100},
            {"source": "E079", "target": "E083", "type": "owner_of", "ownership_pct": 100},
            {"source": "E079", "target": "E084", "type": "dependent_of"},
            {"source": "E080", "target": "E085", "type": "owner_of", "ownership_pct": 100},
            {"source": "E078", "target": "E086", "type": "owner_of", "ownership_pct": 85},
            {"source": "E079", "target": "E087", "type": "owner_of", "ownership_pct": 100},
            {"source": "E078", "target": "E088", "type": "owner_of", "ownership_pct": 100},
            {"source": "E079", "target": "E089", "type": "dependent_of"},
        ],
        "engagements": {
            "E078": ["Assurance", "Tax", "Business Operations", "Digital"],
            "E079": ["Tax"],
            "E080": ["Tax"],
            "E081": ["Tax", "Business Operations"],
            "E082": ["Tax"],
            "E083": ["Tax"],
            "E085": ["Tax"],
            "E086": ["Assurance", "Tax"],
            "E087": ["Tax"],
            "E088": ["Tax", "Business Operations"],
            "E089": ["Tax"],
        },
        "tenure_years": {"E078": 3, "E079": 3, "E080": 3, "E081": 2, "E082": 1, "E083": 3, "E085": 2, "E086": 1, "E087": 3, "E088": 2, "E089": 2},
    },
    # --- Family 8: Real Estate (Carolinas/Atlanta) ---
    {
        "cluster_name": "Galosa LLC",
        "entities": [
            {"id": "E090", "name": "Galosa LLC", "type": "1065 Partnership", "industry": "Investor", "geography": "Atlanta", "revenue_k": 62.0},
            {"id": "E091", "name": "Michael DiNatale", "type": "Individual", "industry": "Investor", "geography": "Greater Carolinas", "revenue_k": 13.0},
            {"id": "E092", "name": "Lisa Lankford", "type": "Individual", "industry": "Investor", "geography": "Atlanta", "revenue_k": 11.0},
            {"id": "E093", "name": "KERUPE LLC", "type": "1120 Corporation", "industry": "Investor", "geography": "Central Texas", "revenue_k": 48.0},
            {"id": "E094", "name": "Williams & Fudge Inc", "type": "1120S S-Corp", "industry": "Banks", "geography": "Greater Carolinas", "revenue_k": 30.0},
            {"id": "E095", "name": "Yelloledbedder Inc", "type": "1120S S-Corp", "industry": "Other Real Estate", "geography": "Atlanta", "revenue_k": 22.0},
            {"id": "E096", "name": "Risk Reduction Plus Group Inc", "type": "1065 Partnership", "industry": "Investor", "geography": "Greater Philadelphia", "revenue_k": 38.0},
            {"id": "E097", "name": "DiNatale Family Trust", "type": "1041 Trust", "industry": "Investor", "geography": "Greater Carolinas", "revenue_k": 14.0},
            {"id": "E098", "name": "Lankford Advisory LLC", "type": "1120S S-Corp", "industry": "Investor", "geography": "Atlanta", "revenue_k": 18.0},
            {"id": "E099", "name": "Southeastern Capital Fund LP", "type": "1065 Partnership", "industry": "Investor", "geography": "Atlanta", "revenue_k": 42.0},
            {"id": "E100", "name": "DiNatale Holdings Inc", "type": "1120 Corporation", "industry": "Investor", "geography": "Greater Carolinas", "revenue_k": 25.0},
        ],
        "relationships": [
            {"source": "E090", "target": "E091", "type": "partner_of", "ownership_pct": 50},
            {"source": "E090", "target": "E092", "type": "partner_of", "ownership_pct": 50},
            {"source": "E090", "target": "E093", "type": "owner_of", "ownership_pct": 100},
            {"source": "E091", "target": "E094", "type": "owner_of", "ownership_pct": 100},
            {"source": "E092", "target": "E095", "type": "owner_of", "ownership_pct": 100},
            {"source": "E090", "target": "E096", "type": "owner_of", "ownership_pct": 60},
            {"source": "E091", "target": "E097", "type": "owner_of", "ownership_pct": 100},
            {"source": "E092", "target": "E098", "type": "owner_of", "ownership_pct": 100},
            {"source": "E090", "target": "E099", "type": "owner_of", "ownership_pct": 70},
            {"source": "E091", "target": "E100", "type": "owner_of", "ownership_pct": 100},
        ],
        "engagements": {
            "E090": ["Assurance", "Tax"],
            "E091": ["Tax"],
            "E092": ["Tax"],
            "E093": ["Assurance"],
            "E094": ["Tax", "Business Operations"],
            "E095": ["Tax"],
            "E096": ["Tax"],
            "E097": ["Tax"],
            "E098": ["Tax"],
            "E099": ["Assurance", "Tax"],
        },
        "tenure_years": {"E090": 5, "E091": 5, "E092": 4, "E093": 1, "E094": 3, "E095": 2, "E096": 2, "E097": 5, "E098": 3, "E099": 1},
    },
    # --- Family 9: Healthcare & Non-Profit (Midwest) ---
    {
        "cluster_name": "Heartland Health Systems",
        "entities": [
            {"id": "E101", "name": "Heartland Health Systems Inc", "type": "1120 Corporation", "industry": "Insurance", "geography": "Greater Indiana", "revenue_k": 88.0},
            {"id": "E102", "name": "Dr. Rajan Patel", "type": "Individual", "industry": "Insurance", "geography": "Greater Indiana", "revenue_k": 14.0},
            {"id": "E103", "name": "Sharon Whitfield", "type": "Individual", "industry": "Insurance", "geography": "Western Ohio", "revenue_k": 11.5},
            {"id": "E104", "name": "Patel Medical Group LLC", "type": "1120S S-Corp", "industry": "Insurance", "geography": "Greater Indiana", "revenue_k": 42.0},
            {"id": "E105", "name": "Whitfield Family Foundation", "type": "1041 Trust", "industry": "Insurance", "geography": "Western Ohio", "revenue_k": 18.0},
            {"id": "E106", "name": "Heartland Physician Partners LP", "type": "1065 Partnership", "industry": "Insurance", "geography": "Greater Indiana", "revenue_k": 55.0},
            {"id": "E107", "name": "Midwest Wellness Corp", "type": "1120 Corporation", "industry": "Insurance", "geography": "Eastern Ohio", "revenue_k": 35.0},
            {"id": "E108", "name": "Patel Charitable Trust", "type": "1041 Trust", "industry": "Insurance", "geography": "Greater Indiana", "revenue_k": 12.0},
            {"id": "E109", "name": "Anita Patel", "type": "Individual", "industry": "Insurance", "geography": "Greater Indiana", "revenue_k": 8.0},
            {"id": "E110", "name": "Whitfield Realty Holdings", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Western Ohio", "revenue_k": 28.0},
            {"id": "E111", "name": "HealthFirst Consulting LLC", "type": "1120S S-Corp", "industry": "Insurance", "geography": "Greater Indiana", "revenue_k": 20.0},
            {"id": "E112", "name": "Kevin Whitfield", "type": "Individual", "industry": "Insurance", "geography": "Western Ohio", "revenue_k": 7.0},
        ],
        "relationships": [
            {"source": "E101", "target": "E102", "type": "partner_of", "ownership_pct": 45},
            {"source": "E101", "target": "E103", "type": "partner_of", "ownership_pct": 35},
            {"source": "E102", "target": "E104", "type": "owner_of", "ownership_pct": 100},
            {"source": "E103", "target": "E105", "type": "owner_of", "ownership_pct": 100},
            {"source": "E101", "target": "E106", "type": "owner_of", "ownership_pct": 80},
            {"source": "E101", "target": "E107", "type": "owner_of", "ownership_pct": 100},
            {"source": "E102", "target": "E108", "type": "owner_of", "ownership_pct": 100},
            {"source": "E102", "target": "E109", "type": "dependent_of"},
            {"source": "E103", "target": "E110", "type": "owner_of", "ownership_pct": 100},
            {"source": "E101", "target": "E111", "type": "working_partnership"},
            {"source": "E103", "target": "E112", "type": "dependent_of"},
        ],
        "engagements": {
            "E101": ["Assurance", "Tax", "Business Operations"],
            "E102": ["Tax"],
            "E103": ["Tax"],
            "E104": ["Tax", "Business Operations"],
            "E105": ["Tax"],
            "E106": ["Assurance", "Tax"],
            "E107": ["Tax"],
            "E108": ["Tax"],
            "E109": ["Tax"],
            "E110": ["Tax"],
        },
        "tenure_years": {"E101": 6, "E102": 6, "E103": 5, "E104": 4, "E105": 5, "E106": 3, "E107": 2, "E108": 5, "E109": 4, "E110": 3},
    },
    # --- Family 10: Agricultural Holdings (Upper Midwest) ---
    {
        "cluster_name": "Prairie Grain Cooperative",
        "entities": [
            {"id": "E113", "name": "Prairie Grain Cooperative", "type": "1065 Partnership", "industry": "Other Real Estate", "geography": "Greater Iowa", "revenue_k": 72.0},
            {"id": "E114", "name": "Harold Swenson", "type": "Individual", "industry": "Other Real Estate", "geography": "Greater Iowa", "revenue_k": 12.0},
            {"id": "E115", "name": "Betty Mueller", "type": "Individual", "industry": "Other Real Estate", "geography": "Southern Minnesota", "revenue_k": 10.0},
            {"id": "E116", "name": "Carl Johansson", "type": "Individual", "industry": "Other Real Estate", "geography": "Greater Iowa", "revenue_k": 9.5},
            {"id": "E117", "name": "Swenson Farms LLC", "type": "1120S S-Corp", "industry": "Other Real Estate", "geography": "Greater Iowa", "revenue_k": 32.0},
            {"id": "E118", "name": "Mueller Land Trust", "type": "1041 Trust", "industry": "Other Real Estate", "geography": "Southern Minnesota", "revenue_k": 18.0},
            {"id": "E119", "name": "Johansson Equipment Inc", "type": "1120 Corporation", "industry": "Other Real Estate", "geography": "Greater Iowa", "revenue_k": 25.0},
            {"id": "E120", "name": "Prairie Storage Solutions LP", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Greater Iowa", "revenue_k": 38.0},
            {"id": "E121", "name": "Swenson Family Trust", "type": "1041 Trust", "industry": "Other Real Estate", "geography": "Greater Iowa", "revenue_k": 14.0},
            {"id": "E122", "name": "Erik Swenson", "type": "Individual", "industry": "Other Real Estate", "geography": "Greater Iowa", "revenue_k": 7.5},
            {"id": "E123", "name": "Heartland Ag Finance Corp", "type": "1120S S-Corp", "industry": "Specialty Finance", "geography": "Greater Iowa", "revenue_k": 28.0},
            {"id": "E124", "name": "Mueller Dairy Operations LLC", "type": "1120S S-Corp", "industry": "Other Real Estate", "geography": "Southern Minnesota", "revenue_k": 35.0},
        ],
        "relationships": [
            {"source": "E113", "target": "E114", "type": "partner_of", "ownership_pct": 35},
            {"source": "E113", "target": "E115", "type": "partner_of", "ownership_pct": 35},
            {"source": "E113", "target": "E116", "type": "partner_of", "ownership_pct": 30},
            {"source": "E114", "target": "E117", "type": "owner_of", "ownership_pct": 100},
            {"source": "E115", "target": "E118", "type": "owner_of", "ownership_pct": 100},
            {"source": "E116", "target": "E119", "type": "owner_of", "ownership_pct": 100},
            {"source": "E113", "target": "E120", "type": "owner_of", "ownership_pct": 60},
            {"source": "E114", "target": "E121", "type": "owner_of", "ownership_pct": 100},
            {"source": "E114", "target": "E122", "type": "dependent_of"},
            {"source": "E113", "target": "E123", "type": "working_partnership"},
            {"source": "E115", "target": "E124", "type": "owner_of", "ownership_pct": 100},
        ],
        "engagements": {
            "E113": ["Assurance", "Tax"],
            "E114": ["Tax"],
            "E115": ["Tax"],
            "E116": ["Tax"],
            "E117": ["Tax", "Business Operations"],
            "E118": ["Tax"],
            "E119": ["Tax"],
            "E120": ["Tax", "Assurance"],
            "E121": ["Tax"],
            "E124": ["Tax", "Business Operations"],
        },
        "tenure_years": {"E113": 15, "E114": 14, "E115": 12, "E116": 10, "E117": 8, "E118": 11, "E119": 6, "E120": 4, "E121": 13, "E124": 5},
    },
    # --- Family 11: Construction & Development (Mountain West) ---
    {
        "cluster_name": "Summit Ridge Partners",
        "entities": [
            {"id": "E125", "name": "Summit Ridge Partners LP", "type": "1065 Partnership", "industry": "Developers & Subdividers", "geography": "Rocky Mountains", "revenue_k": 65.0},
            {"id": "E126", "name": "Nathan Torres", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Rocky Mountains", "revenue_k": 13.0},
            {"id": "E127", "name": "Michelle Chang", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Greater Southwest", "revenue_k": 11.0},
            {"id": "E128", "name": "Torres Construction Group Inc", "type": "1120 Corporation", "industry": "Developers & Subdividers", "geography": "Rocky Mountains", "revenue_k": 48.0},
            {"id": "E129", "name": "Chang Design Studio LLC", "type": "1120S S-Corp", "industry": "Developers & Subdividers", "geography": "Greater Southwest", "revenue_k": 22.0},
            {"id": "E130", "name": "Summit Commercial Fund II", "type": "1065 Partnership", "industry": "Investor", "geography": "Rocky Mountains", "revenue_k": 40.0},
            {"id": "E131", "name": "Torres Family Trust", "type": "1041 Trust", "industry": "Developers & Subdividers", "geography": "Rocky Mountains", "revenue_k": 15.0},
            {"id": "E132", "name": "Alpine Property Mgmt LLC", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Rocky Mountains", "revenue_k": 28.0},
            {"id": "E133", "name": "Chang Holdings LP", "type": "1065 Partnership", "industry": "Investor", "geography": "Greater Southwest", "revenue_k": 32.0},
            {"id": "E134", "name": "Marco Torres", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Rocky Mountains", "revenue_k": 7.0},
            {"id": "E135", "name": "Summit Residential Inc", "type": "1120S S-Corp", "industry": "Developers & Subdividers", "geography": "Rocky Mountains", "revenue_k": 35.0},
        ],
        "relationships": [
            {"source": "E125", "target": "E126", "type": "partner_of", "ownership_pct": 55},
            {"source": "E125", "target": "E127", "type": "partner_of", "ownership_pct": 45},
            {"source": "E126", "target": "E128", "type": "owner_of", "ownership_pct": 100},
            {"source": "E127", "target": "E129", "type": "owner_of", "ownership_pct": 100},
            {"source": "E125", "target": "E130", "type": "owner_of", "ownership_pct": 75},
            {"source": "E126", "target": "E131", "type": "owner_of", "ownership_pct": 100},
            {"source": "E125", "target": "E132", "type": "owner_of", "ownership_pct": 100},
            {"source": "E127", "target": "E133", "type": "owner_of", "ownership_pct": 80},
            {"source": "E126", "target": "E134", "type": "dependent_of"},
            {"source": "E125", "target": "E135", "type": "owner_of", "ownership_pct": 100},
        ],
        "engagements": {
            "E125": ["Assurance", "Tax", "Digital"],
            "E126": ["Tax"],
            "E127": ["Tax"],
            "E128": ["Tax", "Business Operations"],
            "E129": ["Tax"],
            "E130": ["Tax", "Assurance"],
            "E131": ["Tax"],
            "E132": ["Tax"],
            "E133": ["Tax"],
            "E135": ["Tax", "Business Operations"],
        },
        "tenure_years": {"E125": 4, "E126": 4, "E127": 3, "E128": 4, "E129": 2, "E130": 2, "E131": 4, "E132": 3, "E133": 2, "E135": 1},
    },
    # --- Family 12: Credit Union Network (Pacific Northwest) ---
    {
        "cluster_name": "Cascade Financial Group",
        "entities": [
            {"id": "E136", "name": "Cascade Financial Group LP", "type": "1065 Partnership", "industry": "Credit Unions", "geography": "Pacific Northwest", "revenue_k": 75.0},
            {"id": "E137", "name": "David Olsen", "type": "Individual", "industry": "Credit Unions", "geography": "Pacific Northwest", "revenue_k": 12.0},
            {"id": "E138", "name": "Jennifer Nakamura", "type": "Individual", "industry": "Credit Unions", "geography": "Pacific Northwest", "revenue_k": 11.5},
            {"id": "E139", "name": "Puget Sound Credit Union", "type": "1120 Corporation", "industry": "Credit Unions", "geography": "Pacific Northwest", "revenue_k": 52.0},
            {"id": "E140", "name": "Columbia River Federal CU", "type": "1120 Corporation", "industry": "Credit Unions", "geography": "Pacific Northwest", "revenue_k": 38.0},
            {"id": "E141", "name": "Olsen Wealth Trust", "type": "1041 Trust", "industry": "Credit Unions", "geography": "Pacific Northwest", "revenue_k": 16.0},
            {"id": "E142", "name": "Nakamura Investments LLC", "type": "1120S S-Corp", "industry": "Specialty Finance", "geography": "Pacific Northwest", "revenue_k": 24.0},
            {"id": "E143", "name": "Cascade Insurance Services", "type": "1120S S-Corp", "industry": "Insurance", "geography": "Pacific Northwest", "revenue_k": 30.0},
            {"id": "E144", "name": "Olsen Properties LP", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Pacific Northwest", "revenue_k": 28.0},
            {"id": "E145", "name": "Emily Olsen", "type": "Individual", "industry": "Credit Unions", "geography": "Pacific Northwest", "revenue_k": 6.5},
            {"id": "E146", "name": "Northwest Fintech Corp", "type": "1120 Corporation", "industry": "Specialty Finance", "geography": "Pacific Northwest", "revenue_k": 35.0},
            {"id": "E147", "name": "Cascade Charitable Foundation", "type": "1041 Trust", "industry": "Credit Unions", "geography": "Pacific Northwest", "revenue_k": 10.0},
            {"id": "E148", "name": "Nakamura Family Trust", "type": "1041 Trust", "industry": "Credit Unions", "geography": "Pacific Northwest", "revenue_k": 12.0},
        ],
        "relationships": [
            {"source": "E136", "target": "E137", "type": "partner_of", "ownership_pct": 50},
            {"source": "E136", "target": "E138", "type": "partner_of", "ownership_pct": 50},
            {"source": "E136", "target": "E139", "type": "owner_of", "ownership_pct": 100},
            {"source": "E136", "target": "E140", "type": "owner_of", "ownership_pct": 100},
            {"source": "E137", "target": "E141", "type": "owner_of", "ownership_pct": 100},
            {"source": "E138", "target": "E142", "type": "owner_of", "ownership_pct": 100},
            {"source": "E136", "target": "E143", "type": "owner_of", "ownership_pct": 80},
            {"source": "E137", "target": "E144", "type": "owner_of", "ownership_pct": 100},
            {"source": "E137", "target": "E145", "type": "dependent_of"},
            {"source": "E136", "target": "E146", "type": "working_partnership"},
            {"source": "E136", "target": "E147", "type": "owner_of", "ownership_pct": 100},
            {"source": "E138", "target": "E148", "type": "owner_of", "ownership_pct": 100},
        ],
        "engagements": {
            "E136": ["Assurance", "Tax", "Business Operations"],
            "E137": ["Tax"],
            "E138": ["Tax"],
            "E139": ["Assurance", "Tax"],
            "E140": ["Assurance", "Tax"],
            "E141": ["Tax"],
            "E142": ["Tax"],
            "E143": ["Tax", "Business Operations"],
            "E144": ["Tax"],
            "E147": ["Tax"],
            "E148": ["Tax"],
        },
        "tenure_years": {"E136": 7, "E137": 7, "E138": 6, "E139": 5, "E140": 4, "E141": 6, "E142": 3, "E143": 4, "E144": 5, "E147": 6, "E148": 4},
    },
]


# =============================================================================
# HEALTH CALCULATION — Tenure-aware
# =============================================================================

def compute_health(days_since_activity: int, tenure_years: int, num_services: int) -> str:
    """
    Compute health status factoring in tenure.
    Long-term clients (3+ years) with recurring contracts are considered
    stable even with slightly aged AR. Tenure provides a buffer of ~5 days
    per year (capped at 30). Multi-service clients get additional resilience.
    """
    tenure_buffer = min(tenure_years * 5, 30)
    service_buffer = (num_services - 1) * 5

    effective_days = max(0, days_since_activity - tenure_buffer - service_buffer)

    if effective_days < 30:
        return "Healthy"
    elif effective_days < 60:
        return "Strained"
    else:
        return "Poor"


# =============================================================================
# DATA GENERATION FUNCTIONS
# =============================================================================

def get_all_entities() -> pd.DataFrame:
    """
    Get all entities with engagement status and health scoring.
    Health factors: days since last activity, tenure (years with CLA),
    and number of service lines engaged.
    """
    records = []

    for cluster in ENTITY_CLUSTERS:
        cluster_name = cluster["cluster_name"]
        engagements = cluster["engagements"]
        tenure_map = cluster.get("tenure_years", {})

        for entity in cluster["entities"]:
            eid = entity["id"]
            is_served = eid in engagements
            services_engaged = engagements.get(eid, [])
            services_not_engaged = [s for s in SERVICE_LINES if s not in services_engaged]

            seamless_score = len(services_engaged)
            is_seamless = seamless_score >= 2

            years_with_cla = tenure_map.get(eid, 0)

            if is_served:
                if years_with_cla >= 5:
                    days_since_activity = random.choices(
                        [random.randint(1, 20), random.randint(15, 40), random.randint(35, 70)],
                        weights=[0.75, 0.20, 0.05]
                    )[0]
                elif years_with_cla >= 3:
                    days_since_activity = random.choices(
                        [random.randint(1, 25), random.randint(20, 50), random.randint(45, 85)],
                        weights=[0.65, 0.25, 0.10]
                    )[0]
                else:
                    days_since_activity = random.choices(
                        [random.randint(1, 29), random.randint(25, 59), random.randint(50, 100)],
                        weights=[0.55, 0.30, 0.15]
                    )[0]

                health_status = compute_health(days_since_activity, years_with_cla, seamless_score)
                last_activity_date = (datetime.now() - timedelta(days=days_since_activity)).strftime("%Y-%m-%d")
            else:
                days_since_activity = None
                health_status = "Not Engaged"
                last_activity_date = None

            crl_idx = hash(cluster_name) % len(CRL_NAMES)
            crl = CRL_NAMES[crl_idx] if is_served else None

            if is_served:
                consent = random.choices(["Granted", "Pending", "Not Requested"], weights=[0.4, 0.3, 0.3])[0]
            else:
                consent = "Not Applicable"

            records.append({
                "entity_id": eid,
                "entity_name": entity["name"],
                "entity_type": entity["type"],
                "cluster_name": cluster_name,
                "industry": entity["industry"],
                "geography": entity["geography"],
                "annual_revenue_k": entity["revenue_k"],
                "is_served": is_served,
                "services_engaged": services_engaged,
                "services_not_engaged": services_not_engaged,
                "num_services": len(services_engaged),
                "seamless_score": seamless_score,
                "is_seamless": is_seamless,
                "years_with_cla": years_with_cla,
                "health_status": health_status,
                "days_since_activity": days_since_activity,
                "last_activity_date": last_activity_date,
                "crl_owner": crl,
                "consent_status": consent,
            })

    return pd.DataFrame(records)


def get_all_relationships() -> pd.DataFrame:
    """Get all entity-to-entity relationship edges for the client family graph."""
    records = []

    for cluster in ENTITY_CLUSTERS:
        cluster_name = cluster["cluster_name"]
        engagements = cluster["engagements"]
        entity_lookup = {e["id"]: e["name"] for e in cluster["entities"]}

        for rel in cluster["relationships"]:
            records.append({
                "source_id": rel["source"],
                "source_name": entity_lookup.get(rel["source"], "Unknown"),
                "target_id": rel["target"],
                "target_name": entity_lookup.get(rel["target"], "Unknown"),
                "relationship_type": rel["type"],
                "ownership_pct": rel.get("ownership_pct"),
                "cluster_name": cluster_name,
                "source_served": rel["source"] in engagements,
                "target_served": rel["target"] in engagements,
            })

    return pd.DataFrame(records)


def get_billing_history() -> pd.DataFrame:
    """Billing history for served entities — quarterly, last 2 years, with AR aging."""
    records = []
    entities_df = get_all_entities()
    served = entities_df[entities_df["is_served"]]

    quarters = []
    for yr in [2024, 2025, 2026]:
        for q in [1, 2, 3, 4]:
            if yr == 2026 and q > 2:
                break
            quarters.append(f"{yr}-Q{q}")

    for _, entity in served.iterrows():
        base_quarterly = entity["annual_revenue_k"] * 1_000 / 4  # quarterly in dollars
        num_services = len(entity["services_engaged"])
        if num_services == 0:
            continue

        for service in entity["services_engaged"]:
            svc_share = base_quarterly / num_services

            for quarter in quarters:
                if random.random() < 0.92:
                    amount = svc_share * random.uniform(0.85, 1.15)

                    if quarter == quarters[-1]:
                        days_outstanding = random.choices(
                            [0, 15, 35, 65],
                            weights=[0.70, 0.15, 0.10, 0.05]
                        )[0]
                    else:
                        days_outstanding = 0

                    paid = round(amount if days_outstanding == 0 else 0, 2)
                    outstanding = round(amount if days_outstanding > 0 else 0, 2)

                    records.append({
                        "entity_id": entity["entity_id"],
                        "entity_name": entity["entity_name"],
                        "cluster_name": entity["cluster_name"],
                        "period": quarter,
                        "service_line": service,
                        "billed_amount": round(amount, 2),
                        "paid_amount": paid,
                        "outstanding_amount": outstanding,
                        "days_outstanding": days_outstanding,
                    })

    return pd.DataFrame(records)


def get_cluster_summary() -> pd.DataFrame:
    """Summarize each client family for the One-Firm view."""
    entities_df = get_all_entities()
    records = []

    for cluster_name in entities_df["cluster_name"].unique():
        cluster_ents = entities_df[entities_df["cluster_name"] == cluster_name]
        served = cluster_ents[cluster_ents["is_served"]]

        records.append({
            "cluster_name": cluster_name,
            "total_entities": len(cluster_ents),
            "served_entities": len(served),
            "unserved_entities": len(cluster_ents) - len(served),
            "total_revenue_k": round(cluster_ents["annual_revenue_k"].sum(), 1),
            "served_revenue_k": round(served["annual_revenue_k"].sum(), 1),
            "penetration_pct": round(len(served) / len(cluster_ents) * 100, 1) if len(cluster_ents) > 0 else 0,
            "industries": cluster_ents["industry"].nunique(),
            "geographies": cluster_ents["geography"].nunique(),
            "avg_seamless": round(served["seamless_score"].mean(), 1) if len(served) > 0 else 0,
            "avg_tenure_years": round(served["years_with_cla"].mean(), 1) if len(served) > 0 else 0,
            "healthy_count": len(served[served["health_status"] == "Healthy"]),
            "strained_count": len(served[served["health_status"] == "Strained"]),
            "poor_count": len(served[served["health_status"] == "Poor"]),
        })

    return pd.DataFrame(records)


def get_opportunities() -> pd.DataFrame:
    """
    Two types:
    1. Unserved entities in client families (red nodes)
    2. Served entities with service gaps (seamless growth)
    """
    entities_df = get_all_entities()
    opportunities = []

    for _, entity in entities_df.iterrows():
        if not entity["is_served"] and entity["annual_revenue_k"] > 0:
            opportunities.append({
                "entity_id": entity["entity_id"],
                "entity_name": entity["entity_name"],
                "entity_type": entity["entity_type"],
                "cluster_name": entity["cluster_name"],
                "industry": entity["industry"],
                "geography": entity["geography"],
                "revenue_k": entity["annual_revenue_k"],
                "opportunity_type": "New Engagement (Red Node)",
                "available_services": SERVICE_LINES.copy(),
                "num_available_services": len(SERVICE_LINES),
                "seamless_potential": True,
                "priority_score": round(entity["annual_revenue_k"] * 0.15, 1),
            })
        elif entity["is_served"] and entity["services_not_engaged"]:
            opportunities.append({
                "entity_id": entity["entity_id"],
                "entity_name": entity["entity_name"],
                "entity_type": entity["entity_type"],
                "cluster_name": entity["cluster_name"],
                "industry": entity["industry"],
                "geography": entity["geography"],
                "revenue_k": entity["annual_revenue_k"],
                "opportunity_type": "Service Gap (Seamless Growth)",
                "available_services": entity["services_not_engaged"],
                "num_available_services": len(entity["services_not_engaged"]),
                "seamless_potential": len(entity["services_engaged"]) >= 1,
                "priority_score": round(entity["annual_revenue_k"] * len(entity["services_not_engaged"]) * 0.05, 1),
            })

    df = pd.DataFrame(opportunities)
    return df.sort_values("priority_score", ascending=False).reset_index(drop=True)


def get_seamless_analysis() -> pd.DataFrame:
    """Analyze seamless vs single-service clients for retention risk."""
    entities_df = get_all_entities()
    served = entities_df[entities_df["is_served"]].copy()

    served["seamless_status"] = served["num_services"].apply(
        lambda x: "Fully Seamless (3+)" if x >= 3
        else "Partially Seamless (2)" if x == 2
        else "Single Service (At Risk)"
    )
    return served


def get_interaction_history():
    """Generate realistic interaction history for check-in tracking."""
    entities_df = get_all_entities()
    served = entities_df[entities_df["is_served"]]
    records = []
    interaction_types = ["In-Person Meeting", "Phone Call", "Video Call", "Email Exchange", "Client Event", "Informal (Lunch/Coffee)"]
    health_signals = ["Healthy — no concerns", "Mentioned competing firms", "Payment delay mentioned", "Very engaged", "Key contact leaving", "Expressed fee concerns"]

    for month_offset in range(12):
        month_date = datetime.now() - timedelta(days=30 * month_offset)
        for _ in range(random.randint(20, 45)):
            entity = served.sample(1).iloc[0]
            interaction_date = (month_date - timedelta(days=random.randint(0, 29))).strftime("%Y-%m-%d")
            services_discussed = random.sample(SERVICE_LINES, k=random.randint(1, 3))
            records.append({
                "entity_name": entity["entity_name"],
                "cluster_name": entity["cluster_name"],
                "interaction_date": interaction_date,
                "interaction_type": random.choice(interaction_types),
                "crl_name": entity["crl_owner"],
                "services_discussed": ", ".join(services_discussed),
                "new_entities_found": random.choice(["Yes", "No", "No", "No", "No"]),
                "health_signal": random.choice(health_signals),
                "consent_status": random.choice(["Granted", "Pending", "Not Discussed", "Not Discussed"]),
            })
    return pd.DataFrame(records)


def get_crl_actions(crl_name: str = None):
    """
    Generate upcoming actions/tasks for a CRL — check-ins, meetings, follow-ups.
    Returns a DataFrame with action items categorised by urgency.
    """
    entities_df = get_all_entities()
    if crl_name:
        crl_entities = entities_df[(entities_df["crl_owner"] == crl_name) & (entities_df["is_served"])]
    else:
        crl_entities = entities_df[entities_df["is_served"]]

    records = []
    action_types = ["Check-In Call", "Quarterly Review", "Proposal Follow-Up", "Health Check", "Contract Renewal"]

    for _, entity in crl_entities.iterrows():
        if entity["health_status"] in ["Strained", "Poor"] or (entity["days_since_activity"] and entity["days_since_activity"] > 30):
            records.append({
                "entity_name": entity["entity_name"],
                "cluster_name": entity["cluster_name"],
                "action_type": "Health Check" if entity["health_status"] == "Poor" else "Check-In Call",
                "urgency": "Immediate",
                "due_date": (datetime.now() + timedelta(days=random.randint(0, 2))).strftime("%Y-%m-%d"),
                "crl_owner": entity["crl_owner"],
            })

        if random.random() < 0.3:
            records.append({
                "entity_name": entity["entity_name"],
                "cluster_name": entity["cluster_name"],
                "action_type": random.choice(action_types),
                "urgency": "This Week",
                "due_date": (datetime.now() + timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d"),
                "crl_owner": entity["crl_owner"],
            })

        if random.random() < 0.4:
            records.append({
                "entity_name": entity["entity_name"],
                "cluster_name": entity["cluster_name"],
                "action_type": random.choice(action_types),
                "urgency": "Upcoming",
                "due_date": (datetime.now() + timedelta(days=random.randint(8, 30))).strftime("%Y-%m-%d"),
                "crl_owner": entity["crl_owner"],
            })

    return pd.DataFrame(records)


# Legacy compat
def get_client_ontology_data():
    return get_all_entities()

def get_relationship_edges():
    return get_all_relationships()
