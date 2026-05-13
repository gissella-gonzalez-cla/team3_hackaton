"""
Sample Data Generator — Entity-Level Ontology Model
=====================================================
Models realistic professional services client relationships:
- Partnership entities (1065s) with partners and dependents
- Corporations (1120s), trusts, individuals
- Service engagements per entity (assurance, tax, bizops, digital)
- Billing/AR data with 30/60/90-day health model
- Relationship edges (partner-of, dependent-of, working-partnership, ownership)

Key Concepts:
- ONTOLOGY: The web of complex relationships between client entities
- HEALTH: Based on 90-day AR policy (healthy < 30d, strained 60d, poor 90d+)
- OPPORTUNITY: Unserved entities (red nodes) OR service gaps on served entities
- SEAMLESS: Bundled services (assurance + tax, etc.) that increase retention
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

# Real CLA geography hierarchy: Region > Sub-Region > Office
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

# Flat list of all offices for data generation
GEOGRAPHIES = [
    "Minneapolis", "Northern Wisconsin", "Southern Wisconsin", "Central Wisconsin",
    "Central Illinois", "Greater Missouri", "Western Ohio", "Greater Indiana",
    "Northern Illinois", "Southern California", "Northern California",
    "Pacific Northwest", "Greater Southwest", "Rocky Mountains",
    "Northern Texas", "Central Texas", "Southwest Florida", "Greater Tampa Bay",
    "Orlando", "Greater Carolinas", "Atlanta", "Greater New York",
    "Southern New England", "Baltimore/Washington", "Greater Philadelphia",
]

# Real CLA industry hierarchy: Level 2 > Level 3 > Level 4
INDUSTRY_HIERARCHY = {
    "Financial Services": ["Banks", "Specialty Finance", "Insurance", "Credit Unions"],
    "Real Estate": ["Lessors & Operators", "Developers & Subdividers", "Investor", "Other Real Estate"],
    "Private Equity": ["Private Equity - Industry Segment"],
}

# Flat list for backward compat
INDUSTRIES = [
    "Banks", "Specialty Finance", "Insurance", "Credit Unions",
    "Lessors & Operators", "Developers & Subdividers", "Investor",
    "Other Real Estate", "Private Equity - Industry Segment",
]

# Real CRL names from CLA data
CRL_NAMES = [
    "Rypina, Katarzyna", "Juergensen, Joshua", "Carlson, Erica",
    "Mattson, Brad", "Wieland, Sylvia", "Sabo, Susan",
    "Meyer, Nicholas", "Holthaus, Corey", "McMillon, Jerry",
    "Powers, Harrison", "Estep, Dee", "Vance, Mark",
    "Solley, Caleb", "Leiter, Karen", "Strate, Brittany",
    "Carey, Edward", "Shelton, Kate", "Lounsbery, Tyler",
]

# =============================================================================
# ENTITY ONTOLOGY — Realistic Partnership Structures
# =============================================================================

ENTITY_CLUSTERS = [
    # --- Cluster 1: Real Estate Development Partnership (Midwest) ---
    {
        "cluster_name": "Thomson of Wisconsin Inc",
        "entities": [
            {"id": "E001", "name": "Thomson Management Inc", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_mm": 45.2},
            {"id": "E002", "name": "Thomas Smits", "type": "Individual", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_mm": 2.1},
            {"id": "E003", "name": "Sandra Vance", "type": "Individual", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_mm": 1.8},
            {"id": "E004", "name": "Marcus Webb", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Northern Illinois", "revenue_mm": 1.5},
            {"id": "E005", "name": "Diane Kowalski", "type": "Individual", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_mm": 0.9},
            {"id": "E006", "name": "Smits Family Trust", "type": "1041 Trust", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_mm": 3.2},
            {"id": "E007", "name": "Webb Construction LLC", "type": "1120S S-Corp", "industry": "Developers & Subdividers", "geography": "Northern Illinois", "revenue_mm": 12.8},
            {"id": "E008", "name": "Thomson Property Mgmt LLC", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_mm": 8.5},
            {"id": "E009", "name": "Alex Webb (Dependent)", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Northern Illinois", "revenue_mm": 0.0},
            {"id": "E010", "name": "Vance Holdings LP", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Southern Wisconsin", "revenue_mm": 22.0},
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
        ],
        "engagements": {
            "E001": ["Assurance", "Tax"],
            "E002": ["Tax"],
            "E003": ["Tax"],
            "E008": ["Tax", "Business Operations"],
            "E010": ["Assurance"],
        }
    },
    # --- Cluster 2: Financial Services Group (Central) ---
    {
        "cluster_name": "Community Illinois Corporation",
        "entities": [
            {"id": "E011", "name": "CIC Capital Trust I", "type": "1065 Partnership", "industry": "Banks", "geography": "Central Illinois", "revenue_mm": 78.5},
            {"id": "E012", "name": "Robert Scanlan", "type": "Individual", "industry": "Banks", "geography": "Central Illinois", "revenue_mm": 3.5},
            {"id": "E013", "name": "Patricia Alvarez", "type": "Individual", "industry": "Banks", "geography": "Central Illinois", "revenue_mm": 2.8},
            {"id": "E014", "name": "Merchants and Manufacturers Bank", "type": "1120 Corporation", "industry": "Banks", "geography": "Central Illinois", "revenue_mm": 34.0},
            {"id": "E015", "name": "Busey Financial Corp", "type": "1120S S-Corp", "industry": "Banks", "geography": "Greater Missouri", "revenue_mm": 18.2},
            {"id": "E016", "name": "Scanlan Family Foundation", "type": "1041 Trust", "industry": "Banks", "geography": "Central Illinois", "revenue_mm": 5.0},
            {"id": "E017", "name": "David Scanlan (Dependent)", "type": "Individual", "industry": "Banks", "geography": "Central Illinois", "revenue_mm": 0.0},
            {"id": "E018", "name": "Deere Credit Services Inc", "type": "1120 Corporation", "industry": "Specialty Finance", "geography": "Greater Iowa", "revenue_mm": 15.6},
            {"id": "E019", "name": "Farmers State Bank & Trust", "type": "1065 Partnership", "industry": "Banks", "geography": "Central Illinois", "revenue_mm": 9.3},
        ],
        "relationships": [
            {"source": "E011", "target": "E012", "type": "partner_of", "ownership_pct": 60},
            {"source": "E011", "target": "E013", "type": "partner_of", "ownership_pct": 40},
            {"source": "E011", "target": "E014", "type": "owner_of", "ownership_pct": 100},
            {"source": "E011", "target": "E015", "type": "owner_of", "ownership_pct": 100},
            {"source": "E012", "target": "E016", "type": "owner_of", "ownership_pct": 100},
            {"source": "E012", "target": "E017", "type": "dependent_of"},
            {"source": "E013", "target": "E018", "type": "owner_of", "ownership_pct": 100},
            {"source": "E011", "target": "E019", "type": "working_partnership"},
        ],
        "engagements": {
            "E011": ["Assurance", "Tax", "Business Operations"],
            "E012": ["Tax"],
            "E014": ["Assurance", "Tax"],
            "E015": ["Tax"],
            "E016": ["Tax"],
            "E019": ["Assurance"],
        }
    },
    # --- Cluster 3: Real Estate Investment (Florida) ---
    {
        "cluster_name": "Miromar Development Corporation",
        "entities": [
            {"id": "E020", "name": "Miromar Development Corporation", "type": "1065 Partnership", "industry": "Developers & Subdividers", "geography": "Greater Tampa Bay", "revenue_mm": 55.0},
            {"id": "E021", "name": "Leonard Pratt", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Greater Tampa Bay", "revenue_mm": 1.2},
            {"id": "E022", "name": "James Pomeroy", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Southwest Florida", "revenue_mm": 1.4},
            {"id": "E023", "name": "Amy Costa", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Orlando", "revenue_mm": 1.1},
            {"id": "E024", "name": "Costa Maggiore II HOA Inc", "type": "1120S S-Corp", "industry": "Developers & Subdividers", "geography": "Greater Tampa Bay", "revenue_mm": 28.0},
            {"id": "E025", "name": "Miromar Outlet West LLC", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Greater Tampa Bay", "revenue_mm": 12.5},
            {"id": "E026", "name": "Pratt Family Trust", "type": "1041 Trust", "industry": "Developers & Subdividers", "geography": "Greater Tampa Bay", "revenue_mm": 4.0},
            {"id": "E027", "name": "Pomeroy Commercial Properties LP", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Southwest Florida", "revenue_mm": 8.7},
            {"id": "E028", "name": "Liam Pratt (Dependent)", "type": "Individual", "industry": "Developers & Subdividers", "geography": "Greater Tampa Bay", "revenue_mm": 0.0},
            {"id": "E029", "name": "Costa Development Corp", "type": "1120S S-Corp", "industry": "Developers & Subdividers", "geography": "Orlando", "revenue_mm": 6.3},
        ],
        "relationships": [
            {"source": "E020", "target": "E021", "type": "partner_of", "ownership_pct": 40},
            {"source": "E020", "target": "E022", "type": "partner_of", "ownership_pct": 35},
            {"source": "E020", "target": "E023", "type": "partner_of", "ownership_pct": 25},
            {"source": "E020", "target": "E024", "type": "owner_of", "ownership_pct": 100},
            {"source": "E020", "target": "E025", "type": "owner_of", "ownership_pct": 100},
            {"source": "E021", "target": "E026", "type": "owner_of", "ownership_pct": 100},
            {"source": "E022", "target": "E027", "type": "partner_of", "ownership_pct": 50},
            {"source": "E021", "target": "E028", "type": "dependent_of"},
            {"source": "E023", "target": "E029", "type": "owner_of", "ownership_pct": 100},
        ],
        "engagements": {
            "E020": ["Assurance", "Tax", "Digital"],
            "E021": ["Tax"],
            "E024": ["Assurance", "Tax", "Business Operations"],
            "E025": ["Tax"],
            "E026": ["Tax"],
        }
    },
    # --- Cluster 4: Private Equity (West) ---
    {
        "cluster_name": "Pacific Assets Investment Corp",
        "entities": [
            {"id": "E030", "name": "Pacific Assets Investment Corporation", "type": "1065 Partnership", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_mm": 92.0},
            {"id": "E031", "name": "Hae-Jeong Kim", "type": "Individual", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_mm": 4.2},
            {"id": "E032", "name": "Samantha Reeves", "type": "Individual", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_mm": 3.1},
            {"id": "E033", "name": "Meridian General Inc", "type": "1120 Corporation", "industry": "Lessors & Operators", "geography": "Southern California", "revenue_mm": 45.0},
            {"id": "E034", "name": "Arlington Housing Corporation", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Southern California", "revenue_mm": 18.5},
            {"id": "E035", "name": "Kim Family Office LP", "type": "1065 Partnership", "industry": "Specialty Finance", "geography": "Southern California", "revenue_mm": 12.0},
            {"id": "E036", "name": "Reeves Capital Trust", "type": "1041 Trust", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_mm": 7.5},
            {"id": "E037", "name": "Ethan Kim (Dependent)", "type": "Individual", "industry": "Private Equity - Industry Segment", "geography": "Southern California", "revenue_mm": 0.0},
            {"id": "E038", "name": "Catalina Island Camps Inc", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Southern California", "revenue_mm": 22.0},
        ],
        "relationships": [
            {"source": "E030", "target": "E031", "type": "partner_of", "ownership_pct": 55},
            {"source": "E030", "target": "E032", "type": "partner_of", "ownership_pct": 45},
            {"source": "E030", "target": "E033", "type": "owner_of", "ownership_pct": 100},
            {"source": "E030", "target": "E034", "type": "owner_of", "ownership_pct": 100},
            {"source": "E031", "target": "E035", "type": "owner_of", "ownership_pct": 100},
            {"source": "E032", "target": "E036", "type": "owner_of", "ownership_pct": 100},
            {"source": "E031", "target": "E037", "type": "dependent_of"},
            {"source": "E030", "target": "E038", "type": "working_partnership"},
        ],
        "engagements": {
            "E030": ["Assurance", "Tax", "Digital"],
            "E031": ["Tax"],
            "E033": ["Assurance", "Tax", "Business Operations", "Digital"],
            "E035": ["Tax"],
        }
    },
    # --- Cluster 5: Insurance & Finance (Northeast) ---
    {
        "cluster_name": "Intrum Corporation",
        "entities": [
            {"id": "E039", "name": "Intrum Corp", "type": "1065 Partnership", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_mm": 120.0},
            {"id": "E040", "name": "William Graves", "type": "Individual", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_mm": 5.5},
            {"id": "E041", "name": "Margaret Enverso", "type": "Individual", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_mm": 4.2},
            {"id": "E042", "name": "Jonathan Fields", "type": "Individual", "industry": "Insurance", "geography": "Connecticut", "revenue_mm": 3.8},
            {"id": "E043", "name": "ComProps Limited Partnership", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Southern New England", "revenue_mm": 35.0},
            {"id": "E044", "name": "Tamid Reinsurance Ltd", "type": "1120 Corporation", "industry": "Insurance", "geography": "Connecticut", "revenue_mm": 28.0},
            {"id": "E045", "name": "Graves Family Trust", "type": "1041 Trust", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_mm": 8.0},
            {"id": "E046", "name": "Messina Commercial Properties LLC", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Southern New England", "revenue_mm": 18.5},
            {"id": "E047", "name": "FXM Management Inc", "type": "1120S S-Corp", "industry": "Lessors & Operators", "geography": "Southern New England", "revenue_mm": 9.2},
            {"id": "E048", "name": "Caroline Graves (Dependent)", "type": "Individual", "industry": "Specialty Finance", "geography": "Southern New England", "revenue_mm": 0.0},
        ],
        "relationships": [
            {"source": "E039", "target": "E040", "type": "partner_of", "ownership_pct": 40},
            {"source": "E039", "target": "E041", "type": "partner_of", "ownership_pct": 35},
            {"source": "E039", "target": "E042", "type": "partner_of", "ownership_pct": 25},
            {"source": "E039", "target": "E043", "type": "owner_of", "ownership_pct": 100},
            {"source": "E039", "target": "E044", "type": "owner_of", "ownership_pct": 100},
            {"source": "E040", "target": "E045", "type": "owner_of", "ownership_pct": 100},
            {"source": "E041", "target": "E046", "type": "owner_of", "ownership_pct": 50},
            {"source": "E042", "target": "E047", "type": "owner_of", "ownership_pct": 100},
            {"source": "E040", "target": "E048", "type": "dependent_of"},
        ],
        "engagements": {
            "E039": ["Assurance", "Tax"],
            "E040": ["Tax"],
            "E043": ["Assurance", "Business Operations"],
            "E044": ["Assurance", "Tax"],
            "E045": ["Tax"],
        }
    },
    # --- Cluster 6: Banking (Upper Midwest) ---
    {
        "cluster_name": "Van Hoof Corporation & Subs",
        "entities": [
            {"id": "E049", "name": "Van Hoof Corporation", "type": "1065 Partnership", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_mm": 38.0},
            {"id": "E050", "name": "Dale Behm", "type": "Individual", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_mm": 2.0},
            {"id": "E051", "name": "Karen Yarrington", "type": "Individual", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_mm": 1.7},
            {"id": "E052", "name": "Fulfillment Specialists Of America", "type": "1120 Corporation", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_mm": 15.0},
            {"id": "E053", "name": "Oostburg State Bank", "type": "1120S S-Corp", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_mm": 8.0},
            {"id": "E054", "name": "Androscoggin Bancshares LP", "type": "1065 Partnership", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_mm": 12.5},
            {"id": "E055", "name": "Yarrington Land Trust", "type": "1041 Trust", "industry": "Banks", "geography": "Central Wisconsin", "revenue_mm": 6.0},
            {"id": "E056", "name": "Tyler Behm (Dependent)", "type": "Individual", "industry": "Banks", "geography": "Northern Wisconsin", "revenue_mm": 0.0},
        ],
        "relationships": [
            {"source": "E049", "target": "E050", "type": "partner_of", "ownership_pct": 50},
            {"source": "E049", "target": "E051", "type": "partner_of", "ownership_pct": 50},
            {"source": "E049", "target": "E052", "type": "owner_of", "ownership_pct": 100},
            {"source": "E049", "target": "E053", "type": "owner_of", "ownership_pct": 100},
            {"source": "E050", "target": "E054", "type": "owner_of", "ownership_pct": 70},
            {"source": "E051", "target": "E055", "type": "owner_of", "ownership_pct": 100},
            {"source": "E050", "target": "E056", "type": "dependent_of"},
            {"source": "E049", "target": "E054", "type": "working_partnership"},
        ],
        "engagements": {
            "E049": ["Assurance", "Tax"],
            "E050": ["Tax"],
            "E052": ["Tax"],
            "E054": ["Tax", "Business Operations"],
        }
    },
    # --- Cluster 7: Real Estate Investment (Texas) ---
    {
        "cluster_name": "Conti Capital",
        "entities": [
            {"id": "E057", "name": "Conti Capital LP", "type": "1065 Partnership", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_mm": 32.0},
            {"id": "E058", "name": "Angela Estep", "type": "Individual", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_mm": 2.5},
            {"id": "E059", "name": "Brian Donnell", "type": "Individual", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_mm": 2.0},
            {"id": "E060", "name": "Conti ROM Corp", "type": "1120 Corporation", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_mm": 14.0},
            {"id": "E061", "name": "BIP Multifamily Fund I LP", "type": "1065 Partnership", "industry": "Investor", "geography": "Northern Texas", "revenue_mm": 7.8},
            {"id": "E062", "name": "Estep Foundation", "type": "1041 Trust", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_mm": 3.5},
            {"id": "E063", "name": "Sofia Estep (Dependent)", "type": "Individual", "industry": "Lessors & Operators", "geography": "Northern Texas", "revenue_mm": 0.0},
        ],
        "relationships": [
            {"source": "E057", "target": "E058", "type": "partner_of", "ownership_pct": 55},
            {"source": "E057", "target": "E059", "type": "partner_of", "ownership_pct": 45},
            {"source": "E057", "target": "E060", "type": "owner_of", "ownership_pct": 100},
            {"source": "E059", "target": "E061", "type": "owner_of", "ownership_pct": 100},
            {"source": "E058", "target": "E062", "type": "owner_of", "ownership_pct": 100},
            {"source": "E058", "target": "E063", "type": "dependent_of"},
        ],
        "engagements": {
            "E057": ["Assurance", "Tax", "Business Operations", "Digital"],
            "E058": ["Tax"],
            "E060": ["Tax", "Business Operations"],
            "E062": ["Tax"],
        }
    },
    # --- Cluster 8: Real Estate (Carolinas/Atlanta) ---
    {
        "cluster_name": "Galosa LLC",
        "entities": [
            {"id": "E064", "name": "Galosa LLC", "type": "1065 Partnership", "industry": "Investor", "geography": "Atlanta", "revenue_mm": 42.0},
            {"id": "E065", "name": "Michael DiNatale", "type": "Individual", "industry": "Investor", "geography": "Greater Carolinas", "revenue_mm": 2.8},
            {"id": "E066", "name": "Lisa Lankford", "type": "Individual", "industry": "Investor", "geography": "Atlanta", "revenue_mm": 2.3},
            {"id": "E067", "name": "KERUPE LLC", "type": "1120 Corporation", "industry": "Investor", "geography": "Central Texas", "revenue_mm": 25.0},
            {"id": "E068", "name": "Williams & Fudge Inc", "type": "1120S S-Corp", "industry": "Banks", "geography": "Greater Carolinas", "revenue_mm": 11.0},
            {"id": "E069", "name": "Yelloledbedder Inc", "type": "1120S S-Corp", "industry": "Other Real Estate", "geography": "Atlanta", "revenue_mm": 6.5},
            {"id": "E070", "name": "Risk Reduction Plus Group Inc", "type": "1065 Partnership", "industry": "Investor", "geography": "Greater Philadelphia", "revenue_mm": 18.0},
        ],
        "relationships": [
            {"source": "E064", "target": "E065", "type": "partner_of", "ownership_pct": 50},
            {"source": "E064", "target": "E066", "type": "partner_of", "ownership_pct": 50},
            {"source": "E064", "target": "E067", "type": "owner_of", "ownership_pct": 100},
            {"source": "E065", "target": "E068", "type": "owner_of", "ownership_pct": 100},
            {"source": "E066", "target": "E069", "type": "owner_of", "ownership_pct": 100},
            {"source": "E064", "target": "E070", "type": "owner_of", "ownership_pct": 60},
        ],
        "engagements": {
            "E064": ["Assurance", "Tax"],
            "E065": ["Tax"],
            "E067": ["Assurance"],
            "E070": ["Tax"],
        }
    },
]


# =============================================================================
# DATA GENERATION FUNCTIONS
# =============================================================================

def get_all_entities() -> pd.DataFrame:
    """
    Get all entities with engagement status and health scoring.
    Health: Healthy (<30d), Strained (30-59d), Poor (60+d) based on 90-day AR.
    """
    records = []

    for cluster in ENTITY_CLUSTERS:
        cluster_name = cluster["cluster_name"]
        engagements = cluster["engagements"]

        for entity in cluster["entities"]:
            eid = entity["id"]
            is_served = eid in engagements
            services_engaged = engagements.get(eid, [])
            services_not_engaged = [s for s in SERVICE_LINES if s not in services_engaged]

            seamless_score = len(services_engaged)
            is_seamless = seamless_score >= 2

            if is_served:
                if random.random() < 0.6:
                    days_since_activity = random.randint(1, 29)
                    health_status = "Healthy"
                elif random.random() < 0.7:
                    days_since_activity = random.randint(30, 59)
                    health_status = "Strained"
                else:
                    days_since_activity = random.randint(60, 120)
                    health_status = "Poor"
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
                "annual_revenue_mm": entity["revenue_mm"],
                "is_served": is_served,
                "services_engaged": services_engaged,
                "services_not_engaged": services_not_engaged,
                "num_services": len(services_engaged),
                "seamless_score": seamless_score,
                "is_seamless": is_seamless,
                "health_status": health_status,
                "days_since_activity": days_since_activity,
                "last_activity_date": last_activity_date,
                "crl_owner": crl,
                "consent_status": consent,
            })

    return pd.DataFrame(records)


def get_all_relationships() -> pd.DataFrame:
    """Get all entity-to-entity relationship edges for the ontology graph."""
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
        base_amount = entity["annual_revenue_mm"] * 1_000_000 / 4

        for service in entity["services_engaged"]:
            svc_share = base_amount / len(entity["services_engaged"])

            for quarter in quarters:
                if random.random() < 0.85:
                    amount = svc_share * random.uniform(0.75, 1.25)
                    if quarter == quarters[-1]:
                        days_outstanding = random.choice([0, 0, 0, 0, 15, 35, 65, 95])
                    else:
                        days_outstanding = 0

                    records.append({
                        "entity_id": entity["entity_id"],
                        "entity_name": entity["entity_name"],
                        "cluster_name": entity["cluster_name"],
                        "period": quarter,
                        "service_line": service,
                        "billed_amount": round(amount, 2),
                        "paid_amount": round(amount if days_outstanding == 0 else 0, 2),
                        "outstanding_amount": round(amount if days_outstanding > 0 else 0, 2),
                        "days_outstanding": days_outstanding,
                    })

    return pd.DataFrame(records)


def get_cluster_summary() -> pd.DataFrame:
    """Summarize each cluster for the One-Firm view."""
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
            "total_revenue_mm": cluster_ents["annual_revenue_mm"].sum(),
            "served_revenue_mm": served["annual_revenue_mm"].sum(),
            "penetration_pct": round(len(served) / len(cluster_ents) * 100, 1),
            "industries": cluster_ents["industry"].nunique(),
            "geographies": cluster_ents["geography"].nunique(),
            "avg_seamless": served["seamless_score"].mean() if len(served) > 0 else 0,
            "healthy_count": len(served[served["health_status"] == "Healthy"]),
            "strained_count": len(served[served["health_status"] == "Strained"]),
            "poor_count": len(served[served["health_status"] == "Poor"]),
        })

    return pd.DataFrame(records)


def get_opportunities() -> pd.DataFrame:
    """
    Two types:
    1. Unserved entities in the ontology (red nodes)
    2. Served entities with service gaps (seamless growth)
    """
    entities_df = get_all_entities()
    opportunities = []

    for _, entity in entities_df.iterrows():
        if not entity["is_served"] and entity["annual_revenue_mm"] > 0:
            opportunities.append({
                "entity_id": entity["entity_id"],
                "entity_name": entity["entity_name"],
                "entity_type": entity["entity_type"],
                "cluster_name": entity["cluster_name"],
                "industry": entity["industry"],
                "geography": entity["geography"],
                "revenue_mm": entity["annual_revenue_mm"],
                "opportunity_type": "New Engagement (Red Node)",
                "available_services": SERVICE_LINES.copy(),
                "num_available_services": len(SERVICE_LINES),
                "seamless_potential": True,
                "priority_score": round(entity["annual_revenue_mm"] * 1.5, 1),
            })
        elif entity["is_served"] and entity["services_not_engaged"]:
            opportunities.append({
                "entity_id": entity["entity_id"],
                "entity_name": entity["entity_name"],
                "entity_type": entity["entity_type"],
                "cluster_name": entity["cluster_name"],
                "industry": entity["industry"],
                "geography": entity["geography"],
                "revenue_mm": entity["annual_revenue_mm"],
                "opportunity_type": "Service Gap (Seamless Growth)",
                "available_services": entity["services_not_engaged"],
                "num_available_services": len(entity["services_not_engaged"]),
                "seamless_potential": len(entity["services_engaged"]) >= 1,
                "priority_score": round(entity["annual_revenue_mm"] * len(entity["services_not_engaged"]) * 0.5, 1),
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


# Legacy compat
def get_client_ontology_data():
    return get_all_entities()

def get_interaction_history():
    entities_df = get_all_entities()
    served = entities_df[entities_df["is_served"]]
    records = []
    interaction_types = ["In-Person Meeting", "Phone Call", "Video Call", "Email Exchange", "Client Event", "Informal (Lunch/Coffee)"]
    health_signals = ["Healthy — no concerns", "Mentioned competing firms", "Payment delay mentioned", "Very engaged", "Key contact leaving", "Expressed fee concerns"]

    for month_offset in range(12):
        month_date = datetime.now() - timedelta(days=30 * month_offset)
        for _ in range(random.randint(15, 35)):
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

def get_relationship_edges():
    return get_all_relationships()
