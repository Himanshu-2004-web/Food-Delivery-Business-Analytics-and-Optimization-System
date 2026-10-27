# Food Delivery Business Analytics and Performance Optimization System
**Business Analytics Mini Project | Academic Year 2025–2026**

![Project Status](https://img.shields.io/badge/Project_Status-Clean_&_Production_Ready-success)
![Technology](https://img.shields.io/badge/Tech_Stack-MySQL_|_Python_|_Excel_|_HTML5_Dashboard-blue)
![Analytics](https://img.shields.io/badge/Analytics-Descriptive_|_Diagnostic_|_Predictive_|_Prescriptive-orange)

An end-to-end, intermediate-level Business Analytics system evaluating **2,000 multi-city food delivery orders** across 5 metropolitan hubs (Bangalore, Mumbai, Delhi NCR, Hyderabad, Pune). 

The system operates on an integrated **Production Analytics Architecture**:
1. 🗄️ **MySQL Relational Backend:** Production relational schema (`food_delivery_db`), 5 normalized tables with Foreign Key constraints, indexes, views, and 11 analytical queries.
2. 📊 **Microsoft Excel Dashboard:** Deep spreadsheet modeling, dynamic logical formulas (`IF`, `AND`, `OR`, `VLOOKUP`), and statistical IQR outlier calculation.
3. 🐍 **Python Analytics Engine:** Preprocessing, statistical computing, correlation diagnostics ($r = -0.424$), 3-Month Moving Average Demand Forecast, and publication charts.
4. ⚡ **Interactive Web Dashboard (`dashboard.html`):** Standalone zero-setup UI with real-time filters, animations, and Chart.js visualizations that opens with a single double-click.

---

## 📁 Clean Project Architecture

```
Food_Delivery_Analytics/
├── sql/
│   ├── 01_schema.sql                  <- MySQL DDL (Database food_delivery_db, 5 tables, PK/FK, indexes)
│   ├── 02_seed_data.sql               <- Batch INSERT statements for all 2,000 orders & master records
│   ├── 03_analytical_queries.sql      <- 11 business intelligence queries (KPIs, city rank, delays, RFM)
│   └── 04_views_and_procedures.sql    <- Unified order view (vw_order_details), KPI view, & stored procedures
├── data/
│   ├── raw_food_orders.csv            <- Raw operational dataset (2,008 rows with duplicates & noise)
│   ├── cleaned_food_orders.csv        <- Cleaned primary dataset (2,000 verified rows)
│   ├── food_orders.csv                <- Primary dataset mirror
│   ├── customers.csv                  <- Customer Master (300 records with loyalty tiers & demographics)
│   ├── restaurants.csv                <- Restaurant Master (20 partner brands with commission rates)
│   ├── delivery_partners.csv          <- Delivery Partner Master (30 riders with vehicles & ratings)
│   └── order_items.csv                <- Granular Order Item breakdown (3,994 line items)
├── excel/
│   └── food_delivery_analysis.xlsx    <- Full Excel workbook (Executive Dashboard, IQR stats, Pivots & formulas)
├── output/
│   ├── charts/
│   │   ├── monthly_order_trend.png               <- Monthly orders & revenue trend
│   │   ├── city_performance_comparison.png       <- City-wise revenue benchmark
│   │   ├── delivery_time_outliers_boxplot.png     <- IQR outlier detection boxplot
│   │   ├── customer_rating_distribution.png      <- Customer review breakdown
│   │   ├── rating_vs_delay_diagnostic.png        <- Speed bracket vs rating degradation
│   │   └── peak_hour_demand_heatmap.png          <- Hourly demand heatmap across days of week
│   ├── summary_kpis.json             <- Machine-readable executive KPI dictionary
│   ├── descriptive_stats.csv         <- Formatted statistical measures & IQR thresholds
│   └── business_recommendations.txt  <- 6 actionable prescriptive strategies
├── scripts/
│   ├── generate_data.py               <- Reproducible dataset generator
│   ├── build_sql_backend.py           <- Compiles SQL seed scripts from CSV datasets
│   ├── load_to_mysql.py               <- Automated CLI MySQL loader
│   ├── build_excel_workbook.py        <- Automated openpyxl workbook builder
│   └── build_web_dashboard.py         <- Standalone animated HTML dashboard compiler
├── analysis.py                        <- Python analytics pipeline (Descriptive, Diagnostic, Predictive, Prescriptive)
├── dashboard.html                     <- Standalone Interactive Web Dashboard (Zero setup, double-click to run)
├── PROJECT_REPORT.md                  <- Academic Project Report
├── VIVA_QUESTIONS.md                  <- 25+ Viva Voce questions & model answers
└── README.md                          <- Project overview & execution guide
```

---

## 🗄️ MySQL Database Setup Guide (MySQL Workbench)

### Database Details:
- **Database Name:** `food_delivery_db`
- **Tables (5):**
  1. `customers` (Master customer demographics & loyalty tiers: 300 rows)
  2. `restaurants` (Partner restaurants with commission rates: 20 rows)
  3. `delivery_partners` (Fleet riders across vehicle types: 30 rows)
  4. `food_orders` (Fact table with 2,000 orders, order values, delivery times, ratings)
  5. `order_items` (Granular line-items: 3,994 rows)

### Step-by-Step in MySQL Workbench:
1. Open **MySQL Workbench** and connect to your local MySQL instance.
2. Click **File -> Open SQL Script...** (or press `Ctrl + O`).
3. Select [`sql/01_schema.sql`](file:///c:/Users/anshu/Desktop/Food_Delivery_Analytics/sql/01_schema.sql) and click the **⚡ (Execute)** button.
4. Next, open and execute [`sql/02_seed_data.sql`](file:///c:/Users/anshu/Desktop/Food_Delivery_Analytics/sql/02_seed_data.sql) to populate all 2,000 orders and master tables.
5. Open and execute [`sql/04_views_and_procedures.sql`](file:///c:/Users/anshu/Desktop/Food_Delivery_Analytics/sql/04_views_and_procedures.sql) to create analytical views (`vw_order_details`, `vw_city_kpi`) and stored procedures.
6. Open [`sql/03_analytical_queries.sql`](file:///c:/Users/anshu/Desktop/Food_Delivery_Analytics/sql/03_analytical_queries.sql) to run any of the 11 business intelligence queries.

*(Alternatively, run `python scripts/load_to_mysql.py` in your terminal to automate steps 3-5 in one go!)*

---

## 🚀 How to Run the Working Trio

### 1. View the Interactive Dashboard (Zero Commands Needed) 🌟
1. Open the folder: `C:\Users\anshu\Desktop\Food_Delivery_Analytics`
2. **Double-click `dashboard.html`** in your file explorer.
3. It opens immediately in Chrome or Edge with:
   - **4 Core Tabs:** Executive Dashboard, Diagnostic Analytics, Predictive Forecast, and Prescriptive Strategy.
   - **Interactive Control Bar:** Live City, Cuisine, and Order Status filters that update all charts and KPIs in real time.
   - **Modern UI/UX:** Clean styling, CSS animations, and zero third-party banners.

### 2. Run the Python Analytics Engine
To re-run the backend statistical computations, calculate correlation metrics, generate the 3-Month Moving Average forecast, and update the PNG chart files in `output/charts/`:
```bash
python analysis.py
```

### 3. Open the Microsoft Excel Workbook
Open [`excel/food_delivery_analysis.xlsx`](file:///c:/Users/anshu/Desktop/Food_Delivery_Analytics/excel/food_delivery_analysis.xlsx) to inspect:
- **`Executive_Dashboard` Sheet:** KPI summary cards, monthly trend chart, and city platform revenue chart.
- **`Cleaned_Orders` Sheet:** 2,000 orders with live formulas demonstrating `IF`, nested `IF`, `AND`, `OR`, `NOT`, `IFERROR`, `VLOOKUP`, and `CONCATENATE`.
- **`Statistical_Analysis` Sheet:** Mean, Median, Mode, Quartiles ($Q_1$, $Q_3$), IQR, and outlier thresholds.
- **`Pivot_Summaries` Sheet:** Multi-dimensional summaries across City, Cuisine, and Customer Loyalty Tiers.

---

## 📊 Core Business Metrics Summary

| Business Metric | Value | Business Definition & Interpretation |
| :--- | :---: | :--- |
| **Total Orders Placed** | **2,000** | Full order volume across the 12-month evaluation period. |
| **Delivered Orders** | **1,881** | Successfully fulfilled orders (**94.05% fulfillment rate**). |
| **Cancelled Orders** | **98** | Order cancellations (**4.90% cancellation rate**). |
| **Gross Merchandise Value (GMV)** | **₹12.41 Lakhs** | Total customer gross spend on food items. |
| **Net Platform Revenue** | **₹2.59 Lakhs** | Platform earnings from commission + delivery fees (**20.90% take rate**). |
| **Average Order Value (AOV)** | **₹620.50** | Mean transaction ticket size. |
| **Average Delivery Time** | **35.16 mins** | Door-to-door delivery latency (Median: **33.80 mins**). |
| **Average Customer Rating** | **3.65 / 5.0** | Overall customer satisfaction score. |
| **Statistical IQR Upper Bound** | **55.90 mins** | Statistical upper bound ($Q_3 + 1.5 \times \text{IQR}$) for normal delivery. |
| **Forecasting Accuracy (MAPE)** | **8.36%** | 3-Month Moving Average Demand Forecast evaluation error. |
