# Retail Sales & Profitability Analysis

**SQL · Excel · Python · SQLite**

A reproducible analysis of 9,994 Superstore sales lines: where sales become profit, which discounts accompany losses, and how performance varies across categories, regions, and customer segments.

## Business question

Which parts of the sales mix deserve closer attention when revenue growth does not translate into profit?

This project turns the supplied Excel extract into a local SQLite database, runs ten SQL analyses, and exports results that can be inspected in Excel or used in a portfolio case study.

## Results at a glance

| Metric | Verified result |
| --- | ---: |
| Recorded sales lines | 9,994 |
| Units sold | 37,873 |
| Total sales | 2,297,200.86 |
| Total profit | 286,397.02 |
| Profit / sales | 12.47% |

Amounts use the workbook's units; the extract does not specify a currency.

| Finding | Supporting result | Suggested business action |
| --- | --- | --- |
| Revenue alone masks category profitability | Furniture sales of 741,999.80 produce 18,451.27 profit, versus Technology profit of 145,454.95 | Review Furniture's subcategory and discount mix before increasing sales targets |
| Larger discounts accompany losses | Every observed discount level above 20% has negative average profit per sales line | Investigate discount approvals and product mix; test policy changes before rollout |
| West leads sales | West sales total 725,457.82, ahead of East at 678,781.24 | Compare regional mix and margins before copying sales tactics |

These are descriptive findings from this extract. They do not establish that a discount policy caused a loss or that an intervention improved performance.

## Run the analysis

Requires Python 3.12 (validated) and Internet access only for the initial dependency installation.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python analyze.py
python -m unittest -v
```

On Windows, activate with `.venv\Scripts\activate` instead. The command works from any directory because input paths resolve relative to the script.

Generated files are ignored by Git:

- `outputs/retail.sqlite`: local database with a `SampleSuperstore` table.
- `outputs/query-01.csv` through `query-10.csv`: results of the ten statements in [project.sql](project.sql).
- `outputs/summary.json`: totals, row counts, and result metadata.

Use `python analyze.py --output /path/to/results` for an alternative output directory. The importer checks the source schema, missing values, finite numeric values, positive integer quantities, nonnegative sales, and discount bounds before loading. It preserves repeated lines because this extract has no identifiers to distinguish legitimate repetitions from duplicates.

## Analysis walkthrough

| Query | Question | Technique |
| --- | --- | --- |
| 1 | What are the overall KPIs? | Aggregation and safe margin calculation |
| 2 | Which categories/subcategories contribute profit? | Grouping and margin comparison |
| 3 | Where is profit concentrated geographically? | Region/state aggregation |
| 4 | How does profitability vary by discount bracket? | CTE, CASE, explicit bracket ordering |
| 5–6 | Which ten subcategories rank highest/lowest by profit? | Deterministic sorting and LIMIT |
| 7 | How do customer segments compare? | Sales-line counts, units, and margins |
| 8 | How do category totals compare? | Category-level reconciliation |
| 9 | What happens at each exact discount level? | Averages with supporting sample sizes |
| 10 | What share of sales does each region contribute? | CTE and window aggregation |

## Data scope and metric definitions

The file is named `SampleSuperstore.csv.xlsx`, but it is an Excel workbook. The `SampleSuperstore` sheet contains 13 fields: shipping mode, segment, country, city, state, postal code, region, category, subcategory, sales, quantity, discount, and profit. See [the data dictionary](docs/data-dictionary.md).

One row is a recorded sales line. `COUNT(*)` measures lines; `SUM(Quantity)` measures units. Profit margin is `SUM(Profit) / SUM(Sales)`, with a zero-denominator guard, rather than an average of row margins.

The supplied extract has **no order ID, customer ID, product ID/name, or dates**. Distinct orders, unique customers, product-level rankings, monthly trends, and customer retention cannot be derived reliably. No joins are needed for this single-table extract. The SQL ranks subcategories rather than claiming to rank individual products.

SQLite stores monetary values as floating-point numbers for this exploratory analysis, with results rounded at output. Financial reporting would require an agreed decimal representation and rounding policy.

## Validation

Six automated tests cover the full supplied dataset, repeatable execution, category-independent segment reconciliation, regional sales-share totals, top/bottom result limits, and rejection of malformed workbook values/schema. GitHub Actions is configured to run those tests and regenerate the analysis on pushes and pull requests.

## Files and related work

- [SQL analysis](project.sql) · [Python runner](analyze.py) · [validation tests](test_analysis.py)
- [Case study](docs/case-study.md) · [data dictionary](docs/data-dictionary.md)
- [Healthcare Billing Dashboard](https://github.com/marwanfaisal14/-Healthcare-Billing-Cost-Analysis-Dashboard-Power-BI-)
- [Pizza Sales Dashboard](https://github.com/marwanfaisal14/Pizza-sales-dashboard)
