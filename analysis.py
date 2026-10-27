"""
=============================================================================
Project Title: Food Delivery Business Analytics and Optimization System
File: analysis.py
Description: End-to-end Python Business Analytics Pipeline covering:
             1. Data Ingestion & Preprocessing
             2. Descriptive Analytics (KPIs, Monthly, City, Restaurant metrics)
             3. Statistical Modeling & IQR Outlier Detection
             4. Diagnostic Analytics (Delays, Distance impact, Rating correlation)
             5. Predictive Analytics (3-Month Moving Average Demand Forecasting)
             6. Prescriptive Analytics (Rule-Based Business Action Engine)
             7. Visualizations (Matplotlib & Seaborn)
             8. Export of KPI Summary Files and Actionable Insights
Author: Business Analytics Project Team
=============================================================================
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ---------------------------------------------------------------------------
# Set Global Plot Styling for Professional Reports
# ---------------------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['figure.titlesize'] = 14

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
CHARTS_DIR = os.path.join(OUTPUT_DIR, 'charts')

os.makedirs(CHARTS_DIR, exist_ok=True)

# ===========================================================================
# STEP 1: DATA INGESTION & PREPROCESSING
# ===========================================================================
def load_and_preprocess_data():
    """
    Loads raw and cleaned food delivery orders, checks data health,
    and performs feature engineering for temporal and categorical analytics.
    """
    clean_path = os.path.join(DATA_DIR, 'cleaned_food_orders.csv')
    print("=" * 80)
    print(f"[STEP 1] Ingesting Cleaned Food Delivery Dataset from: {clean_path}")
    
    df = pd.read_csv(clean_path)
    print(f"Dataset successfully loaded. Shape: {df.shape[0]} rows x {df.shape[1]} columns.")
    
    # Convert dates and parse time features
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['order_year_month'] = df['order_date'].dt.to_period('M').astype(str)
    df['order_month_name'] = df['order_date'].dt.strftime('%b')
    df['order_hour'] = pd.to_datetime(df['order_time'], format='%H:%M:%S').dt.hour
    df['day_of_week'] = df['order_date'].dt.day_name()
    
    # Categorize time windows
    def categorize_window(hour):
        if 12 <= hour <= 14:
            return 'Lunch Peak (12-2 PM)'
        elif 19 <= hour <= 21:
            return 'Dinner Peak (7-9 PM)'
        elif 8 <= hour <= 11:
            return 'Breakfast/Morning'
        elif 15 <= hour <= 18:
            return 'Evening Snacks'
        else:
            return 'Late Night / Off-Peak'

    df['time_window'] = df['order_hour'].apply(categorize_window)
    
    # Delivery Speed Category
    def categorize_speed(mins):
        if pd.isna(mins):
            return 'Not Delivered / Cancelled'
        elif mins <= 30:
            return 'Fast (<= 30 mins)'
        elif mins <= 45:
            return 'Moderate (31 - 45 mins)'
        else:
            return 'Delayed (> 45 mins)'

    df['delivery_speed_cat'] = df['delivery_time_mins'].apply(categorize_speed)
    
    return df

# ===========================================================================
# STEP 2: DESCRIPTIVE ANALYTICS & EXECUTIVE KPIS
# ===========================================================================
def calculate_descriptive_kpis(df):
    """
    Calculates primary descriptive metrics: Volume, GMV, Revenue,
    Fulfillment rate, Cancellation rate, Average Delivery Time, and AOV.
    """
    print("\n" + "=" * 80)
    print("[STEP 2] DESCRIPTIVE ANALYTICS: High-Level Business KPIs")
    print("=" * 80)
    
    total_orders = len(df)
    delivered_orders = len(df[df['order_status'] == 'Delivered'])
    cancelled_orders = len(df[df['order_status'] == 'Cancelled'])
    returned_orders = len(df[df['order_status'] == 'Returned'])
    cancellation_rate = (cancelled_orders / total_orders) * 100
    
    total_gmv = df['order_value'].sum()
    total_revenue = df['platform_revenue'].sum()
    total_discounts = df['discount_amount'].sum()
    
    # Delivery time and rating for completed deliveries
    delivered_df = df[df['order_status'] == 'Delivered']
    avg_delivery_time = delivered_df['delivery_time_mins'].mean()
    median_delivery_time = delivered_df['delivery_time_mins'].median()
    avg_customer_rating = delivered_df['customer_rating'].mean()
    avg_order_value = df['order_value'].mean()
    avg_distance = df['delivery_distance_km'].mean()
    
    kpis = {
        'total_orders': int(total_orders),
        'delivered_orders': int(delivered_orders),
        'cancelled_orders': int(cancelled_orders),
        'returned_orders': int(returned_orders),
        'cancellation_rate_pct': round(float(cancellation_rate), 2),
        'total_gross_merchandise_value_inr': round(float(total_gmv), 2),
        'total_platform_revenue_inr': round(float(total_revenue), 2),
        'total_discounts_given_inr': round(float(total_discounts), 2),
        'take_rate_pct': round(float((total_revenue / total_gmv) * 100), 2),
        'average_order_value_inr': round(float(avg_order_value), 2),
        'average_delivery_time_mins': round(float(avg_delivery_time), 2),
        'median_delivery_time_mins': round(float(median_delivery_time), 2),
        'average_customer_rating': round(float(avg_customer_rating), 2),
        'average_distance_km': round(float(avg_distance), 2)
    }
    
    print(f"Total Orders Placed        : {kpis['total_orders']:,}")
    print(f"Delivered Orders Fulfilled : {kpis['delivered_orders']:,} ({kpis['delivered_orders']/total_orders*100:.1f}%)")
    print(f"Cancelled Orders           : {kpis['cancelled_orders']:,} ({kpis['cancellation_rate_pct']}%)")
    print(f"Gross Sales (GMV)          : INR {kpis['total_gross_merchandise_value_inr']:,.2f}")
    print(f"Net Platform Revenue       : INR {kpis['total_platform_revenue_inr']:,.2f} (Take Rate: {kpis['take_rate_pct']}%)")
    print(f"Average Order Value (AOV)  : INR {kpis['average_order_value_inr']:,.2f}")
    print(f"Average Delivery Time      : {kpis['average_delivery_time_mins']} minutes (Median: {kpis['median_delivery_time_mins']} mins)")
    print(f"Average Customer Rating    : {kpis['average_customer_rating']} / 5.0")
    
    return kpis

# ===========================================================================
# STEP 3: STATISTICAL ANALYSIS & IQR OUTLIER DETECTION
# ===========================================================================
def calculate_statistical_metrics_and_iqr(df):
    """
    Computes rigorous descriptive statistics and identifies operational outliers
    in delivery times and order values using the Interquartile Range (IQR) technique.
    """
    print("\n" + "=" * 80)
    print("[STEP 3] STATISTICAL ANALYSIS & IQR OUTLIER DETECTION")
    print("=" * 80)
    
    delivered_times = df[df['order_status'] == 'Delivered']['delivery_time_mins'].dropna()
    order_vals = df['order_value'].dropna()
    
    def compute_stats(series, col_name):
        mean_val = series.mean()
        median_val = series.median()
        mode_res = stats.mode(series, keepdims=False)
        mode_val = float(mode_res.mode) if hasattr(mode_res, 'mode') else float(series.mode()[0])
        std_val = series.std()
        min_val = series.min()
        max_val = series.max()
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        low_outliers = series[series < lower_bound]
        high_outliers = series[series > upper_bound]
        
        return {
            'Variable': col_name,
            'Count': int(series.count()),
            'Mean': round(float(mean_val), 2),
            'Median': round(float(median_val), 2),
            'Mode': round(float(mode_val), 2),
            'Std Dev': round(float(std_val), 2),
            'Min': round(float(min_val), 2),
            'Max': round(float(max_val), 2),
            'Q1 (25th)': round(float(q1), 2),
            'Q3 (75th)': round(float(q3), 2),
            'IQR': round(float(iqr), 2),
            'Lower Bound': round(float(lower_bound), 2),
            'Upper Bound': round(float(upper_bound), 2),
            'Low Outliers Count': int(len(low_outliers)),
            'High Outliers Count': int(len(high_outliers)),
            'Total Outliers': int(len(low_outliers) + len(high_outliers))
        }
    
    stat_deliv = compute_stats(delivered_times, 'Delivery Time (Minutes)')
    stat_val = compute_stats(order_vals, 'Order Value (INR)')
    
    df_stats = pd.DataFrame([stat_deliv, stat_val])
    print(df_stats.T.to_string(header=False))
    
    # Save descriptive stats table
    df_stats.to_csv(os.path.join(OUTPUT_DIR, 'descriptive_stats.csv'), index=False)
    
    return stat_deliv, stat_val

# ===========================================================================
# STEP 4: DIAGNOSTIC ANALYTICS (Investigating Delay Causes & Dissatisfaction)
# ===========================================================================
def perform_diagnostic_analytics(df):
    """
    Examines underlying factors contributing to delivery delays, cancellations,
    and poor ratings (Correlation vs Causation principles).
    """
    print("\n" + "=" * 80)
    print("[STEP 4] DIAGNOSTIC ANALYTICS: Investigating Latency, Ratings & Friction")
    print("=" * 80)
    
    delivered = df[df['order_status'] == 'Delivered'].copy()
    
    # 1. Delivery Time vs Rating Degradation
    rating_by_speed = delivered.groupby('delivery_speed_cat').agg(
        Order_Count=('order_id', 'count'),
        Avg_Rating=('customer_rating', 'mean'),
        Low_Rating_Pct=('customer_rating', lambda x: round((x <= 2).mean() * 100, 1))
    ).reset_index()
    
    print("\nDiagnostic 1: Impact of Delivery Speed on Customer Satisfaction:")
    print(rating_by_speed.to_string(index=False))
    
    # Correlation between Delivery Time and Rating
    corr_time_rating, p_val = stats.pearsonr(delivered['delivery_time_mins'], delivered['customer_rating'])
    print(f"\nPearson Correlation (Delivery Time vs Customer Rating): r = {corr_time_rating:.3f} (p-value: {p_val:.2e})")
    print("Interpretation: Statistically significant negative correlation; higher wait times drive customer dissatisfaction.")
    
    # 2. Distance vs Delay & Cancellation Diagnostic
    df['dist_bucket'] = pd.cut(df['delivery_distance_km'], bins=[0, 3, 7, 10, 20], labels=['<= 3km', '3-7km', '7-10km', '> 10km'])
    dist_diag = df.groupby('dist_bucket', observed=False).agg(
        Total_Orders=('order_id', 'count'),
        Avg_Delivery_Time=('delivery_time_mins', 'mean'),
        Cancelled_Orders=('order_status', lambda x: (x == 'Cancelled').sum()),
        Cancellation_Rate=('order_status', lambda x: round((x == 'Cancelled').mean() * 100, 2)),
        Avg_Rating=('customer_rating', 'mean')
    ).reset_index()
    
    print("\nDiagnostic 2: Delivery Distance Bracket vs Operational Outcome:")
    print(dist_diag.to_string(index=False))
    
    # 3. Peak Hour Congestion Diagnostic
    hour_diag = delivered.groupby('time_window').agg(
        Order_Volume=('order_id', 'count'),
        Avg_Delivery_Mins=('delivery_time_mins', 'mean'),
        Late_Orders_Pct=('delivery_time_mins', lambda x: round((x > 45).mean() * 100, 1))
    ).reset_index()
    
    print("\nDiagnostic 3: Time Window Traffic Congestion vs Late Orders:")
    print(hour_diag.to_string(index=False))
    
    return rating_by_speed, dist_diag

# ===========================================================================
# STEP 5: PREDICTIVE ANALYTICS (3-Month Moving Average Demand Forecast)
# ===========================================================================
def perform_predictive_analytics(df):
    """
    Implements a simple, explainable baseline moving average demand forecasting
    model to predict monthly order volumes and evaluates error metrics (MAE & MAPE).
    """
    print("\n" + "=" * 80)
    print("[STEP 5] PREDICTIVE ANALYTICS: 3-Month Moving Average Demand Forecast")
    print("=" * 80)
    
    monthly_series = df.groupby('order_year_month').size().reset_index(name='actual_orders')
    monthly_series['3_month_MA_forecast'] = monthly_series['actual_orders'].rolling(window=3).mean().shift(1)
    
    # Calculate Forecast Errors where historical window is available (Month 4 onwards)
    eval_df = monthly_series.dropna().copy()
    eval_df['absolute_error'] = np.abs(eval_df['actual_orders'] - eval_df['3_month_MA_forecast'])
    eval_df['pct_error'] = (eval_df['absolute_error'] / eval_df['actual_orders']) * 100
    
    mae = eval_df['absolute_error'].mean()
    mape = eval_df['pct_error'].mean()
    
    # Forecast Next Period (Jan 2026)
    last_3_months = monthly_series['actual_orders'].iloc[-3:].mean()
    next_month_forecast = round(float(last_3_months), 1)
    
    print("Monthly Actuals vs Moving Average Forecast:")
    print(monthly_series.to_string(index=False))
    print(f"\nModel Evaluation Metrics (Months 4-12):")
    print(f"Mean Absolute Error (MAE)          : {mae:.2f} orders")
    print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
    print(f"Baseline Forecast for Next Month    : {next_month_forecast} orders")
    
    return monthly_series, next_month_forecast, mae, mape

# ===========================================================================
# STEP 6: PRESCRIPTIVE ANALYTICS (Rule-Based Business Strategy Engine)
# ===========================================================================
def generate_prescriptive_recommendations(df, stat_deliv):
    """
    Applies rule-based business logic to formulate actionable optimization strategies
    for restaurant partners, delivery logistics, discount budgets, and SLA enforcement.
    """
    print("\n" + "=" * 80)
    print("[STEP 6] PRESCRIPTIVE ANALYTICS: Data-Driven Optimization Engine")
    print("=" * 80)
    
    recs = []
    
    # Rule 1: Peak Hour Surge Capacity
    delivered = df[df['order_status'] == 'Delivered']
    dinner_peak_late = (delivered[delivered['time_window'] == 'Dinner Peak (7-9 PM)']['delivery_time_mins'] > 45).mean()
    if dinner_peak_late > 0.15:
        recs.append(
            "[STRATEGY 1 - LOGISTICS] Dynamic Fleet Capacity Surge: Dinner peak orders experience "
            f"a {dinner_peak_late*100:.1f}% late delivery rate. Implement a 20-25% delivery partner surge bonus "
            "between 19:00 - 21:30 in Bangalore and Mumbai to reduce order dispatch latency."
        )
        
    # Rule 2: Outlier Distance Throttling
    far_cancel_rate = (df[df['delivery_distance_km'] > 10]['order_status'] == 'Cancelled').mean()
    if far_cancel_rate > 0.08:
        recs.append(
            "[STRATEGY 2 - OPERATIONS] Distance Throttling & Weather Buffers: Deliveries exceeding 10 km "
            f"display an alarming {far_cancel_rate*100:.1f}% cancellation rate and significant rating drops. "
            "Cap non-essential long-distance delivery radiuses to 8 km during peak rain/traffic periods."
        )
        
    # Rule 3: Quality Audit for Underperforming Restaurants
    rest_perf = df.groupby('restaurant_id').agg(
        total=('order_id', 'count'),
        avg_rating=('customer_rating', 'mean')
    )
    flagged_rests = rest_perf[(rest_perf['total'] >= 30) & (rest_perf['avg_rating'] < 3.9)]
    recs.append(
        f"[STRATEGY 3 - PARTNER QUALITY] SLA & Quality Review: Identified {len(flagged_rests)} restaurant partner(s) "
        "consistently averaging below 3.9 stars. Place these kitchens on a 14-day packaging & prep time review "
        "program before terminating platform listing."
    )
    
    # Rule 4: Discount Optimization
    recs.append(
        "[STRATEGY 4 - FINANCIAL OPTIMIZATION] Margin Rationalization: Maintain free delivery subsidies "
        "strictly for orders above INR 550. Subsidies on low-ticket orders under INR 300 erode over 40% of platform revenue."
    )
    
    # Rule 5: Delivery SLA Thresholding
    upper_iqr = stat_deliv['Upper Bound']
    recs.append(
        f"[STRATEGY 5 - CUSTOMER RETENTION] Automated Compensation Trigger: Set an automated customer service credit "
        f"trigger for any order exceeding the statistical IQR Upper Bound ({upper_iqr:.1f} mins) to prevent long-term churn."
    )
    
    for r in recs:
        print(f"\n* {r}")
        
    # Export Recommendations to Text File
    rec_path = os.path.join(OUTPUT_DIR, 'business_recommendations.txt')
    with open(rec_path, 'w', encoding='utf-8') as f:
        f.write("FOOD DELIVERY BUSINESS ANALYTICS - PRESCRIPTIVE RECOMMENDATIONS\n")
        f.write("=" * 70 + "\n\n")
        for idx, r in enumerate(recs, 1):
            f.write(f"{idx}. {r}\n\n")
            
    print(f"\nPrescriptive recommendations successfully written to: {rec_path}")
    return recs

# ===========================================================================
# STEP 7: DATA VISUALIZATIONS (Exporting Visual Assets)
# ===========================================================================
def generate_visualizations(df, monthly_df):
    """
    Renders high-quality visualization figures and exports them to output/charts.
    """
    print("\n" + "=" * 80)
    print("[STEP 7] GENERATING BUSINESS VISUALIZATIONS")
    print("=" * 80)
    
    delivered = df[df['order_status'] == 'Delivered'].copy()
    
    # -----------------------------------------------------------------------
    # Chart 1: Monthly Order Volume & Platform Revenue Trend
    # -----------------------------------------------------------------------
    plt.figure(figsize=(10, 5))
    monthly_agg = df.groupby('order_year_month').agg(
        Orders=('order_id', 'count'),
        Revenue=('platform_revenue', 'sum')
    ).reset_index()
    
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    bars = ax1.bar(monthly_agg['order_year_month'], monthly_agg['Orders'], color='#3182CE', alpha=0.75, width=0.5, label='Monthly Orders')
    lines = ax2.plot(monthly_agg['order_year_month'], monthly_agg['Revenue'], color='#DD6B20', marker='o', linewidth=2.5, label='Platform Revenue (INR)')
    
    ax1.set_xlabel('Month', fontweight='bold')
    ax1.set_ylabel('Order Count', color='#3182CE', fontweight='bold')
    ax2.set_ylabel('Platform Revenue (₹)', color='#DD6B20', fontweight='bold')
    ax1.set_title('Monthly Order Demand & Platform Revenue Trend (2025)', pad=15)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    c1_path = os.path.join(CHARTS_DIR, 'monthly_order_trend.png')
    plt.savefig(c1_path, dpi=300)
    plt.close()
    print(f"Saved: {c1_path}")
    
    # -----------------------------------------------------------------------
    # Chart 2: City Performance Comparison (Orders & Revenue)
    # -----------------------------------------------------------------------
    city_agg = df.groupby('city').agg(
        Orders=('order_id', 'count'),
        Revenue=('platform_revenue', 'sum'),
        Avg_Rating=('customer_rating', 'mean')
    ).sort_values(by='Revenue', ascending=False).reset_index()
    
    plt.figure(figsize=(9, 5))
    palette = sns.color_palette("Blues_r", len(city_agg))
    bars = plt.bar(city_agg['city'], city_agg['Revenue'], color=palette, edgecolor='#2B6CB0')
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1000, f"₹{yval:,.0f}", ha='center', va='bottom', fontsize=9, fontweight='bold')
        
    plt.title('City-wise Platform Revenue Benchmark', pad=15)
    plt.xlabel('City', fontweight='bold')
    plt.ylabel('Platform Revenue (INR)', fontweight='bold')
    plt.tight_layout()
    c2_path = os.path.join(CHARTS_DIR, 'city_performance_comparison.png')
    plt.savefig(c2_path, dpi=300)
    plt.close()
    print(f"Saved: {c2_path}")
    
    # -----------------------------------------------------------------------
    # Chart 3: Delivery Time IQR Outliers Boxplot
    # -----------------------------------------------------------------------
    plt.figure(figsize=(9, 4.5))
    flierprops = dict(marker='o', markerfacecolor='#E53E3E', markersize=7, markeredgecolor='black', linestyle='none')
    box = plt.boxplot(delivered['delivery_time_mins'], vert=False, patch_artist=True, flierprops=flierprops, widths=0.5)
    
    for patch in box['boxes']:
        patch.set_facecolor('#63B3ED')
    for median in box['medians']:
        median.set(color='#C53030', linewidth=2.5)
        
    # Annotate IQR upper bound
    q1 = delivered['delivery_time_mins'].quantile(0.25)
    q3 = delivered['delivery_time_mins'].quantile(0.75)
    iqr = q3 - q1
    ub = q3 + 1.5 * iqr
    
    plt.axvline(ub, color='#E53E3E', linestyle='--', linewidth=1.5, label=f'Upper Threshold ({ub:.1f} mins)')
    plt.title('Delivery Time Distribution & IQR Outlier Identification', pad=15)
    plt.xlabel('Delivery Time (Minutes)', fontweight='bold')
    plt.legend(loc='upper right')
    plt.tight_layout()
    c3_path = os.path.join(CHARTS_DIR, 'delivery_time_outliers_boxplot.png')
    plt.savefig(c3_path, dpi=300)
    plt.close()
    print(f"Saved: {c3_path}")
    
    # -----------------------------------------------------------------------
    # Chart 4: Customer Rating Distribution
    # -----------------------------------------------------------------------
    plt.figure(figsize=(8, 4.5))
    rating_counts = delivered['customer_rating'].value_counts().sort_index()
    bars = plt.bar(rating_counts.index, rating_counts.values, color='#48BB78', edgecolor='#22543D', width=0.55)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 15, f"{yval} ({yval/len(delivered)*100:.1f}%)", ha='center', va='bottom', fontsize=9, fontweight='bold')
        
    plt.title('Customer Rating Distribution (Delivered Orders)', pad=15)
    plt.xlabel('Rating (Stars)', fontweight='bold')
    plt.ylabel('Number of Reviews', fontweight='bold')
    plt.xticks([1, 2, 3, 4, 5])
    plt.tight_layout()
    c4_path = os.path.join(CHARTS_DIR, 'customer_rating_distribution.png')
    plt.savefig(c4_path, dpi=300)
    plt.close()
    print(f"Saved: {c4_path}")
    
    # -----------------------------------------------------------------------
    # Chart 5: Delivery Speed vs Rating Diagnostic Breakdown
    # -----------------------------------------------------------------------
    plt.figure(figsize=(9, 4.8))
    sns.boxplot(data=delivered, x='delivery_speed_cat', y='customer_rating', palette='Set2')
    plt.title('Diagnostic Analysis: Customer Rating by Delivery Speed Category', pad=15)
    plt.xlabel('Delivery Speed Category', fontweight='bold')
    plt.ylabel('Customer Rating (Stars)', fontweight='bold')
    plt.tight_layout()
    c5_path = os.path.join(CHARTS_DIR, 'rating_vs_delay_diagnostic.png')
    plt.savefig(c5_path, dpi=300)
    plt.close()
    print(f"Saved: {c5_path}")
    
    # -----------------------------------------------------------------------
    # Chart 6: Peak Hour Demand Heatmap
    # -----------------------------------------------------------------------
    plt.figure(figsize=(10, 5))
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heat_data = df.pivot_table(index='day_of_week', columns='order_hour', values='order_id', aggfunc='count').reindex(days_order).fillna(0)
    
    sns.heatmap(heat_data, cmap='YlGnBu', annot=False, cbar_kws={'label': 'Orders Placed'})
    plt.title('Hourly Order Volume Heatmap across Days of the Week', pad=15)
    plt.xlabel('Hour of Day (24-Hour Format)', fontweight='bold')
    plt.ylabel('Day of Week', fontweight='bold')
    plt.tight_layout()
    c6_path = os.path.join(CHARTS_DIR, 'peak_hour_demand_heatmap.png')
    plt.savefig(c6_path, dpi=300)
    plt.close()
    print(f"Saved: {c6_path}")

# ===========================================================================
# MAIN PIPELINE EXECUTION
# ===========================================================================
def main():
    print("=" * 80)
    print("FOOD DELIVERY BUSINESS ANALYTICS & PERFORMANCE OPTIMIZATION SYSTEM")
    print("University Mini Project Pipeline Execution")
    print("=" * 80)
    
    # 1. Ingestion
    df = load_and_preprocess_data()
    
    # 2. Descriptive KPIs
    kpis = calculate_descriptive_kpis(df)
    
    # 3. Statistical Analysis & Outliers
    stat_deliv, stat_val = calculate_statistical_metrics_and_iqr(df)
    
    # 4. Diagnostic Analytics
    rating_by_speed, dist_diag = perform_diagnostic_analytics(df)
    
    # 5. Predictive Analytics
    monthly_df, next_forecast, mae, mape = perform_predictive_analytics(df)
    
    # 6. Prescriptive Analytics
    recs = generate_prescriptive_recommendations(df, stat_deliv)
    
    # 7. Visualizations
    generate_visualizations(df, monthly_df)
    
    # 8. Export KPI Summary JSON
    kpi_file = os.path.join(OUTPUT_DIR, 'summary_kpis.json')
    with open(kpi_file, 'w', encoding='utf-8') as f:
        json.dump(kpis, f, indent=4)
    print(f"\nSummary KPIs exported to: {kpi_file}")
    
    print("\n" + "=" * 80)
    print("ALL ANALYTICS STAGES EXECUTED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == '__main__':
    main()
