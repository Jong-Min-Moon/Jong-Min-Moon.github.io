---
layout: distill
title: "Time Series Operations in Pandas"
description: "A collection of useful pandas snippets for time series analysis, including date filtering, period conversion, and merging by nearest match."
date: 2025-12-18
categories: database
tags: pandas python time-series leetcode
project: database
---

# Time Series Operations in Pandas

Handling time-series data efficiently is a core skill for data analysis. Whether you are filtering by year, converting to specific periods, or performing asynchronous joins, `pandas` provides a robust set of tools. Below are some common patterns and techniques, often encountered in database-style coding challenges.

# Format change

## to string: .dt.strftime('%Y-%m-%d')
- **str**ing **f**ormat **time** : .dt.strftime('%Y-%m-%d')

### Leetcode 615: Average Salary: Departments VS Company
- need to change paydate column into paymonth column
```python
   df['pay_month'] = df['pay_date'].dt.strftime('%Y-%m')
```

## 1. Date Filtering and Extraction

Extracting parts of a date or filtering by specific time components is frequent in reporting.

- **Extracting Year (LeetCode 1890):**
  Use the `.dt` accessor to reach datetime properties.
  ```python
  df.query('timestamp.dt.year == 2020')
  ```

- **Converting to Period (LeetCode 1327):**
  When you need to match a specific month and year regardless of the day.
  ```python
  df[df['order_date'].dt.to_period('M') == '2020-02']
  ```

- **Range Filtering:**
  Standard tools for checking if dates fall within a specific window.
  - `pd.to_datetime()`: Converts strings or other formats to datetime objects.
  - `.between()`: Checks if values are within a range.
  - `pd.to_timedelta()`: Represents durations/differences in time.

---

## 2. Advanced Merging and Analysis

### [1251. Average Selling Price](https://leetcode.com/problems/average-selling-price/)
- **`merge_asof`**: This is powerful for "nearest match" joins. Unlike a standard join that requires exact matches, `merge_asof` aligns data based on the closest key (e.g., matching a transaction date to the price active at that time).
- **Handling Nulls**: When dividing (e.g., total price / total units), various nulls or `NaN` values may appear if some products had no sales. Always handle these or avoid dividing by zero using `.fillna(0)` or similar logic.

### [197. Rising Temperature](https://leetcode.com/problems/rising-temperature/)
To compare a value with "yesterday's" value, you can merge the table with itself using a calculated date offset.
- **Timedelta**: `pd.to_timedelta(1, unit='D')` adds or subtracts one day.
- **Suffixes**: Use `suffixes=('_today', '_yesterday')` in `pd.merge()` to keep the columns distinguishable.
- **Conversion**: Ensure keys are datetime objects using `pd.to_datetime()`.

---

## 3. Filtering by Aggregation

### [1084. Sales Analysis III](https://leetcode.com/problems/sales-analysis-iii/)
Sometimes you need to filter groups based on whether *all* their records fall within a certain range.

```python
start_time = pd.to_datetime('2019-01-01')
end_time = pd.to_datetime('2019-03-31')

# Filter groups where the entire date range is within the window
df.groupby('product_id').filter(
    lambda x: x['sale_date'].min() >= start_time and x['sale_date'].max() <= end_time
)
```

This approach ensures that products sold strictly within the first quarter are selected, excluding any that had sales outside that period.
