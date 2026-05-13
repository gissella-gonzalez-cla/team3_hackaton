# Phase 2: Cross-Sell Propensity Model

## Model

- Type: Mixed Naive Bayes (stdlib implementation)
- Target: client has 2+ service lines (proxy)

## Test Metrics

- Accuracy: 0.8571
- Precision: 0.7
- Recall: 1.0
- F1: 0.8235

## Top 20 Cross-Sell Candidates

- C122868 - King Group: score=1.0 (services=1, active_projects=1, degree=0)
- C123507 - Obrien-Gibbs: score=1.0 (services=1, active_projects=2, degree=0)
- C103600 - Lakeshore County Government: score=0.9993 (services=1, active_projects=2, degree=0)
- C100377 - North Ridge Health Group: score=0.947 (services=1, active_projects=1, degree=4)
- C115847 - Williams Group: score=0.8957 (services=1, active_projects=1, degree=0)
- C114171 - Stein-Silva: score=0.2075 (services=1, active_projects=0, degree=0)
- C118014 - Trujillo, Hogan and Knight: score=0.0361 (services=1, active_projects=0, degree=0)
- C101820 - Cascade-backed Apex Logistics LLC: score=0.0252 (services=1, active_projects=0, degree=1)
- C102686 - Cascade-backed Coastal Hardware Co: score=0.0252 (services=1, active_projects=0, degree=1)
- C105993 - Apex Brokerage & Logistics LLC: score=0.0206 (services=1, active_projects=1, degree=0)
- C106472 - Hudson Freight Solutions Inc: score=0.0104 (services=1, active_projects=1, degree=0)
- C116788 - Gould, Marshall and Scott: score=0.0085 (services=1, active_projects=1, degree=0)
- C119665 - Rosales-White: score=0.0063 (services=1, active_projects=1, degree=0)
- C104514 - Vector Precision Industries: score=0.0052 (services=1, active_projects=1, degree=0)
- C107488 - Magnolia Energy Holdings LLC: score=0.0048 (services=1, active_projects=1, degree=1)
- C122611 - Garcia-Smith: score=0.0046 (services=1, active_projects=1, degree=0)
- C122245 - Martinez, Williams and Brown: score=0.0042 (services=1, active_projects=1, degree=0)
- C103948 - City of Pinewood: score=0.0041 (services=1, active_projects=1, degree=1)
- C107646 - Peachtree Industrial Partners: score=0.0036 (services=1, active_projects=1, degree=1)
- C119506 - Keith-Sanchez: score=0.003 (services=1, active_projects=1, degree=0)

## Output Files

- outputs/ml_cross_sell_metrics.json
- outputs/ml_cross_sell_ranked_candidates.csv
- outputs/ml_cross_sell_summary.md
- outputs/action_plans/top10_ml_cross_sell_pursuits.csv
