-- Retail analysis. One row is a recorded sales line, not a distinct order.
-- Run with: python analyze.py

-- 1. Portfolio KPI summary
SELECT COUNT(*) AS Sales_Lines,
       SUM(Quantity) AS Units_Sold,
       ROUND(SUM(Sales), 2) AS Total_Sales,
       ROUND(SUM(Profit), 2) AS Total_Profit,
       ROUND(100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0), 2) AS Profit_Margin_Pct
FROM SampleSuperstore;

-- 2. Category and subcategory profitability
SELECT Category, Sub_Category,
       ROUND(SUM(Sales), 2) AS Total_Sales,
       ROUND(SUM(Profit), 2) AS Total_Profit,
       ROUND(100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0), 2) AS Profit_Margin_Pct
FROM SampleSuperstore
GROUP BY Category, Sub_Category
ORDER BY Total_Profit ASC, Category, Sub_Category;

-- 3. Regional and state profitability
SELECT Region, State,
       ROUND(SUM(Sales), 2) AS Total_Sales,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM SampleSuperstore
GROUP BY Region, State
ORDER BY Total_Profit ASC, Region, State;

-- 4. Discount brackets. Counts are sales lines, not orders.
WITH Discounted_Lines AS (
    SELECT Sales, Profit,
           CASE WHEN Discount = 0 THEN '0%'
                WHEN Discount <= 0.10 THEN '1-10%'
                WHEN Discount <= 0.20 THEN '11-20%'
                WHEN Discount <= 0.30 THEN '21-30%'
                ELSE 'Above 30%' END AS Discount_Bracket,
           CASE WHEN Discount = 0 THEN 0
                WHEN Discount <= 0.10 THEN 1
                WHEN Discount <= 0.20 THEN 2
                WHEN Discount <= 0.30 THEN 3 ELSE 4 END AS Bracket_Order
    FROM SampleSuperstore
)
SELECT Discount_Bracket, COUNT(*) AS Sales_Lines,
       ROUND(SUM(Sales), 2) AS Total_Sales,
       ROUND(SUM(Profit), 2) AS Total_Profit,
       ROUND(AVG(Profit), 2) AS Avg_Profit_Per_Line
FROM Discounted_Lines
GROUP BY Discount_Bracket, Bracket_Order
ORDER BY Bracket_Order;

-- 5. Top 10 subcategories by profit. Product identifiers are unavailable.
SELECT Sub_Category, ROUND(SUM(Profit), 2) AS Total_Profit
FROM SampleSuperstore
GROUP BY Sub_Category
ORDER BY Total_Profit DESC, Sub_Category
LIMIT 10;

-- 6. Bottom 10 subcategories by profit
SELECT Sub_Category, ROUND(SUM(Profit), 2) AS Total_Profit
FROM SampleSuperstore
GROUP BY Sub_Category
ORDER BY Total_Profit ASC, Sub_Category
LIMIT 10;

-- 7. Segment performance. Unique customers cannot be counted from this extract.
SELECT Segment, COUNT(*) AS Sales_Lines, SUM(Quantity) AS Units_Sold,
       ROUND(SUM(Sales), 2) AS Total_Sales,
       ROUND(SUM(Profit), 2) AS Total_Profit,
       ROUND(100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0), 2) AS Profit_Margin_Pct
FROM SampleSuperstore
GROUP BY Segment
ORDER BY Total_Profit DESC, Segment;

-- 8. Category totals
SELECT Category, ROUND(SUM(Sales), 2) AS Total_Sales,
       ROUND(SUM(Profit), 2) AS Total_Profit
FROM SampleSuperstore
GROUP BY Category
ORDER BY Total_Profit DESC, Category;

-- 9. Exact discount levels and supporting sample sizes
SELECT Discount, COUNT(*) AS Sales_Lines,
       ROUND(AVG(Profit), 2) AS Avg_Profit_Per_Line
FROM SampleSuperstore
GROUP BY Discount
ORDER BY Discount;

-- 10. Regional sales contribution using a CTE and window aggregation
WITH Regional_Totals AS (
    SELECT Region, SUM(Sales) AS Sales, SUM(Profit) AS Profit
    FROM SampleSuperstore
    GROUP BY Region
)
SELECT Region, ROUND(Sales, 2) AS Total_Sales,
       ROUND(Profit, 2) AS Total_Profit,
       ROUND(100.0 * Sales / NULLIF(SUM(Sales) OVER (), 0), 2) AS Sales_Share_Pct
FROM Regional_Totals
ORDER BY Total_Sales DESC, Region;
