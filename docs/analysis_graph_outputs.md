# Team 3 Hackathon: Analysis Outputs in Graphs

This document visualizes the latest outputs from:

- `uv run src/entity_view_analysis.py`
- `uv run src/relationship_view_analysis.py`
- `uv run src/engagement_view_analysis.py`

Data snapshot source: console output shared on May 13, 2026.

## 1) Entity View

### Client Status Distribution

```mermaid
pie title Client Status Distribution (n=82)
    "Active" : 74
    "Prospect" : 4
    "Inactive" : 4
```

### Industry Distribution (Level 2)

```mermaid
pie title Industry Distribution L2 (n=82)
    "Industrials" : 21
    "Financial Services and Real Estate" : 16
    "Other Industries" : 13
    "Service Industries" : 12
    "Health Care" : 10
    "Public Sector" : 10
```

### Top Industry Distribution (Level 3)

```mermaid
pie title Top Industry Distribution L3 (Top 10)
    "Manufacturing" : 14
    "Health Care and Life Sciences" : 10
    "Agribusiness, Food and Beverage" : 8
    "Real Estate" : 8
    "Financial Services" : 6
    "Federal Government" : 6
    "Nonprofit" : 5
    "Logistics" : 4
    "State & Local Government" : 4
    "Construction" : 3
```

### Geography Distribution (Country)

```mermaid
pie title Country Distribution
    "USA" : 82
```

### Top States (Top 10)

```mermaid
pie title State Distribution (Top 10)
    "TN" : 5
    "MA" : 4
    "AL" : 3
    "KS" : 3
    "CO" : 3
    "MO" : 3
    "ME" : 3
    "WI" : 3
    "NV" : 3
    "WV" : 3
```

## 2) Relationship View

### Relationship Type Distribution

```mermaid
pie title Relationship Type Distribution (n=41)
    "PARENT_CHILD" : 18
    "AFFILIATE" : 12
    "OWNERSHIP" : 9
    "SHARED_LEADERSHIP" : 1
    "SUCCESSOR" : 1
```

### Parent Entities by Number of Children (Top)

```mermaid
pie title Parent Entities By Number Of Children
    "North Ridge Health Group (C100377)" : 4
    "Pinnacle Financial Holdings Inc (C108091)" : 3
    "Cornerstone Manufacturing Group (C108873)" : 3
    "Bayview Real Estate Holdings (C110236)" : 3
    "Greenfield Agribusiness Group (C111745)" : 3
    "Beacon Construction Group (C102970)" : 2
```

### Owners by Number of Ownership Links

```mermaid
pie title Owners By Number Of Ownership Links
    "Cascade Equity Partners (C101295)" : 5
    "City of Pinewood (C103948)" : 1
    "Sunshine Charitable Foundation (C105640)" : 1
    "Magnolia Energy Holdings LLC (C107488)" : 1
    "Peachtree Industrial Partners (C107646)" : 1
```

### Example Relationship Network (First 10 Rows)

```mermaid
graph LR
    C100377[North Ridge Health Group] -->|PARENT_CHILD| C100804[North Ridge Dental Holdings LLC]
    C100377 -->|PARENT_CHILD| C100869[North Ridge Dental - Iowa]
    C100377 -->|PARENT_CHILD| C101020[North Ridge Dental - Wisconsin]
    C100377 -->|PARENT_CHILD| C101212[North Ridge Specialty Surgery LLC]
    C100804 -->|AFFILIATE| C100869
    C100804 -->|AFFILIATE| C101020
    C100869 -->|AFFILIATE| C101020
    C101295[Cascade Equity Partners] -->|OWNERSHIP| C101579[Cascade-backed Lakeside Manufacturing]
    C101295 -->|OWNERSHIP| C101820[Cascade-backed Apex Logistics LLC]
    C101295 -->|OWNERSHIP| C102316[Cascade-backed BrightLeaf Foods]
```

## 3) Engagement View

### Service Line L2 Usage

```mermaid
pie title Service Line L2 Usage (n=142 projects)
    "Assurance" : 56
    "Tax" : 45
    "Outsourcing" : 21
    "Digital" : 20
```

### Top Service Line L3 Usage (Top 10)

```mermaid
pie title Service Line L3 Usage (Top 10)
    "Audit" : 34
    "Business Tax" : 17
    "Federal Tax Strategies" : 12
    "Digital - Cybersecurity" : 11
    "CAAS" : 9
    "Talent Solutions" : 7
    "Review" : 6
    "Digital - Data and Automation" : 6
    "Assurance Related Consulting" : 6
    "Transaction Tax" : 6
```

### Project Status Distribution

```mermaid
pie title Project Status Distribution
    "Active" : 81
    "Completed" : 61
```

### Billable Distribution

```mermaid
pie title Billable Distribution
    "true" : 135
    "false" : 7
```

### Top Project Types (Top 10)

```mermaid
pie title Top Project Types
    "AS 001 Audit Excl SEC, GAS, EBP, FDICIA" : 22
    "TX 131 1065 Compliance" : 11
    "TX 129 1120 Compliance" : 9
    "AS 009 Review (Other than SEC)" : 7
    "OS 234 Enhanced Managed Services" : 7
    "AS 003 Audit Performed under GAS (excl A-133 and Hud)" : 7
    "OS 271 Internal Audit" : 6
    "AS 004 Single Audit" : 6
    "TX 130 1120S Compliance" : 6
    "TX 117 990 Compliance - Tax Exempts" : 6
```

## Notes

- Values above are sourced from command output and represent the shared snapshot.
- Re-run scripts and update this file when data changes.