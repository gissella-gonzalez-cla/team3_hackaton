# Cross-Entity Portfolio Review Playbook

## Action
Launch a cross-entity portfolio review with one relationship lead and shared pursuit list.

## Objective
Create one recurring forum where all entity-level teams align on growth, coordination, and risk decisions for a strategic client network.

## Scope
- Applies to parent + child + ownership-linked entities.
- Covers active pursuits, risk flags, and next-step introductions.
- Uses one source of truth: the shared pursuit list.

## Named Roles
- Relationship Lead: single accountable owner for portfolio decisions and escalation.
- Service Line Leads: responsible for offer strategy and pursuit execution.
- Delivery Lead: responsible for delivery risk and staffing signals.
- Operations Analyst: responsible for data updates and KPI tracking.

## Cadence
- Weekly 30-minute portfolio review.
- Monthly 45-minute executive sponsor checkpoint.

## Weekly Meeting Agenda (30 min)
1. KPI snapshot (5 min):
Validated relationship coverage, open pursuits, at-risk accounts, introductions-to-opportunities.
2. Pursuit list review (10 min):
Top 10 pursuits by stage, blockers, and next actions.
3. Cross-entity opportunities (10 min):
Adjacent services, sponsor intros, and bundled proposals.
4. Risk and decisions (5 min):
COI/compliance concerns, ownership changes, and go/no-go decisions.

## Decision Rules
- Every pursuit must have one owner and one next action date.
- Any pursuit with no movement for 14 days is flagged for decision.
- Any risk flagged as High requires a named mitigation owner in the same meeting.

## Shared Pursuit List Fields
Use [outputs/action_plans/shared_pursuit_list_template.csv](outputs/action_plans/shared_pursuit_list_template.csv).

Required fields:
- pursuit_id
- parent_account_id
- entity_client_id
- entity_client_name
- relationship_lead
- service_line
- opportunity_name
- stage
- estimated_value
- probability_pct
- risk_level
- blocker
- next_action
- next_action_owner
- next_action_due_date
- last_updated_utc

## 30-Day Launch Plan
1. Week 1:
Assign relationship lead per priority account and publish first pursuit list draft.
2. Week 2:
Start weekly review, validate entity mapping, and clean duplicate pursuits.
3. Week 3:
Run sponsor-led introductions for top 5 opportunities.
4. Week 4:
Publish first monthly readout: wins, risks, conversion rate, and asks.

## Success Metrics
- % pursuits with owner + next action date (target: >= 95%)
- Introductions-to-opportunities conversion rate
- Time from identified need to go/no-go decision
- Cross-entity win rate trend
- # of high-risk items mitigated within SLA

## Operating Notes
- Keep one canonical pursuit row per opportunity.
- Link each pursuit to a relationship context (PARENT_CHILD, OWNERSHIP, AFFILIATE, etc.).
- Use this as the standing operating model for Jordan Patel's strategic accounts.
