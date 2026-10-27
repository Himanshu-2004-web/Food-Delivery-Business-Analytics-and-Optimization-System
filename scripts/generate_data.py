"""
Data Generation Script: Food Delivery Business Analytics
Generates realistic, relatable relational data for 2,000 orders across 5 major cities.
Produces both raw (with realistic noise/duplicates/missing values) and cleaned datasets,
along with relational master tables (Customers, Restaurants, Delivery_Partners, Order_Items).
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Fix seed for strict reproducibility
np.random.seed(42)
random.seed(42)

# Directory Setup
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# 1. Master Data Definitions
CITIES = ['Bangalore', 'Mumbai', 'Delhi NCR', 'Hyderabad', 'Pune']
PAYMENT_METHODS = ['UPI', 'Credit Card', 'Debit Card', 'Cash on Delivery', 'Digital Wallet']
CUISINES = ['North Indian', 'Biryani', 'Fast Food', 'South Indian', 'Desserts', 'Chinese', 'Italian']

# Restaurants (20 entities)
RESTAURANTS_DATA = [
    (101, "Spice Hub", "Bangalore", "North Indian", 4.3, 0.20),
    (102, "Royal Biryani Mahal", "Hyderabad", "Biryani", 4.6, 0.22),
    (103, "Pizza Fiesta", "Mumbai", "Italian", 4.1, 0.18),
    (104, "Burger Junction", "Delhi NCR", "Fast Food", 4.2, 0.18),
    (105, "Wok Express", "Bangalore", "Chinese", 3.9, 0.20),
    (106, "Green Leaf Veg", "Pune", "South Indian", 4.5, 0.15),
    (107, "Sweet Tooth Bakery", "Mumbai", "Desserts", 4.7, 0.25),
    (108, "Dilli 6 Chaat Corner", "Delhi NCR", "Fast Food", 4.4, 0.18),
    (109, "Hyderabadi Bawarchi", "Hyderabad", "Biryani", 4.3, 0.20),
    (110, "Puneri Thali House", "Pune", "North Indian", 4.0, 0.18),
    (111, "Udupi Sagar", "Bangalore", "South Indian", 4.4, 0.15),
    (112, "Tandoori Nights", "Delhi NCR", "North Indian", 3.8, 0.22),
    (113, "Chowpatty Delights", "Mumbai", "Fast Food", 4.2, 0.18),
    (114, "Nizam's Kitchen", "Hyderabad", "Biryani", 4.5, 0.22),
    (115, "Pasta Street", "Bangalore", "Italian", 4.0, 0.20),
    (116, "The Belgian Waffle Co", "Pune", "Desserts", 4.6, 0.25),
    (117, "Dragon Bowl", "Mumbai", "Chinese", 3.7, 0.20),
    (118, "Punjabi Angithi", "Delhi NCR", "North Indian", 4.3, 0.20),
    (119, "Paradise Flavors", "Hyderabad", "Biryani", 4.1, 0.20),
    (120, "Cafe Goodluck", "Pune", "Fast Food", 4.5, 0.18)
]

df_restaurants = pd.DataFrame(RESTAURANTS_DATA, columns=[
    'restaurant_id', 'restaurant_name', 'city', 'cuisine_category', 'avg_rating', 'commission_rate'
])

# Delivery Partners (30 entities)
VEHICLE_TYPES = ['Motorcycle', 'Scooter', 'Electric Bike']
PARTNERS_DATA = []
for p_id in range(201, 231):
    city = random.choice(CITIES)
    vehicle = random.choice(VEHICLE_TYPES)
    rating = round(random.uniform(4.0, 4.9), 1)
    PARTNERS_DATA.append((p_id, f"Partner_{p_id}", city, vehicle, rating))

df_partners = pd.DataFrame(PARTNERS_DATA, columns=[
    'partner_id', 'partner_name', 'base_city', 'vehicle_type', 'rating'
])

# Customers (300 entities)
TIERS = ['Regular', 'Silver', 'Gold']
CUSTOMERS_DATA = []
for c_id in range(1001, 1301):
    c_city = random.choice(CITIES)
    tier = np.random.choice(TIERS, p=[0.60, 0.25, 0.15])
    age = random.randint(18, 58)
    gender = random.choice(['Male', 'Female', 'Other'])
    CUSTOMERS_DATA.append((c_id, f"Customer_{c_id}", c_city, tier, age, gender))

df_customers = pd.DataFrame(CUSTOMERS_DATA, columns=[
    'customer_id', 'customer_name', 'city', 'loyalty_tier', 'age', 'gender'
])

# 2. Generate 2,000 Orders
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

orders = []
order_items = []
item_counter = 1

for i in range(1, 2001):
    order_id = f"ORD{1000 + i}"
    
    # Customer
    cust = df_customers.sample(1).iloc[0]
    cust_id = cust['customer_id']
    city = cust['city']
    
    # Pick restaurant in the same city
    city_restaurants = df_restaurants[df_restaurants['city'] == city]
    if len(city_restaurants) == 0:
        city_restaurants = df_restaurants
    rest = city_restaurants.sample(1).iloc[0]
    rest_id = rest['restaurant_id']
    rest_name = rest['restaurant_name']
    cuisine = rest['cuisine_category']
    commission_pct = rest['commission_rate']
    
    # Pick delivery partner in same city
    city_partners = df_partners[df_partners['base_city'] == city]
    if len(city_partners) == 0:
        city_partners = df_partners
    partner = city_partners.sample(1).iloc[0]
    partner_id = partner['partner_id']
    
    # Date & Peak Hours
    random_day = random.randint(0, date_range_days)
    order_date = start_date + timedelta(days=random_day)
    
    # Time weighting: peaks at lunch (12-14) and dinner (19-22)
    hour_weights = [
        1, 1, 0, 0, 0, 0, 1, 2, 4, 3, 5, 8,     # 00:00 to 11:00
        12, 10, 6, 4, 3, 4, 7, 12, 15, 12, 6, 2  # 12:00 to 23:00
    ]
    norm_weights = [w / sum(hour_weights) for w in hour_weights]
    hour = np.random.choice(range(24), p=norm_weights)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    order_time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
    
    # Delivery Distance (km): lognormal distribution around 4.5 km, capped 1 to 16 km
    distance = round(float(np.clip(np.random.lognormal(mean=1.35, sigma=0.45), 1.0, 16.0)), 1)
    
    # Order Value (INR): between 180 and 1600 depending on tier & cuisine
    base_val = random.randint(220, 950)
    if cust['loyalty_tier'] == 'Gold':
        base_val += random.randint(100, 350)
    order_val = float(round(base_val, 2))
    
    # Discount
    if cust['loyalty_tier'] == 'Gold':
        discount = round(order_val * random.uniform(0.10, 0.20), 2)
    elif cust['loyalty_tier'] == 'Silver':
        discount = round(order_val * random.uniform(0.05, 0.12), 2)
    else:
        discount = round(order_val * random.uniform(0.00, 0.08), 2) if random.random() > 0.5 else 0.0
    discount = min(discount, 250.0)
    
    # Delivery Fee: 25 base + distance scaling (free for Gold over 500)
    if cust['loyalty_tier'] == 'Gold' and order_val > 500:
        delivery_fee = 0.0
    else:
        delivery_fee = round(25.0 + max(0, distance - 3) * 5.0, 2)
    
    # Order Status: 93% Delivered, 5.5% Cancelled, 1.5% Returned/Refunded
    status_choice = np.random.choice(['Delivered', 'Cancelled', 'Returned'], p=[0.93, 0.055, 0.015])
    
    # Delivery Time Calculation (mins)
    # Base prep time (15 mins) + distance travel time (2.8 mins/km) + traffic factor + noise
    prep_time = random.uniform(12, 22)
    traffic_factor = 1.35 if (19 <= hour <= 21 or 12 <= hour <= 14) else 1.0
    travel_time = (distance * 2.8) * traffic_factor
    random_delay = np.random.exponential(scale=3.5)
    
    deliv_time = round(prep_time + travel_time + random_delay, 1)
    
    # Inject deliberate outliers for diagnostic & IQR detection
    if i in [142, 389, 715, 1102, 1450, 1789, 1920]:
        deliv_time = round(deliv_time + random.uniform(40, 55), 1)  # Extreme delay outlier
    
    if status_choice == 'Cancelled':
        deliv_time = np.nan
        cust_rating = np.nan
    else:
        # Customer rating diagnostic relationship:
        # If delivery time > 45 mins, probability of low rating (1-2) increases drastically
        if deliv_time > 50:
            rating_probs = [0.45, 0.30, 0.15, 0.07, 0.03]  # 1 to 5
        elif deliv_time > 40:
            rating_probs = [0.15, 0.25, 0.35, 0.18, 0.07]
        else:
            rating_probs = [0.03, 0.07, 0.15, 0.40, 0.35]
        cust_rating = int(np.random.choice([1, 2, 3, 4, 5], p=rating_probs))
        
    payment = random.choice(PAYMENT_METHODS)
    
    # Platform Revenue = (Order_Value * Commission) + Delivery_Fee
    # Delivery Partner Payout = Delivery_Fee * 0.85 + base incentive
    platform_revenue = round((order_val * commission_pct) + (delivery_fee * 0.25), 2)
    
    orders.append({
        'order_id': order_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'order_time': order_time_str,
        'customer_id': cust_id,
        'restaurant_id': rest_id,
        'partner_id': partner_id,
        'city': city,
        'cuisine_category': cuisine,
        'order_value': order_val,
        'discount_amount': discount,
        'delivery_fee': delivery_fee,
        'platform_commission_pct': commission_pct,
        'platform_revenue': platform_revenue,
        'delivery_distance_km': distance,
        'delivery_time_mins': deliv_time,
        'payment_method': payment,
        'order_status': status_choice,
        'customer_rating': cust_rating
    })
    
    # Generate 1 to 3 order items for relational Order_Items table
    num_items = random.randint(1, 3)
    item_val_share = order_val / num_items
    for it in range(num_items):
        order_items.append({
            'item_id': f"ITM{item_counter:05d}",
            'order_id': order_id,
            'item_name': f"{cuisine} Special Item {it+1}",
            'quantity': random.randint(1, 2),
            'item_price': round(item_val_share, 2)
        })
        item_counter += 1

df_clean_orders = pd.DataFrame(orders)
df_order_items = pd.DataFrame(order_items)

# Save Master & Order Items Tables
df_customers.to_csv(os.path.join(DATA_DIR, 'customers.csv'), index=False)
df_restaurants.to_csv(os.path.join(DATA_DIR, 'restaurants.csv'), index=False)
df_partners.to_csv(os.path.join(DATA_DIR, 'delivery_partners.csv'), index=False)
df_order_items.to_csv(os.path.join(DATA_DIR, 'order_items.csv'), index=False)

# Save Clean Primary Dataset
df_clean_orders.to_csv(os.path.join(DATA_DIR, 'cleaned_food_orders.csv'), index=False)
# Also copy to legacy food_orders.csv to satisfy any legacy reference
df_clean_orders.to_csv(os.path.join(DATA_DIR, 'food_orders.csv'), index=False)

# 3. Create RAW Dataset with Realistic Data Quality Flaws (for Cleaning Demonstration)
# We duplicate ~10 records, add trailing spaces, introduce casing inconsistencies, and minor NaN fields.
df_raw = df_clean_orders.copy()

# Add 8 duplicate rows
duplicates = df_raw.sample(8, random_state=42)
df_raw = pd.concat([df_raw, duplicates], ignore_index=True)

# Add casing inconsistencies in 'city' and trailing whitespace
for idx in [5, 12, 45, 90, 150]:
    df_raw.loc[idx, 'city'] = df_raw.loc[idx, 'city'].lower() + "  "

for idx in [88, 210, 440]:
    df_raw.loc[idx, 'payment_method'] = df_raw.loc[idx, 'payment_method'].upper()

# Add a few unrated completed orders (simulating customer skipping review)
for idx in [20, 55, 112, 305, 520, 810]:
    if df_raw.loc[idx, 'order_status'] == 'Delivered':
        df_raw.loc[idx, 'customer_rating'] = np.nan

df_raw.to_csv(os.path.join(DATA_DIR, 'raw_food_orders.csv'), index=False)

print(f"Data generation complete!")
print(f"Total Clean Orders: {len(df_clean_orders)}")
print(f"Total Raw Orders (with duplicates): {len(df_raw)}")
print(f"Total Customers: {len(df_customers)}")
print(f"Total Restaurants: {len(df_restaurants)}")
print(f"Total Delivery Partners: {len(df_partners)}")
print(f"Total Order Items: {len(df_order_items)}")
