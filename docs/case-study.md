# Case study: separating revenue from profitable growth

## Decision context

A sales manager needs to identify where revenue and profitability diverge before changing category targets or discount rules. The available evidence is a 13-column extract of 9,994 sales lines, rather than a full transaction system.

## Approach

1. Inspect the workbook schema and define the sales-line grain before choosing KPIs.
2. Validate numeric fields and import every recorded line into SQLite without unsupported deduplication.
3. Use SQL aggregations, CASE expressions, CTEs, and a window total to compare categories, geography, segments, and discounts.
4. Export all ten query results and reconcile segment totals against dataset totals.
5. Separate observed patterns from recommendations that require an experiment or operational investigation.

## Evidence

Total sales are 2,297,200.86 and profit is 286,397.02, giving a weighted profit margin of 12.47%. Technology contributes 145,454.95 profit; Office Supplies contributes 122,490.80; Furniture contributes 18,451.27 despite substantial sales.

All observed discount levels above 20% have negative average line profit. The 50% discount group averages -310.70 profit over 66 sales lines. The 10% group averages 96.06 across 94 lines. Different group sizes and product mixes prevent a causal comparison from these aggregates alone.

West has the highest sales at 725,457.82. This supports a regional mix review, not a claim that West's practices can be transferred without checking profitability and customer mix.

## Recommendations to evaluate

- Investigate Furniture losses at the subcategory and discount level before extending promotions.
- Review deep-discount approvals, then measure both sales and profit in a controlled pilot.
- Compare regional margins and category composition before setting regional growth targets.

No realized savings, revenue uplift, or business deployment is claimed. The deliverable is a reproducible analysis and a set of evidence-based questions for decision makers.

## What would improve the analysis

Order and customer identifiers would enable valid order/customer KPIs. Dates would enable time trends. Product identifiers, cost components, and a documented currency would support more detailed profitability work. None of these fields is present in the supplied extract.
