-- 1. Sales & profit by category/sub-category ? 
SELECT Category, Sub_Category,
       SUM(Sales) AS Total_Sales,
       SUM(Profit) AS Total_Profit,
       ROUND(SUM(Profit)/SUM(Sales)*100, 2) AS Profit_Margin_Pct
FROM SampleSuperstore
GROUP BY Category, Sub_Category
ORDER BY Total_Profit ASC;

--2. Profit by region/state ?
SELECT Region, State,
       SUM(Sales) AS Total_Sales,
       SUM(Profit) AS Total_Profit
FROM SampleSuperstore
GROUP BY Region, State
ORDER BY Total_Profit ASC ;

-- 3. Discount vs. profit (the key insight query) ?
SELECT 
  CASE 
    WHEN Discount = 0 THEN '0%'
    WHEN Discount <= 0.10 THEN '1-10%'
    WHEN Discount <= 0.20 THEN '11-20%'
    WHEN Discount <= 0.30 THEN '21-30%'
    ELSE '30%+'
  END AS Discount_Bracket,
  COUNT(*) AS Order_Count,
  SUM(Sales) AS Total_Sales,
  SUM(Profit) AS Total_Profit,
  ROUND(AVG(Profit), 2) AS Avg_Profit_Per_Order
FROM SampleSuperstore
GROUP BY  CASE 
    WHEN Discount = 0 THEN '0%'
    WHEN Discount <= 0.10 THEN '1-10%'
    WHEN Discount <= 0.20 THEN '11-20%'
    WHEN Discount <= 0.30 THEN '21-30%'
    ELSE '30%+'
    end
ORDER BY Discount_Bracket;


-- 5. Top/bottom 10 products by profit ? 

-- Top 10
SELECT Sub_Category, SUM(Profit) AS Total_Profit
FROM SampleSuperstore GROUP BY Sub_Category
ORDER BY Total_Profit DESC;

-- Bottom 10
SELECT Sub_Category, SUM(Profit) AS Total_Profit
FROM SampleSuperstore GROUP BY Sub_Category
ORDER BY Total_Profit ASC;

-- 6. Segment performance ? 
SELECT Segment,
       SUM(Sales) AS Total_Sales,
       SUM(Profit) AS Total_Profit,
       COUNT(DISTINCT Segment) AS Customer_Count
FROM SampleSuperstore
GROUP BY Segment
ORDER BY Total_Profit DESC;


select * from SampleSuperstore ; 

