# team3_hackaton — CLA One Firm View

Central repo for Team 3 hackathon work (May 2026).

## Application — One Firm View

A Databricks App (Streamlit) providing two core functions:

1. **Centralized Reporting** — Firmwide client family visualization, aggregated views of health, risk, and opportunity stratified by geography, service line, and industry.
2. **Structured Data Collection** — CRL check-in workflow with front-end guardrails for consistent, high-quality data capture during every client interaction.

### Running the App

```bash
cd app
streamlit run app.py
```

### Pages

| Page | Purpose |
|------|---------|
| **Home (app.py)** | CRL profile sidebar with Quick Pulse metrics; key definitions |
| **Client Family Explorer** | Firmwide client family graph, family overview, health monitor, seamless analysis |
| **Opportunity Manager** | New leads (unserved entities), service gaps, entity drill-down, check-in form, history |

### Key Concepts

- **Client Family**: The web of complex relationships between client entities (partnerships, individuals, trusts, corps).
- **Health**: Based on AR recency + client tenure. Long-term clients earn grace; multi-service clients have additional resilience.
- **Seamless**: Bundled services increasing retention through higher barriers to exit.
- **Opportunity**: Unserved entities (red nodes) or service gaps on served entities.

## Participants

- Behera, Mamatamayi
- Brady, Heidi
- Carey, Jason
- Cunningham, Brian
- Gonzalez, Gissella
- Hoff, Kim
- Kreiner, Cody

## Data Files

- `data/client.csv`: client master data (identity, industry, geography, parent fields)
- `data/relationship.csv`: links between clients (parent-child, ownership, affiliate, etc.)
- `data/projects.csv`: project and service engagement data
- `data/pick_lists.csv`: pick-list reference values

## Analysis Scripts

All scripts are in `src/` and can be run with `uv`.

Graph-based output report:
- `docs/analysis_graph_outputs.md`
- `docs/analysis_graph_outputs.html` (browser-rendered graphs)
- `docs/model_goal_readme.md` (model explanation and goal alignment)

Leadership-ready summary output:
- `outputs/leader_brief.md`

Action plan assets:
- `outputs/action_plans/cross_entity_portfolio_review.md`
- `outputs/action_plans/shared_pursuit_list_template.csv`
- `outputs/action_plans/pinnacle_financial_cross_entity_review.md`
- `outputs/action_plans/pinnacle_financial_shared_pursuit_list.csv`
- `outputs/action_plans/top10_ml_cross_sell_pursuits.csv`

### 1) Entity View

Script: `src/entity_view_analysis.py`

Questions answered:
- Who is the client?
- What is their industry profile?
- What is their geography profile?

Run:

```bash
uv run src/entity_view_analysis.py
```

Examples:

```bash
# Exact client by ID
uv run src/entity_view_analysis.py --client-id C100377

# Partial name match
uv run src/entity_view_analysis.py --client-name "North Ridge"

# Show more rows in distributions
uv run src/entity_view_analysis.py --top-n 20
```

### 2) Relationship View

Script: `src/relationship_view_analysis.py`

Questions answered:
- Parent / child relationships
- Shared ownership relationships
- Connections between clients

Run:

```bash
uv run src/relationship_view_analysis.py
```

Examples:

```bash
# Focus on one client's relationship edges
uv run src/relationship_view_analysis.py --client-id C100377

# Focus on one relationship type
uv run src/relationship_view_analysis.py --relationship-type OWNERSHIP

# Show larger output sections
uv run src/relationship_view_analysis.py --top-n 20
```

### 3) Engagement View

Script: `src/engagement_view_analysis.py`

Questions answered:
- What services are they using?
- What projects exist?

Run:

```bash
uv run src/engagement_view_analysis.py
```

Examples:

```bash
# One client
uv run src/engagement_view_analysis.py --client-id C100377

# Client name match
uv run src/engagement_view_analysis.py --client-name "North Ridge"

# Only active projects
uv run src/engagement_view_analysis.py --project-status Active

# Show more rows
uv run src/engagement_view_analysis.py --top-n 20
```

### 4) Phase 2 ML: Cross-Sell Propensity

Script: `src/cross_sell_propensity_model.py`

Goal:
- Train a simple baseline model to prioritize clients for cross-sell outreach.

Run:

```bash
uv run src/cross_sell_propensity_model.py --top-n 20
```

Optional:

```bash
# Also control how many rows are generated in the action tracker file
uv run src/cross_sell_propensity_model.py --top-n 20 --pursuit-top-n 10
```

Outputs:

```text
outputs/ml_cross_sell_metrics.json
outputs/ml_cross_sell_ranked_candidates.csv
outputs/ml_cross_sell_summary.md
outputs/action_plans/top10_ml_cross_sell_pursuits.csv
```

### 5) Weekly Model Lift Scorecard

Script: `src/weekly_model_lift_scorecard.py`

Goal:
- Quantify model lift (Top-N vs Rest) and weekly execution quality.

Run:

```bash
uv run src/weekly_model_lift_scorecard.py --top-n 10
```

Outputs:

```text
outputs/weekly_model_lift_scorecard.json
outputs/weekly_model_lift_scorecard.md
```

## Quick Start

From repo root:

```bash
cd /workspaces/team3_hackaton
uv run src/entity_view_analysis.py
```

If `uv` is not installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
