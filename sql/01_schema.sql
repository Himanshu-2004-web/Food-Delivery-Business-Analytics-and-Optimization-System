-- =====================================================================
-- Food Delivery Business Analytics and Performance Optimization System
-- Database Schema Definition (MySQL 8.0+)
-- =====================================================================

-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS food_delivery_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE food_delivery_db;

-- Step 2: Drop Existing Tables (in reverse foreign-key dependency order)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS food_orders;
DROP TABLE IF EXISTS delivery_partners;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS customers;

-- =====================================================================
-- 1. Customers Master Table
-- =====================================================================
CREATE TABLE customers (
    customer_id INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    loyalty_tier ENUM('Regular', 'Silver', 'Gold') NOT NULL DEFAULT 'Regular',
    age INT NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_customers PRIMARY KEY (customer_id)
) ENGINE=InnoDB COMMENT='Master customer demographic & loyalty tier profiles';

-- =====================================================================
-- 2. Restaurants Master Table
-- =====================================================================
CREATE TABLE restaurants (
    restaurant_id INT NOT NULL,
    restaurant_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    cuisine_category VARCHAR(50) NOT NULL,
    avg_rating DECIMAL(3, 2) NOT NULL DEFAULT 0.00,
    commission_rate DECIMAL(4, 2) NOT NULL DEFAULT 0.20,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_restaurants PRIMARY KEY (restaurant_id)
) ENGINE=InnoDB COMMENT='Partner restaurants with cuisine and commission rates';

-- =====================================================================
-- 3. Delivery Partners Master Table
-- =====================================================================
CREATE TABLE delivery_partners (
    partner_id INT NOT NULL,
    partner_name VARCHAR(100) NOT NULL,
    base_city VARCHAR(50) NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL,
    rating DECIMAL(3, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_delivery_partners PRIMARY KEY (partner_id)
) ENGINE=InnoDB COMMENT='Registered delivery fleet riders across metropolitan hubs';

-- =====================================================================
-- 4. Food Orders Table (Fact / Transaction Table)
-- =====================================================================
CREATE TABLE food_orders (
    order_id VARCHAR(20) NOT NULL,
    order_date DATE NOT NULL,
    order_time TIME NOT NULL,
    customer_id INT NOT NULL,
    restaurant_id INT NOT NULL,
    partner_id INT NOT NULL,
    city VARCHAR(50) NOT NULL,
    cuisine_category VARCHAR(50) NOT NULL,
    order_value DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    delivery_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    platform_commission_pct DECIMAL(4, 2) NOT NULL,
    platform_revenue DECIMAL(10, 2) NOT NULL,
    delivery_distance_km DECIMAL(5, 2) NOT NULL,
    delivery_time_mins DECIMAL(5, 2) NULL,
    payment_method VARCHAR(50) NOT NULL,
    order_status ENUM('Delivered', 'Cancelled', 'Returned') NOT NULL DEFAULT 'Delivered',
    customer_rating DECIMAL(2, 1) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_food_orders PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) 
        REFERENCES customers (customer_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_orders_restaurant FOREIGN KEY (restaurant_id) 
        REFERENCES restaurants (restaurant_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_orders_partner FOREIGN KEY (partner_id) 
        REFERENCES delivery_partners (partner_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Primary transactional orders dataset (2,000 orders)';

-- Performance Indexes on Fact Table
CREATE INDEX idx_orders_customer_id ON food_orders (customer_id);
CREATE INDEX idx_orders_restaurant_id ON food_orders (restaurant_id);
CREATE INDEX idx_orders_partner_id ON food_orders (partner_id);
CREATE INDEX idx_orders_date ON food_orders (order_date);
CREATE INDEX idx_orders_city ON food_orders (city);
CREATE INDEX idx_orders_status ON food_orders (order_status);
CREATE INDEX idx_orders_cuisine ON food_orders (cuisine_category);

-- =====================================================================
-- 5. Order Items Table (Granular Order Line Items)
-- =====================================================================
CREATE TABLE order_items (
    item_id VARCHAR(20) NOT NULL,
    order_id VARCHAR(20) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    item_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_order_items PRIMARY KEY (item_id),
    CONSTRAINT fk_items_order FOREIGN KEY (order_id) 
        REFERENCES food_orders (order_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB COMMENT='Granular item-level line items for each order (3,994 items)';

-- Performance Index on Foreign Key
CREATE INDEX idx_items_order_id ON order_items (order_id);
