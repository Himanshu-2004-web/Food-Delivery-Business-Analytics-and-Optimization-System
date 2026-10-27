# Food Delivery Business Analytics System - Viva Voce Preparation Guide
**Comprehensive Q&A Defense Guide for University Evaluation**

This guide provides answers to anticipated questions covering Business Analytics concepts, Excel functions, MySQL queries, Python data analysis, statistical modeling, and business decision-making.

---

## Category 1: General Business Analytics Concepts

### Q1: What are the four types of analytics demonstrated in your project?
**Answer:**
1. **Descriptive Analytics (What happened?):** Summarizes historical performance. In our project, we calculated total order volume (2,000 orders), fulfillment rate (94.05%), Gross Merchandise Value (₹1,241,003.00), platform revenue (₹259,371.35), average delivery time (35.16 mins), and city market shares.
2. **Diagnostic Analytics (Why did it happen?):** Identifies root causes of trends. We investigated why ratings drop (Pearson $r = -0.424$ correlation between delivery time and ratings), identified distance degradation beyond 10 km (where ratings fall to 2.08), and uncovered dinner peak hour fleet shortages.
3. **Predictive Analytics (What will happen?):** Forecasts future outcomes using historical patterns. We built a 3-Month Moving Average model forecasting future monthly order demand with an evaluation MAPE of 8.36%.
4. **Prescriptive Analytics (What should we do?):** Formulates action plans and rules. We designed 5 rule-based operational interventions: peak-hour delivery surge bonuses, distance throttling to 8 km during rain, restaurant kitchen preparation SLAs, discount thresholding at ₹550, and automated credit refunds for orders exceeding the 55.9-minute IQR upper bound.

---

### Q2: What is the fundamental difference between Gross Merchandise Value (GMV) and Platform Revenue?
**Answer:**
- **Gross Merchandise Value (GMV):** The total value of merchandise sold through the platform by partner restaurants before discounts or fees. In our dataset:
  $$\text{GMV} = \sum \text{Order Value} = ₹1,241,003.00$$
- **Platform Revenue:** The actual revenue earned by the platform itself, consisting of merchant commission fees (15%–25%) plus delivery fee markups:
  $$\text{Platform Revenue} = \sum (\text{Order Value} \times \text{Commission \%}) + \text{Net Delivery Fee Cut} = ₹259,371.35$$
- **Take Rate:** The platform's monetization efficiency:
  $$\text{Take Rate} = \frac{\text{Platform Revenue}}{\text{GMV}} = \frac{₹259,371.35}{₹1,241,003.00} \approx 20.90\%$$
*Viva Tip:* Highlight that confusing GMV with Platform Revenue is a common rookie error; a company with ₹1 Crore in GMV may only earn ₹20 Lakhs in top-line revenue!

---

### Q3: Why is Correlation not equal to Causation in your diagnostic analysis?
**Answer:**
In our diagnostic analysis, we found a strong negative correlation ($r = -0.424$) between delivery time and customer rating. While this shows that higher delivery times are associated with lower customer ratings, correlation alone does not prove that delivery time was the sole cause of dissatisfaction. 

Other confounding variables—such as food being served cold, packaging spills, incorrect food items, or pre-existing customer mood—can also cause low ratings. Therefore, we state that delivery latency is a *statistically significant contributor*, but we avoid claiming sole causation without controlled experimental A/B testing.

---

## Category 2: Microsoft Excel Technical Questions

### Q4: Which logical and lookup formulas did you implement in Excel, and for what business purpose?
**Answer:**
1. **`VLOOKUP`:** Retrieves customer loyalty tier dynamically from the master Customers sheet into each order row (`=VLOOKUP(D2, Customers!A:D, 4, FALSE)`).
2. **`CONCATENATE` / `&`:** Generates unique business tracking identifiers combining Order ID and City (`=CONCATENATE(A2, "-", G2)`).
3. **`IF` with `AND`:** Flags high-value fulfilled orders for special loyalty treatment (`=IF(AND(I2>600, P2="Delivered"), "High Value Delivered", "Standard")`).
4. **`IF` with `OR`:** Triggers high-risk alerts when delivery exceeds 50 minutes OR customer rating is $\le 2$ stars (`=IF(OR(N2>50, Q2<=2), "High Risk / Delayed", "Normal")`).
5. **`IF` with `NOT`:** Evaluates order fulfillment status (`=IF(NOT(P2="Cancelled"), "Fulfilled", "Cancelled")`).
6. **Nested `IF`:** Categorizes orders into speed brackets (`=IF(N2<=30, "Fast (<30m)", IF(N2<=45, "Moderate (30-45m)", "Delayed (>45m)"))`).
7. **`IFERROR`:** Safely handles null or unrated orders to avoid formula errors (`=IFERROR(Q2, 0)`).
8. **Summary Formulas:** Used `COUNTIF`, `COUNTIFS`, `SUMIF`, `AVERAGEIF`, and `AVERAGEIFS` to construct monthly and city-level summary cards.

---

### Q5: How did you implement the IQR Outlier Detection method in Excel?
**Answer:**
We used native Excel statistical functions:
1. First Quartile ($Q_1$): `=QUARTILE.INC(Cleaned_Orders!N2:N2001, 1)` $\rightarrow 28.90$ mins
2. Third Quartile ($Q_3$): `=QUARTILE.INC(Cleaned_Orders!N2:N2001, 3)` $\rightarrow 39.70$ mins
3. Interquartile Range (IQR): `=Q3_cell - Q1_cell` $\rightarrow 10.80$ mins
4. Lower Threshold: `=Q1 - (1.5 * IQR)` $\rightarrow 12.70$ mins
5. Upper Threshold: `=Q3 + (1.5 * IQR)` $\rightarrow 55.90$ mins
6. Count of Delay Outliers: `=COUNTIF(Cleaned_Orders!N2:N2001, ">" & Upper_Bound_Cell)` $\rightarrow 55$ orders.

---

### Q6: Why did you use the IQR method instead of the Z-score (Standard Deviation) method for detecting delivery outliers?
**Answer:**
Delivery time data is non-normally distributed and exhibits a right-skewed tail (due to extreme traffic jams and monsoons). 
- The **Z-score method** relies on the mean and standard deviation, both of which are themselves heavily distorted by extreme outliers.
- The **IQR method** relies on quartiles (medians), which are robust statistics and resistant to extreme values. Hence, IQR provides a more realistic operational threshold (55.9 minutes) for non-symmetric real-world delivery data.

---

## Category 3: MySQL & Relational Database Design

### Q7: Describe your database schema and the integrity constraints used.
**Answer:**
We created a 3rd Normal Form (3NF) relational database (`food_delivery_db`) consisting of 5 tables:
- `Customers` (PK: `customer_id`)
- `Restaurants` (PK: `restaurant_id`)
- `Delivery_Partners` (PK: `partner_id`)
- `Orders` (PK: `order_id`, FKs referencing `Customers`, `Restaurants`, `Delivery_Partners` with `ON DELETE CASCADE`)
- `Order_Items` (PK: `item_id`, FK referencing `Orders`)

**Integrity Constraints Applied:**
- `NOT NULL` on mandatory business fields (dates, IDs, amounts).
- `CHECK` constraints on ratings (`CHECK (avg_rating BETWEEN 1.0 AND 5.0)`), ages (`CHECK (age >= 18)`), and values (`CHECK (order_value >= 0)`).
- `ENUM` data types to enforce allowed domain values for `loyalty_tier`, `vehicle_type`, and `order_status`.
- Performance indexes on frequently queried columns: `order_date`, `city`, and `order_status`.

---

### Q8: What is the difference between `WHERE` and `HAVING` in SQL, and where did you use both?
**Answer:**
- **`WHERE`:** Filters individual records *before* aggregation occurs.
- **`HAVING`:** Filters grouped aggregations *after* the `GROUP BY` operation.
- **Example in our project:**
  ```sql
  SELECT r.restaurant_name, COUNT(o.order_id) AS total_orders, AVG(o.customer_rating) AS avg_rating
  FROM Restaurants r
  JOIN Orders o ON r.restaurant_id = o.restaurant_id
  WHERE o.order_status = 'Delivered'       -- WHERE filters rows before grouping
  GROUP BY r.restaurant_name
  HAVING total_orders >= 50 AND avg_rating < 3.8;  -- HAVING filters the aggregated summary
  ```

---

### Q9: What is a Common Table Expression (CTE) and why did you use it?
**Answer:**
A CTE (defined using the `WITH` keyword) creates a named temporary result set that exists only within the execution scope of a single query. 
We used a CTE to build a multi-level restaurant operational efficiency matrix:
The CTE first aggregated order volumes, average delivery times, and revenues per restaurant. The outer query then used a `CASE` statement over the CTE columns to classify partners into 'Gold Standard Partner', 'Consistent Performer', or 'Critical Attention Required'. CTEs make complex analytical SQL queries modular and much easier to read than nested subqueries.

---

### Q10: How did you implement DML updates in SQL for performance tracking?
**Answer:**
We demonstrated both DDL (`ALTER TABLE`) and DML (`UPDATE`):
1. First, we added an operational tracking column:
   ```sql
   ALTER TABLE Orders ADD COLUMN is_delayed TINYINT(1) DEFAULT 0;
   ```
2. Then, we ran a conditional DML update to flag all orders that breached the 45-minute service threshold:
   ```sql
   UPDATE Orders 
   SET is_delayed = 1 
   WHERE delivery_time_mins > 45.00;
   ```
3. Finally, we verified the result by querying average customer satisfaction for delayed vs on-time deliveries.

---

## Category 4: Python & Statistical Modeling

### Q11: What was the purpose of your Python script (`analysis.py`)?
**Answer:**
`analysis.py` serves as the automated data science and analytical engine. It handles:
1. Ingestion of the cleaned data and feature engineering (extracting hour, day of week, time windows).
2. Descriptive KPI calculation.
3. Statistical calculations (Mean, Median, Mode, Standard Deviation, Quartiles, and IQR outlier boundaries).
4. Diagnostic hypothesis testing (Pearson correlation between delay and ratings).
5. 3-Month Moving Average Demand Forecasting and accuracy evaluation.
6. Execution of 5 prescriptive optimization rules.
7. Automated generation and export of 6 publication-grade visualization charts and JSON/CSV summary files.

---

### Q12: How did you choose and evaluate your Predictive Analytics model?
**Answer:**
- **Model Chosen:** 3-Month Simple Moving Average (SMA).
- **Reason:** In business analytics, models should balance interpretability with practical utility. For monthly aggregate order demand across a 12-month period, an explainable moving average provides an intuitive baseline without overfitting or requiring complex external features.
- **Evaluation Metrics Used:**
  - **Mean Absolute Error (MAE):** Average magnitude of forecast error:
    $$\text{MAE} = \frac{1}{n} \sum |Y_t - \hat{Y}_t| = 12.89 \text{ orders}$$
  - **Mean Absolute Percentage Error (MAPE):** Relative percentage error:
    $$\text{MAPE} = \frac{1}{n} \sum \left|\frac{Y_t - \hat{Y}_t}{Y_t}\right| \times 100 = 8.36\%$$
- A MAPE of 8.36% (well below the industry threshold of 10%) confirms that the baseline model is highly reliable for capacity planning.

---

### Q13: What data cleaning steps did you demonstrate between the raw and cleaned datasets?
**Answer:**
Real-world data is inherently dirty. We created both `raw_food_orders.csv` (2,008 records) and `cleaned_food_orders.csv` (2,000 records) to demonstrate:
1. **Deduplication:** Identified and removed 8 duplicate order records using pandas `drop_duplicates()` and Excel Remove Duplicates.
2. **Text Standardization & Trimming:** Cleaned leading and trailing whitespace in city names and normalized casing (e.g., standardizing "bangalore  " and "BANGALORE" to "Bangalore").
3. **Missing Value Treatment:** Identified unrated deliveries (where customers opted out of rating) versus cancelled orders (where delivery time and rating are legitimately null). We used `IFERROR` in Excel and vectorized `.fillna()` / `.dropna()` in Python.
4. **Data Type Casting:** Ensured order dates and order times were properly converted to datetime objects rather than raw strings.

---

## Category 5: Business Insights & Viva Defense Strategy

### Q14: Summarize the top 3 actionable business recommendations from your project.
**Answer:**
1. **Peak Hour Fleet Rebalancing:** Deploy 20%–25% surge partner incentives in Bangalore and Mumbai during the dinner window (19:00–21:30), where 16.1% of orders currently experience late deliveries.
2. **Distance Radius Throttling:** Enforce an 8 km delivery radius cap during monsoons and peak rush hours; our diagnostics proved deliveries over 10 km take an average of 60.6 minutes and crash customer satisfaction to 2.08 stars.
3. **Margin Protection on Free Delivery:** Raise the minimum order value threshold for free delivery subsidies to ₹550; delivering low-ticket orders (< ₹300) with free delivery erodes over 40% of platform commission.

---

### Q15: How did you ensure data consistency across Excel, SQL, and Python?
**Answer:**
We built a cross-validation test suite verifying that all primary metrics match 100%:
- Total Orders: 2,000
- Delivered Orders: 1,881
- Cancelled Orders: 98
- GMV: ₹1,241,003.00
- Platform Revenue: ₹259,371.35
- Average Delivery Time: 35.16 mins
- IQR Outlier Count: Exactly 55 orders (> 55.9 mins) across Excel formulas, MySQL queries, and Python numpy arrays.
This ensures there is zero discrepancies or fabricated numbers across the deliverables.
