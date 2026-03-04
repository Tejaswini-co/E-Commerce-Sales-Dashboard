-- ============================================================================
-- E-COMMERCE SALES ANALYSIS - SQL QUERIES
-- Superstore Dataset Analysis
-- ============================================================================

-- This file contains SQL queries for analyzing the Superstore dataset
-- These queries can be used in SQLite, PostgreSQL, MySQL, or other SQL databases

-- ============================================================================
-- 1. REVENUE TRENDS ANALYSIS
-- ============================================================================

-- Monthly Revenue Trends
SELECT 
    strftime('%Y-%m', "Order Date") AS Year_Month,
    COUNT(DISTINCT "Order ID") AS Total_Orders,
    SUM(Sales) AS Total_Revenue,
    SUM(Profit) AS Total_Profit,
    SUM(Quantity) AS Total_Quantity,
    ROUND(AVG(Sales), 2) AS Avg_Order_Value,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM superstore
GROUP BY Year_Month
ORDER BY Year_Month;

-- Yearly Revenue Summary
SELECT 
    strftime('%Y', "Order Date") AS Year,
    COUNT(DISTINCT "Order ID") AS Total_Orders,
    COUNT(DISTINCT "Customer ID") AS Total_Customers,
    SUM(Sales) AS Total_Revenue,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct,
    ROUND(SUM(Sales) / COUNT(DISTINCT "Order ID"), 2) AS Avg_Order_Value
FROM superstore
GROUP BY Year
ORDER BY Year;

-- Quarterly Performance
SELECT 
    strftime('%Y', "Order Date") AS Year,
    CASE 
        WHEN CAST(strftime('%m', "Order Date") AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
        WHEN CAST(strftime('%m', "Order Date") AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
        WHEN CAST(strftime('%m', "Order Date") AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
        ELSE 'Q4'
    END AS Quarter,
    SUM(Sales) AS Revenue,
    SUM(Profit) AS Profit,
    COUNT(DISTINCT "Order ID") AS Orders
FROM superstore
GROUP BY Year, Quarter
ORDER BY Year, Quarter;

-- ============================================================================
-- 2. REGIONAL PERFORMANCE ANALYSIS
-- ============================================================================

-- Sales Performance by Region
SELECT 
    Region,
    COUNT(DISTINCT "Order ID") AS Total_Orders,
    COUNT(DISTINCT "Customer ID") AS Total_Customers,
    COUNT(DISTINCT "Product ID") AS Products_Sold,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct,
    ROUND(SUM(Sales) / COUNT(DISTINCT "Order ID"), 2) AS Avg_Order_Value,
    SUM(Quantity) AS Total_Quantity
FROM superstore
GROUP BY Region
ORDER BY Total_Sales DESC;

-- Top 15 States by Sales
SELECT 
    State,
    Region,
    COUNT(DISTINCT "Order ID") AS Orders,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM superstore
GROUP BY State, Region
ORDER BY Total_Sales DESC
LIMIT 15;

-- Top 20 Cities by Revenue
SELECT 
    City,
    State,
    Region,
    COUNT(DISTINCT "Customer ID") AS Customers,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM superstore
GROUP BY City, State, Region
ORDER BY Total_Sales DESC
LIMIT 20;

-- Regional Sales Trends by Year
SELECT 
    strftime('%Y', "Order Date") AS Year,
    Region,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit
FROM superstore
GROUP BY Year, Region
ORDER BY Year, Region;

-- ============================================================================
-- 3. PROFIT MARGIN ANALYSIS
-- ============================================================================

-- Overall Profitability Metrics
SELECT 
    COUNT(DISTINCT "Order ID") AS Total_Orders,
    SUM(Sales) AS Total_Revenue,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Overall_Profit_Margin_Pct,
    SUM(CASE WHEN Profit > 0 THEN 1 ELSE 0 END) AS Profitable_Orders,
    SUM(CASE WHEN Profit < 0 THEN 1 ELSE 0 END) AS Loss_Orders,
    SUM(CASE WHEN Profit = 0 THEN 1 ELSE 0 END) AS Breakeven_Orders
FROM superstore;

-- Profit Analysis by Category
SELECT 
    Category,
    COUNT(DISTINCT "Order ID") AS Orders,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct,
    ROUND(AVG(Profit), 2) AS Avg_Profit_Per_Order
FROM superstore
GROUP BY Category
ORDER BY Total_Profit DESC;

-- Profit Analysis by Sub-Category
SELECT 
    Category,
    "Sub-Category",
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct,
    COUNT(DISTINCT "Order ID") AS Orders
FROM superstore
GROUP BY Category, "Sub-Category"
ORDER BY Total_Profit DESC;

-- Discount Impact on Profitability
SELECT 
    CASE 
        WHEN Discount = 0 THEN 'No Discount'
        WHEN Discount <= 0.1 THEN '1-10%'
        WHEN Discount <= 0.2 THEN '11-20%'
        WHEN Discount <= 0.3 THEN '21-30%'
        ELSE '>30%'
    END AS Discount_Range,
    COUNT(*) AS Order_Count,
    ROUND(AVG(Sales), 2) AS Avg_Sales,
    ROUND(AVG(Profit), 2) AS Avg_Profit,
    ROUND(AVG(Profit / NULLIF(Sales, 0)) * 100, 2) AS Avg_Profit_Margin_Pct
FROM superstore
GROUP BY Discount_Range
ORDER BY 
    CASE Discount_Range
        WHEN 'No Discount' THEN 1
        WHEN '1-10%' THEN 2
        WHEN '11-20%' THEN 3
        WHEN '21-30%' THEN 4
        ELSE 5
    END;

-- Monthly Profit Trends
SELECT 
    strftime('%Y-%m', "Order Date") AS Year_Month,
    SUM(Sales) AS Revenue,
    SUM(Profit) AS Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM superstore
GROUP BY Year_Month
ORDER BY Year_Month;

-- ============================================================================
-- 4. TOP PRODUCTS ANALYSIS
-- ============================================================================

-- Top 10 Products by Sales Revenue
SELECT 
    "Product Name",
    Category,
    "Sub-Category",
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    SUM(Quantity) AS Quantity_Sold,
    COUNT(DISTINCT "Order ID") AS Orders,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM superstore
GROUP BY "Product Name", Category, "Sub-Category"
ORDER BY Total_Sales DESC
LIMIT 10;

-- Top 10 Products by Profit
SELECT 
    "Product Name",
    Category,
    "Sub-Category",
    SUM(Profit) AS Total_Profit,
    SUM(Sales) AS Total_Sales,
    SUM(Quantity) AS Quantity_Sold,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM superstore
GROUP BY "Product Name", Category, "Sub-Category"
ORDER BY Total_Profit DESC
LIMIT 10;

-- Top 10 Products by Quantity Sold
SELECT 
    "Product Name",
    Category,
    "Sub-Category",
    SUM(Quantity) AS Quantity_Sold,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    COUNT(DISTINCT "Order ID") AS Orders
FROM superstore
GROUP BY "Product Name", Category, "Sub-Category"
ORDER BY Quantity_Sold DESC
LIMIT 10;

-- Worst 10 Products by Profit (Biggest Losses)
SELECT 
    "Product Name",
    Category,
    "Sub-Category",
    SUM(Profit) AS Total_Profit,
    SUM(Sales) AS Total_Sales,
    SUM(Quantity) AS Quantity_Sold
FROM superstore
GROUP BY "Product Name", Category, "Sub-Category"
ORDER BY Total_Profit ASC
LIMIT 10;

-- ============================================================================
-- 5. CUSTOMER SEGMENT ANALYSIS
-- ============================================================================

-- Performance by Customer Segment
SELECT 
    Segment,
    COUNT(DISTINCT "Customer ID") AS Total_Customers,
    COUNT(DISTINCT "Order ID") AS Total_Orders,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(AVG(Sales), 2) AS Avg_Order_Value,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM superstore
GROUP BY Segment
ORDER BY Total_Sales DESC;

-- Customer Segment by Category
SELECT 
    Segment,
    Category,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    COUNT(DISTINCT "Order ID") AS Orders
FROM superstore
GROUP BY Segment, Category
ORDER BY Segment, Total_Sales DESC;

-- Top 20 Customers by Revenue
SELECT 
    "Customer Name",
    "Customer ID",
    Segment,
    COUNT(DISTINCT "Order ID") AS Total_Orders,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Sales) / COUNT(DISTINCT "Order ID"), 2) AS Avg_Order_Value
FROM superstore
GROUP BY "Customer Name", "Customer ID", Segment
ORDER BY Total_Sales DESC
LIMIT 20;

-- ============================================================================
-- 6. CATEGORY & SUB-CATEGORY ANALYSIS
-- ============================================================================

-- Category Performance Summary
SELECT 
    Category,
    COUNT(DISTINCT "Product ID") AS Unique_Products,
    COUNT(DISTINCT "Order ID") AS Total_Orders,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    SUM(Quantity) AS Quantity_Sold,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM superstore
GROUP BY Category
ORDER BY Total_Sales DESC;

-- Sub-Category Performance
SELECT 
    "Sub-Category",
    Category,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    SUM(Quantity) AS Quantity_Sold,
    COUNT(DISTINCT "Order ID") AS Orders,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin_Pct
FROM superstore
GROUP BY "Sub-Category", Category
ORDER BY Total_Sales DESC;

-- ============================================================================
-- 7. SHIPPING & DELIVERY ANALYSIS
-- ============================================================================

-- Performance by Ship Mode
SELECT 
    "Ship Mode",
    COUNT(DISTINCT "Order ID") AS Orders,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(AVG(julianday("Ship Date") - julianday("Order Date")), 1) AS Avg_Shipping_Days
FROM superstore
GROUP BY "Ship Mode"
ORDER BY Orders DESC;

-- ============================================================================
-- 8. ADVANCED ANALYTICS QUERIES
-- ============================================================================

-- Year-over-Year Growth Analysis
WITH YearlySales AS (
    SELECT 
        strftime('%Y', "Order Date") AS Year,
        SUM(Sales) AS Total_Sales,
        SUM(Profit) AS Total_Profit
    FROM superstore
    GROUP BY Year
)
SELECT 
    Year,
    Total_Sales,
    Total_Profit,
    LAG(Total_Sales) OVER (ORDER BY Year) AS Previous_Year_Sales,
    ROUND((Total_Sales - LAG(Total_Sales) OVER (ORDER BY Year)) / 
          LAG(Total_Sales) OVER (ORDER BY Year) * 100, 2) AS Sales_Growth_Pct
FROM YearlySales
ORDER BY Year;

-- RFM Analysis (Recency, Frequency, Monetary)
SELECT 
    "Customer ID",
    "Customer Name",
    Segment,
    julianday('now') - julianday(MAX("Order Date")) AS Recency_Days,
    COUNT(DISTINCT "Order ID") AS Frequency,
    SUM(Sales) AS Monetary_Value,
    ROUND(SUM(Sales) / COUNT(DISTINCT "Order ID"), 2) AS Avg_Order_Value
FROM superstore
GROUP BY "Customer ID", "Customer Name", Segment
ORDER BY Monetary_Value DESC
LIMIT 50;

-- Product Performance Matrix
SELECT 
    "Product Name",
    Category,
    SUM(Sales) AS Total_Sales,
    SUM(Profit) AS Total_Profit,
    ROUND(SUM(Profit) / SUM(Sales) * 100, 2) AS Profit_Margin,
    CASE 
        WHEN SUM(Sales) > (SELECT AVG(product_sales) FROM (
            SELECT SUM(Sales) AS product_sales FROM superstore GROUP BY "Product Name"
        )) THEN 'High Sales'
        ELSE 'Low Sales'
    END AS Sales_Category,
    CASE 
        WHEN SUM(Profit) / SUM(Sales) * 100 > 10 THEN 'High Margin'
        ELSE 'Low Margin'
    END AS Margin_Category
FROM superstore
GROUP BY "Product Name", Category
HAVING SUM(Sales) > 1000
ORDER BY Total_Sales DESC;

-- ============================================================================
-- END OF SQL QUERIES
-- ============================================================================
