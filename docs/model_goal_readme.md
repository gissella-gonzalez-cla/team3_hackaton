# Model README: Cross-Sell Propensity and Goal Alignment

## Why This Model Exists

This model supports the hackathon goal:

Demonstrate a shared, trusted view of client relationships so leaders can make faster decisions on growth, coordination, and risk.

The model is not replacing leadership judgment. It is a prioritization layer that turns shared relationship and engagement data into an ordered action queue.

## Business Problem It Addresses

Current pain:
- Relationship context is fragmented.
- Parent/child and ownership context is inconsistently used.
- Growth and risk decisions rely on manual stitching.

Model contribution:
- Rank accounts by cross-sell propensity using one repeatable method.
- Feed a shared pursuit tracker used in weekly cross-entity reviews.
- Provide measurable lift indicators (Top N vs Rest) for leadership confidence.

## What the Model Does

Script:
- src/cross_sell_propensity_model.py

Model type:
- Mixed Naive Bayes baseline (numeric + categorical features).

Training target (proxy):
- 1 if a client currently has 2 or more service lines.
- 0 otherwise.

Primary outputs:
- outputs/ml_cross_sell_metrics.json
- outputs/ml_cross_sell_ranked_candidates.csv
- outputs/ml_cross_sell_summary.md
- outputs/action_plans/top10_ml_cross_sell_pursuits.csv

## How It Relates to Your Goal

### 1) Faster growth decisions
- The model ranks cross-sell candidates and removes manual triage.
- Teams focus on highest-priority accounts first.

### 2) Better coordination
- Ranked candidates flow into one shared pursuit tracker.
- Relationship lead, next action owner, and due dates are centralized.

### 3) Earlier risk visibility
- Candidates with low confidence or weak activity are flagged with higher risk.
- Leaders can decide where to validate relationships before pursuing.

### 4) Credible path to scale
- Same process can run weekly and across more accounts.
- Scorecard shows whether model-prioritized accounts outperform the rest.

## Weekly Operating Workflow

1. Refresh model outputs:
- uv run src/cross_sell_propensity_model.py --top-n 20 --pursuit-top-n 10

2. Generate weekly lift scorecard:
- uv run src/weekly_model_lift_scorecard.py --top-n 10

3. Review action tracker:
- outputs/action_plans/top10_ml_cross_sell_pursuits.csv

4. Run leadership review cadence with the cross-entity playbook:
- outputs/action_plans/cross_entity_portfolio_review.md

## What Leaders Should Look At

### Decision quality
- outputs/ml_cross_sell_metrics.json
- Accuracy, precision, recall, F1

### Priority queue
- outputs/ml_cross_sell_ranked_candidates.csv
- Top candidates by propensity score

### Execution readiness
- outputs/action_plans/top10_ml_cross_sell_pursuits.csv
- Owner, stage, due date, blocker, next action

### Business impact trend
- outputs/weekly_model_lift_scorecard.md
- Lift of Top N vs Rest and weekly execution metrics

## Guardrails and Limitations

- This is a Phase 2 baseline model using a proxy target.
- It should be used as decision support, not autopilot.
- Synthetic/demo data means business lift should be validated with real outcomes over time.
- Keep a human review step for compliance, COI, and strategic fit.

## Success Criteria for This Phase

- Top N candidates reviewed weekly by a relationship lead.
- Shared pursuit tracker maintained with owners and due dates.
- Weekly model-lift scorecard published to leadership.
- Evidence that Top N has stronger actionable profile than the rest.

## Next Phase (After Baseline)

- Replace proxy target with real win/loss outcomes.
- Add time-based features and account history.
- Introduce calibrated thresholds by industry segment.
- Track realized pipeline/win lift from model-driven prioritization.
