-- =====================================================================
-- Food Delivery Business Analytics and Performance Optimization System
-- Analytical Views and Stored Procedures (MySQL 8.0+)
-- =====================================================================
USE food_delivery_db;

-- =====================================================================
-- View 1: Unified Order Master View (vw_order_details)
-- Denormalizes orders with customer, restaurant, and rider dimensions
-- =====================================================================
CREATE OR REPLACE VIEW vw_order_details AS
SELECT 
    o.order_id,
    o.order_date,
    o.order_time,
    o.city,
    o.order_status,
    o.order_value,
    o.discount_amount,
    o.delivery_fee,
    o.platform_revenue,
    o.delivery_distance_km,
    o.delivery_time_mins,
    o.customer_rating,
    c.customer_id,
    c.customer_name,
    c.loyalty_tier,
    r.restaurant_id,
    r.restaurant_name,
    r.cuisine_category,
    p.partner_id,
    p.partner_name,
    p.vehicle_type,
    CASE 
        WHEN o.delivery_time_mins > 55.90 THEN 'Outlier Delay'
        WHEN o.delivery_time_mins > 40.00 THEN 'Delayed'
        WHEN o.delivery_time_mins IS NOT NULL THEN 'On-Time'
        ELSE 'Cancelled'
    END AS service_level_status
FROM food_orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
JOIN delivery_partners p ON o.partner_id = p.partner_id;

-- =====================================================================
-- View 2: City Performance Summary View (vw_city_kpi)
-- =====================================================================
CREATE OR REPLACE VIEW vw_city_kpi AS
SELECT 
    city,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(order_value), 2) AS total_gmv,
    ROUND(SUM(platform_revenue), 2) AS net_revenue,
    ROUND(AVG(order_value), 2) AS avg_order_value,
    ROUND(AVG(delivery_time_mins), 2) AS avg_delivery_time,
    ROUND(AVG(customer_rating), 2) AS avg_rating,
    ROUND(SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cancellation_rate
FROM food_orders
GROUP BY city;

-- =====================================================================
-- Stored Procedure 1: City Performance Deep-Dive
-- Call syntax: CALL sp_get_city_summary('Bangalore');
-- =====================================================================
DROP PROCEDURE IF EXISTS sp_get_city_summary;

DELIMITER //
CREATE PROCEDURE sp_get_city_summary(IN target_city VARCHAR(50))
BEGIN
    SELECT 
        city,
        COUNT(order_id) AS total_orders,
        ROUND(SUM(order_value), 2) AS total_gmv,
        ROUND(SUM(platform_revenue), 2) AS total_revenue,
        ROUND(AVG(delivery_time_mins), 2) AS avg_delivery_time,
        ROUND(AVG(customer_rating), 2) AS avg_rating,
        ROUND(SUM(CASE WHEN order_status = 'Cancelled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cancellation_rate_pct
    FROM food_orders
    WHERE city = target_city
    GROUP BY city;
    
    -- Top 5 Restaurants in that City
    SELECT 
        r.restaurant_name,
        r.cuisine_category,
        COUNT(o.order_id) AS orders_count,
        ROUND(SUM(o.order_value), 2) AS gmv
    FROM restaurants r
    JOIN food_orders o ON r.restaurant_id = o.restaurant_id
    WHERE r.city = target_city AND o.order_status = 'Delivered'
    GROUP BY r.restaurant_name, r.cuisine_category
    ORDER BY gmv DESC
    LIMIT 5;
END //
DELIMITER ;

-- =====================================================================
-- Stored Procedure 2: Fetch Outlier Orders for Root-Cause Analysis
-- Call syntax: CALL sp_get_delay_outliers(55.90);
-- =====================================================================
DROP PROCEDURE IF EXISTS sp_get_delay_outliers;

DELIMITER //
CREATE PROCEDURE sp_get_delay_outliers(IN delay_threshold DECIMAL(5, 2))
BEGIN
    SELECT 
        order_id,
        order_date,
        city,
        restaurant_name,
        partner_name,
        delivery_distance_km,
        delivery_time_mins,
        customer_rating
    FROM vw_order_details
    WHERE delivery_time_mins >= delay_threshold
    ORDER BY delivery_time_mins DESC;
END //
DELIMITER ;
