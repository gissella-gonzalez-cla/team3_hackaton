"""Mock data constants for the CLA Customer Relationship Hub."""

ENTITIES = [
    {"id": "E1", "name": "Northwind Manufacturing Group", "type": "Parent", "industry": "Manufacturing", "revenue": "$42M", "relationship_lead": "Casey Wilson", "coverage_team": "Assurance pod", "scorecard": 82},
    {"id": "E2", "name": "Northwind Plastics LLC", "type": "Subsidiary", "parent": "E1", "industry": "Manufacturing", "revenue": "$18M", "relationship_lead": "Casey Wilson", "coverage_team": "Assurance pod", "scorecard": 74},
    {"id": "E3", "name": "Northwind Distribution Co", "type": "Subsidiary", "parent": "E1", "industry": "Logistics", "revenue": "$12M", "relationship_lead": "Casey Wilson", "coverage_team": "Tax pod", "scorecard": 61},
    {"id": "E4", "name": "Atlas Advisory Group", "type": "Parent", "industry": "Financial Services", "revenue": "$85M", "relationship_lead": "Jamie Norris", "coverage_team": "Outsourcing pod", "scorecard": 69},
    {"id": "E5", "name": "Atlas Wealth Management", "type": "Subsidiary", "parent": "E4", "industry": "Financial Services", "revenue": "$35M", "relationship_lead": "Jamie Norris", "coverage_team": "Outsourcing pod", "scorecard": 77},
    {"id": "E6", "name": "Atlas Insurance Partners", "type": "Subsidiary", "parent": "E4", "industry": "Insurance", "revenue": "$22M", "relationship_lead": "Jamie Norris", "coverage_team": "Advisory pod", "scorecard": 58},
    {"id": "E7", "name": "Blue Canyon Hospitality", "type": "Parent", "industry": "Hospitality", "revenue": "$67M", "relationship_lead": "Taylor Stone", "coverage_team": "Advisory pod", "scorecard": 86},
    {"id": "E8", "name": "Blue Canyon Resorts", "type": "Subsidiary", "parent": "E7", "industry": "Hospitality", "revenue": "$28M", "relationship_lead": "Taylor Stone", "coverage_team": "Advisory pod", "scorecard": 73},
    {"id": "E9", "name": "Summit Ag Holdings", "type": "Parent", "industry": "Agriculture", "revenue": "$54M", "relationship_lead": "Morgan Lee", "coverage_team": "Assurance pod", "scorecard": 64},
    {"id": "E10", "name": "Red River Water District", "type": "Parent", "industry": "Government", "revenue": "$15M", "relationship_lead": "Taylor Stone", "coverage_team": "Tax pod", "scorecard": 79},
]

CONTACTS = [
    {"id": "C1", "name": "David Chen", "title": "CFO", "entity": "E1", "email": "dchen@northwind.com", "last_contact": "2025-04-20", "strength": "Strong"},
    {"id": "C2", "name": "Sarah Mitchell", "title": "Controller", "entity": "E2", "email": "smitchell@northwind.com", "last_contact": "2025-04-15", "strength": "Moderate"},
    {"id": "C3", "name": "Robert Hayes", "title": "CEO", "entity": "E4", "email": "rhayes@atlas.com", "last_contact": "2025-04-22", "strength": "Strong"},
    {"id": "C4", "name": "Lisa Park", "title": "VP Finance", "entity": "E4", "email": "lpark@atlas.com", "last_contact": "2025-03-10", "strength": "Weak"},
    {"id": "C5", "name": "James Morrison", "title": "Treasurer", "entity": "E10", "email": "jmorrison@redriver.gov", "last_contact": "2025-04-23", "strength": "Strong"},
    {"id": "C6", "name": "Amanda Foster", "title": "CFO", "entity": "E7", "email": "afoster@bluecanyon.com", "last_contact": "2025-04-18", "strength": "Moderate"},
    {"id": "C7", "name": "Mark Sullivan", "title": "CEO", "entity": "E9", "email": "msullivan@summitagholdings.com", "last_contact": "2025-04-26", "strength": "Strong"},
    {"id": "C8", "name": "Karen Wright", "title": "COO", "entity": "E5", "email": "kwright@atlaswm.com", "last_contact": "2025-02-28", "strength": "Weak"},
    {"id": "C9", "name": "Tom Bradley", "title": "Director of Ops", "entity": "E3", "email": "tbradley@northwinddist.com", "last_contact": "2025-01-15", "strength": "Cold"},
    {"id": "C10", "name": "Nina Patel", "title": "VP Strategy", "entity": "E6", "email": "npatel@atlasins.com", "last_contact": "2025-04-01", "strength": "Moderate"},
]

PROJECTS = [
    {"id": "P1", "entity": "E1", "name": "FY26 Audit", "service": "Assurance", "type": "Audit", "phase": "Fieldwork", "status": "On Track", "value": "$180K", "due_date": "2026-06-30"},
    {"id": "P2", "entity": "E1", "name": "Q2 Review", "service": "Assurance", "type": "Review", "phase": "Interim", "status": "Needs Review", "value": "$65K", "due_date": "2026-05-15"},
    {"id": "P3", "entity": "E4", "name": "CAAS Recurring", "service": "CAAS", "type": "Recurring", "phase": "Apr", "status": "AR Hold", "value": "$240K", "due_date": "2026-05-01"},
    {"id": "P4", "entity": "E7", "name": "Tax Compliance FY25", "service": "Tax", "type": "Compliance", "phase": "Planning", "status": "On Track", "value": "$95K", "due_date": "2026-04-30"},
    {"id": "P5", "entity": "E9", "name": "Advisory - M&A Due Diligence", "service": "Advisory", "type": "Transaction", "phase": "Fieldwork", "status": "Hot", "value": "$320K", "due_date": "2026-05-10"},
    {"id": "P6", "entity": "E10", "name": "Payroll Services", "service": "CAAS", "type": "Recurring", "phase": "Monthly", "status": "On Track", "value": "$48K", "due_date": "2026-05-31"},
    {"id": "P7", "entity": "E2", "name": "Cost Segregation Study", "service": "Tax", "type": "Advisory", "phase": "Reporting", "status": "On Track", "value": "$72K", "due_date": "2026-06-15"},
    {"id": "P8", "entity": "E5", "name": "SOC 2 Type II", "service": "Assurance", "type": "Attestation", "phase": "Planning", "status": "Waiting on Client", "value": "$135K", "due_date": "2026-05-20"},
]

CONTRACTS = [
    {"id": "CT1", "entity": "E1", "type": "Master Service Agreement", "start": "2023-01-01", "end": "2026-12-31", "value": "$1.2M", "status": "Active"},
    {"id": "CT2", "entity": "E4", "type": "Master Service Agreement", "start": "2022-06-01", "end": "2025-05-31", "value": "$2.1M", "status": "Renewal Due"},
    {"id": "CT3", "entity": "E7", "type": "Engagement Letter", "start": "2025-01-01", "end": "2025-12-31", "value": "$95K", "status": "Active"},
    {"id": "CT4", "entity": "E9", "type": "Statement of Work", "start": "2025-03-01", "end": "2025-08-31", "value": "$320K", "status": "Active"},
    {"id": "CT5", "entity": "E10", "type": "Recurring Services Agreement", "start": "2024-07-01", "end": "2027-06-30", "value": "$144K", "status": "Active"},
    {"id": "CT6", "entity": "E5", "type": "Engagement Letter", "start": "2025-02-01", "end": "2025-09-30", "value": "$135K", "status": "Active"},
]

OPPORTUNITIES = [
    {"id": "O1", "entity": "E1", "title": "Tax Advisory - R&D Credits", "description": "Northwind Manufacturing has significant R&D spend but no current R&D credit engagement. Subsidiary Northwind Plastics also qualifies.", "gap_type": "Service Gap", "potential_revenue": "$85K", "confidence": "High", "contact_gap": "No tax contact at Plastics LLC", "priority": "Hot"},
    {"id": "O2", "entity": "E4", "title": "Wealth Management Audit", "description": "Atlas Wealth Management (subsidiary) has grown 40% YoY but has no assurance engagement. SOC report would be valuable for their clients.", "gap_type": "Entity Gap", "potential_revenue": "$150K", "confidence": "High", "contact_gap": "Weak relationship with COO Karen Wright", "priority": "Hot"},
    {"id": "O3", "entity": "E7", "title": "Hospitality Advisory - Tech Implementation", "description": "Blue Canyon is implementing new PMS system across properties. No advisory engagement for system selection or implementation support.", "gap_type": "Service Gap", "potential_revenue": "$200K", "confidence": "Medium", "contact_gap": "No IT leadership contact", "priority": "Warm"},
    {"id": "O4", "entity": "E9", "title": "Succession Planning", "description": "Summit Ag Holdings CEO Mark Sullivan mentioned retirement timeline. No wealth or succession advisory engagement in place.", "gap_type": "Relationship Gap", "potential_revenue": "$175K", "confidence": "Medium", "contact_gap": "No contact with family members/heirs", "priority": "Warm"},
    {"id": "O5", "entity": "E3", "title": "Northwind Distribution - Full Service", "description": "Distribution subsidiary has minimal engagement. Cold contact with Director of Ops. Parent relationship should enable cross-sell.", "gap_type": "Entity Gap", "potential_revenue": "$120K", "confidence": "Low", "contact_gap": "Contact Tom Bradley is Cold - last touch Jan 2025", "priority": "Watch"},
    {"id": "O6", "entity": "E6", "title": "Atlas Insurance - Regulatory Compliance", "description": "New state regulations require enhanced compliance reporting. Atlas Insurance has no current compliance engagement.", "gap_type": "Service Gap", "potential_revenue": "$95K", "confidence": "Medium", "contact_gap": "Moderate relationship with VP Strategy", "priority": "Warm"},
]

DISCOVERY_PLAYBOOK = [
    {
        "title": "Open The Relationship",
        "prompt": "Confirm what changed in the client's business since the last meaningful conversation.",
        "talk_track": [
            "What has changed in the business, leadership team, or ownership structure since our last review?",
            "What decisions are taking the most executive attention this quarter?",
            "Where is the leadership team feeling friction or uncertainty right now?",
        ],
    },
    {
        "title": "Pressure-Test Operations",
        "prompt": "Probe for service gaps, timing risks, and teams that may be under-supported.",
        "talk_track": [
            "Which reporting, close, compliance, or audit cycles feel most fragile right now?",
            "What work is currently being done internally that should probably be standardized or outsourced?",
            "Where are there deadlines, filings, or board expectations that could slip without help?",
        ],
    },
    {
        "title": "Expand The Relationship",
        "prompt": "Surface adjacent entities, stakeholders, and future-state work before the meeting ends.",
        "talk_track": [
            "Which affiliates, subsidiaries, or departments are not getting the same level of support?",
            "Who else should be in the next conversation to accelerate decisions?",
            "If we were meeting again in 90 days, what outcome would make this conversation successful?",
        ],
    },
]

MEETING_AUTOMATION_STEPS = [
    "Create the Teams meeting from this page using the prepared agenda link.",
    "Enable cloud recording and transcription before the conversation starts.",
    "Use the manual capture panel as a mobile fallback when Teams automation is unavailable.",
    "End with a next-step summary and translate transcript notes into follow-up actions.",
]

MOBILE_CAPTURE_TIPS = [
    "Use large primary actions so the page stays usable on a phone during live conversations.",
    "Capture timestamps after topic changes so follow-up notes are easier to find.",
    "Keep manual notes short during the call and expand them into a transcript summary immediately after.",
]

ROADMAP_STAGES = [
    "Discovery",
    "Operating Rhythm",
    "Delivery Risks",
    "Growth Plays",
    "Renewal",
    "Relationship Risk",
]


DISCOVERY_PLAYBOOK = [
    {
        "title": "Open The Relationship",
        "prompt": "Confirm what changed in the client's business since the last meaningful conversation.",
        "talk_track": [
            "What has changed in the business, leadership team, or ownership structure since our last review?",
            "What decisions are taking the most executive attention this quarter?",
            "Where is the leadership team feeling friction or uncertainty right now?",
        ],
    },
    {
        "title": "Pressure-Test Operations",
        "prompt": "Probe for service gaps, timing risks, and teams that may be under-supported.",
        "talk_track": [
            "Which reporting, close, compliance, or audit cycles feel most fragile right now?",
            "What work is currently being done internally that should probably be standardized or outsourced?",
            "Where are there deadlines, filings, or board expectations that could slip without help?",
        ],
    },
    {
        "title": "Expand The Relationship",
        "prompt": "Surface adjacent entities, stakeholders, and future-state work before the meeting ends.",
        "talk_track": [
            "Which affiliates, subsidiaries, or departments are not getting the same level of support?",
            "Who else should be in the next conversation to accelerate decisions?",
            "If we were meeting again in 90 days, what outcome would make this conversation successful?",
        ],
    },
]

MEETING_AUTOMATION_STEPS = [
    "Create the Teams meeting from this page using the prepared agenda link.",
    "Enable cloud recording and transcription before the conversation starts.",
    "Use the manual capture panel as a mobile fallback when Teams automation is unavailable.",
    "End with a next-step summary and translate transcript notes into follow-up actions.",
]

MOBILE_CAPTURE_TIPS = [
    "Use large primary actions so the page stays usable on a phone during live conversations.",
    "Capture timestamps after topic changes so follow-up notes are easier to find.",
    "Keep manual notes short during the call and expand them into a transcript summary immediately after.",
]

ROADMAP_STAGES = [
    "Discovery",
    "Operating Rhythm",
    "Delivery Risks",
    "Growth Plays",
    "Renewal",
    "Relationship Risk",
]
