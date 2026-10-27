"""
Build SQL Backend Data Seeder:
Generates production-grade batch INSERT SQL statements from CSV files
for direct execution in MySQL Workbench or mysql CLI.
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR = os.path.join(BASE_DIR, 'sql')
os.makedirs(SQL_DIR, exist_ok=True)

SEED_FILE = os.path.join(SQL_DIR, '02_seed_data.sql')

def escape_sql_val(val):
    if pd.isna(val) or val is None:
        return "NULL"
    if isinstance(val, (int, np.integer)):
        return str(val)
    if isinstance(val, (float, np.floating)):
        return f"{val:.2f}"
    val_str = str(val).replace("'", "''")
    return f"'{val_str}'"

def generate_batch_inserts(df, table_name, batch_size=100):
    columns = list(df.columns)
    col_str = ", ".join([f"`{col}`" for col in columns])
    statements = []
    
    total_rows = len(df)
    for i in range(0, total_rows, batch_size):
        batch = df.iloc[i : i + batch_size]
        val_rows = []
        for _, row in batch.iterrows():
            formatted_vals = [escape_sql_val(row[col]) for col in columns]
            val_rows.append(f"    ({', '.join(formatted_vals)})")
        stmt = f"INSERT INTO `{table_name}` ({col_str}) VALUES\n" + ",\n".join(val_rows) + ";\n"
        statements.append(stmt)
    return "\n".join(statements)

def main():
    print("Reading CSV files from data directory...")
    df_customers = pd.read_csv(os.path.join(DATA_DIR, 'customers.csv'))
    df_restaurants = pd.read_csv(os.path.join(DATA_DIR, 'restaurants.csv'))
    df_partners = pd.read_csv(os.path.join(DATA_DIR, 'delivery_partners.csv'))
    df_orders = pd.read_csv(os.path.join(DATA_DIR, 'cleaned_food_orders.csv'))
    df_items = pd.read_csv(os.path.join(DATA_DIR, 'order_items.csv'))

    with open(SEED_FILE, 'w', encoding='utf-8') as f:
        f.write("-- =====================================================================\n")
        f.write("-- Food Delivery Analytics - Production Seed Data Script\n")
        f.write("-- Auto-generated from cleaned CSV datasets\n")
        f.write("-- =====================================================================\n\n")
        f.write("USE food_delivery_db;\n\n")
        f.write("SET FOREIGN_KEY_CHECKS = 0;\n")
        f.write("TRUNCATE TABLE `order_items`;\n")
        f.write("TRUNCATE TABLE `food_orders`;\n")
        f.write("TRUNCATE TABLE `delivery_partners`;\n")
        f.write("TRUNCATE TABLE `restaurants`;\n")
        f.write("TRUNCATE TABLE `customers`;\n")
        f.write("SET FOREIGN_KEY_CHECKS = 1;\n\n")

        print("Writing Customers seed data...")
        f.write("-- 1. Seed Customers (300 rows)\n")
        f.write(generate_batch_inserts(df_customers, 'customers', batch_size=100))
        f.write("\n")

        print("Writing Restaurants seed data...")
        f.write("-- 2. Seed Restaurants (20 rows)\n")
        f.write(generate_batch_inserts(df_restaurants, 'restaurants', batch_size=50))
        f.write("\n")

        print("Writing Delivery Partners seed data...")
        f.write("-- 3. Seed Delivery Partners (30 rows)\n")
        f.write(generate_batch_inserts(df_partners, 'delivery_partners', batch_size=50))
        f.write("\n")

        print("Writing Food Orders seed data...")
        f.write("-- 4. Seed Food Orders (2,000 rows)\n")
        f.write(generate_batch_inserts(df_orders, 'food_orders', batch_size=100))
        f.write("\n")

        print("Writing Order Items seed data...")
        f.write("-- 5. Seed Order Items (3,994 rows)\n")
        f.write(generate_batch_inserts(df_items, 'order_items', batch_size=100))
        f.write("\n")

    file_size_mb = os.path.getsize(SEED_FILE) / (1024 * 1024)
    print(f"Generated {SEED_FILE} successfully! Size: {file_size_mb:.2f} MB")

if __name__ == '__main__':
    main()
