# Supplied extract: data dictionary

The workbook has a single data sheet named `SampleSuperstore`; an additional empty sheet is not imported. Source columns retain their order. SQL column names replace spaces and hyphens with underscores.

| Source field | SQL field | Meaning and handling |
| --- | --- | --- |
| Ship Mode | Ship_Mode | Recorded shipping service category |
| Segment | Segment | Customer segment, not customer identity |
| Country | Country | Recorded country |
| City | City | Recorded city |
| State | State | Recorded state |
| Postal Code | Postal_Code | Stored as text in SQLite; leading zeros absent from the workbook are not reconstructed |
| Region | Region | Recorded sales region |
| Category | Category | Broad merchandise category |
| Sub-Category | Sub_Category | Merchandise subcategory, not a unique product |
| Sales | Sales | Nonnegative sales amount in unspecified source currency |
| Quantity | Quantity | Positive integer units for the recorded line |
| Discount | Discount | Fraction in [0, 1], so 0.20 means 20% |
| Profit | Profit | Recorded profit amount; negative values are valid |

The workbook has no data-source URL, license, extraction date, or date coverage documented in this repository. Confirm the original data's attribution and reuse terms before distributing it elsewhere. No provenance or time period is inferred from familiarity with the Superstore name.
