-- =====================================================================
-- Food Delivery Business Analytics and Performance Optimization System
-- Analytical SQL Queries (MySQL 8.0+)
-- =====================================================================
USE food_delivery_db;

-- =====================================================================
-- 1. Executive Summary & Core Platform KPIs
-- Calculates total volume, GMV, net revenue, fulfillment & cancellation rates
-- =====================================================================
SELECT 
    COUNT(*) AS total_orders_placed,
    SUM(CASE WHEN order_status = 'Delivered' THEN 1 ELSE 0 END) AS delivered_orders,
    SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) AS cancelled_orders,
    ROUND(SUM(CASE WHEN order_status = 'Delivered' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS fulfillment_rate_pct,
    ROUND(SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS cancellation_rate_pct,
    ROUND(SUM(order_value), 2) AS gross_merchandise_value_inr,
    ROUND(SUM(platform_revenue), 2) AS net_platform_revenue_inr,
    ROUND(AVG(order_value), 2) AS average_order_value_inr,
    ROUND(AVG(delivery_time_mins), 2) AS avg_delivery_time_mins,
    ROUND(AVG(customer_rating), 2) AS avg_customer_rating
FROM food_orders;

-- =====================================================================
-- 2. City Performance Benchmark
-- Cross-city comparison of volume, revenue, delivery speed, and rating
-- =====================================================================
SELECT 
    city,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(order_value), 2) AS total_gmv,
    ROUND(SUM(platform_revenue), 2) AS platform_revenue,
    ROUND(AVG(order_value), 2) AS avg_order_value,
    ROUND(AVG(delivery_time_mins), 2) AS avg_delivery_time_mins,
    ROUND(AVG(customer_rating), 2) AS avg_customer_rating,
    ROUND(SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS cancellation_rate_pct
FROM food_orders
GROUP BY city
ORDER BY platform_revenue DESC;

-- =====================================================================
-- 3. Monthly Trend & Growth Analysis
-- Aggregates orders and revenue month by month
-- =====================================================================
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS order_month,
    COUNT(order_id) AS monthly_orders,
    ROUND(SUM(order_value), 2) AS monthly_gmv,
    ROUND(SUM(platform_revenue), 2) AS monthly_platform_revenue,
    ROUND(AVG(order_value), 2) AS monthly_aov
FROM food_orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY order_month ASC;

-- =====================================================================
-- 4. Peak Hour Demand Distribution
-- Identifies peak lunch (12:00-14:00) and dinner (19:00-22:00) order clusters
-- =====================================================================
SELECT 
    HOUR(order_time) AS order_hour,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(order_value), 2) AS total_revenue,
    ROUND(AVG(delivery_time_mins), 1) AS avg_delivery_time_mins,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM food_orders), 2) AS order_share_pct
FROM food_orders
GROUP BY HOUR(order_time)
ORDER BY order_hour ASC;

-- =====================================================================
-- 5. Customer Loyalty Tier Contribution
-- Evaluates spending power, discounts availed, and frequency across tiers
-- =====================================================================
SELECT 
    c.loyalty_tier,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    COUNT(o.order_id) AS total_orders_placed,
    ROUND(SUM(o.order_value), 2) AS total_spend_gmv,
    ROUND(AVG(o.order_value), 2) AS avg_order_value,
    ROUND(SUM(o.discount_amount), 2) AS total_discounts_given,
    ROUND(AVG(o.customer_rating), 2) AS avg_customer_rating
FROM customers c
LEFT JOIN food_orders o ON c.customer_id = o.customer_id
GROUP BY c.loyalty_tier
ORDER BY total_spend_gmv DESC;

-- =====================================================================
-- 6. Restaurant Performance & Commission Leaderboard
-- Top restaurants ranked by Gross Merchandise Value and platform earnings
-- =====================================================================
SELECT 
    r.restaurant_id,
    r.restaurant_name,
    r.city,
    r.cuisine_category,
    r.commission_rate,
    COUNT(o.order_id) AS orders_fulfilled,
    ROUND(SUM(o.order_value), 2) AS total_gmv,
    ROUND(SUM(o.platform_revenue), 2) AS total_commission_earned,
    ROUND(AVG(o.customer_rating), 2) AS actual_avg_rating
FROM restaurants r
JOIN food_orders o ON r.restaurant_id = o.restaurant_id
WHERE o.order_status = 'Delivered'
GROUP BY r.restaurant_id, r.restaurant_name, r.city, r.cuisine_category, r.commission_rate
ORDER BY total_gmv DESC
LIMIT 10;

-- =====================================================================
-- 7. Delivery Partner Performance by Vehicle Type
-- Analyzes speed and ratings across Motorcycle, Scooter, and Electric Bike
-- =====================================================================
SELECT 
    p.vehicle_type,
    COUNT(DISTINCT p.partner_id) AS partner_count,
    COUNT(o.order_id) AS completed_trips,
    ROUND(AVG(o.delivery_distance_km), 2) AS avg_distance_km,
    ROUND(AVG(o.delivery_time_mins), 2) AS avg_delivery_time_mins,
    ROUND(AVG(o.customer_rating), 2) AS avg_trip_rating
FROM delivery_partners p
JOIN food_orders o ON p.partner_id = o.partner_id
WHERE o.order_status = 'Delivered'
GROUP BY p.vehicle_type
ORDER BY completed_trips DESC;

-- =====================================================================
-- 8. Diagnostic Query: Delivery Delay Impact on Customer Ratings
-- Proves the inverse relationship between delivery duration and review rating
-- =====================================================================
SELECT 
    CASE 
        WHEN delivery_time_mins < 25 THEN 'Under 25 mins (Super Fast)'
        WHEN delivery_time_mins BETWEEN 25 AND 35 THEN '25 - 35 mins (Standard)'
        WHEN delivery_time_mins BETWEEN 35.01 AND 45 THEN '35 - 45 mins (Moderate Delay)'
        WHEN delivery_time_mins BETWEEN 45.01 AND 55 THEN '45 - 55 mins (Significant Delay)'
        ELSE 'Over 55 mins (Severe Delay / Outlier)'
    END AS delivery_speed_bracket,
    COUNT(order_id) AS order_count,
    ROUND(AVG(delivery_time_mins), 1) AS avg_delivery_time,
    ROUND(AVG(customer_rating), 2) AS avg_customer_rating,
    ROUND(SUM(CASE WHEN customer_rating <= 2 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS low_rating_pct
FROM food_orders
WHERE order_status = 'Delivered' AND delivery_time_mins IS NOT NULL
GROUP BY delivery_speed_bracket
ORDER BY avg_delivery_time ASC;

-- =====================================================================
-- 9. Statistical Outliers: Orders Exceeding IQR Upper Bound (55.90 mins)
-- Identifies critical bottleneck orders requiring operational investigation
-- =====================================================================
SELECT 
    o.order_id,
    o.order_date,
    o.city,
    r.restaurant_name,
    p.partner_name,
    p.vehicle_type,
    o.delivery_distance_km,
    o.delivery_time_mins,
    o.customer_rating
FROM food_orders o
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
JOIN delivery_partners p ON o.partner_id = p.partner_id
WHERE o.delivery_time_mins > 55.90
ORDER BY o.delivery_time_mins DESC;

-- =====================================================================
-- 10. Payment Method Distribution & Digital Adoption
-- Breakdown of transactions across UPI, Cards, Cash, and Wallets
-- =====================================================================
SELECT 
    payment_method,
    COUNT(order_id) AS transaction_count,
    ROUND(COUNT(order_id) * 100.0 / (SELECT COUNT(*) FROM food_orders), 2) AS transaction_share_pct,
    ROUND(SUM(order_value), 2) AS total_gmv,
    ROUND(AVG(order_value), 2) AS avg_ticket_size
FROM food_orders
GROUP BY payment_method
ORDER BY transaction_count DESC;

-- =====================================================================
-- 11. Top Selling Items & Cuisine Basket Analysis
-- =====================================================================
SELECT 
    i.item_name,
    o.cuisine_category,
    SUM(i.quantity) AS total_quantity_sold,
    ROUND(SUM(i.quantity * i.item_price), 2) AS total_item_sales_inr,
    ROUND(AVG(i.item_price), 2) AS avg_unit_price
FROM order_items i
JOIN food_orders o ON i.order_id = o.order_id
GROUP BY i.item_name, o.cuisine_category
ORDER BY total_item_sales_inr DESC
LIMIT 10;
