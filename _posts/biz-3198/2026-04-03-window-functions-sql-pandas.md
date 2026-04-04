---
layout: distill
title: "Window Functions in SQL and Pandas"
description: "A practical guide to window functions—ranking, aggregation, and offset operations computed over a sliding frame—demonstrated side-by-side in SQL and Python's pandas library."
date: 2026-04-03
categories: biz-3198
tags: sql pandas python data-handling
project: biz-3198
---

# Window function = data analysis step

After the database server has completed all of the steps necessary to evaluate a query, including joining, filtering, grouping, and sorting, the result set is complete and ready to be returned to the caller. Imagine if you could pause the query execution at this point and take a walk through the result set while it is still held in memory; what types of analysis might you want to do? If your result set contains sales data, perhaps you might want to generate rankings for salespeople or regions, or calculate percentage differences between one time period and another. If you are generating results for a financial report, perhaps you would like to calculate subtotals for each report section, and a grand total for the final section. Using analytic functions, you can do all of these things and more.

Window functions let you compute aggregations, rankings, or offsets **across a set of rows that are related to the current row**—without collapsing the result into a single row the way `GROUP BY` does. They are one of the most powerful tools for data analysis in both SQL and pandas.


# df.rank()

`
DataFrame.rank(axis=0, method='average', numeric_only=False, na_option='keep', ascending=True, pct=False)
`

- rank is a window function: it does not collapse rows. 
- If just used, it ranks among all rows
- If used with groupby, it ranks among groups

## Key options

### method
- average: average rank of the group. can be float. e.g. rank 2.5 (think of 1.5tier journals)
- min: lowest rank in the group (think of equal contribution co autuors)
- max: highest rank in the group 
- first: ranks assigned in order they appear in the array
- dense: like ‘min’, but rank always increases by 1 between groups.

### ascending
- True: smallest values is rank 1 (think of running)
- False: largest values is rank 1. Think of test score or salary. This is more common.


## Leetcode 178: Rank Scores
This is a almost a tutorial for rank function.

```python
def order_scores(scores: pd.DataFrame) -> pd.DataFrame:
    scores['rank'] = scores['score'].rank(method = 'dense', ascending = False)
    return scores.sort_values(by = 'score', ascending = False)[['score', 'rank']]
```

## Leetcode 184: Department Highest salary

```python
def department_highest_salary(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    df = employee.merge(department, left_on='departmentId', right_on='id', how='left', suffixes=('_emp', '_dept'))
    df['rank'] = df.groupby('departmentId')['salary'].rank(method = 'min', ascending = False)
    return df[df['rank']==1][['name_dept', 'name_emp', 'salary']].rename(
        columns = {
            'name_dept' : 'Department',
            'name_emp' : 'Employee',
            'salary' : 'Salary'
        }
    )
```

## Leetcode 185: Department Top Three Salaries

```python
def top_three_salaries(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    df = employee.merge(department, how = 'left', left_on = 'departmentId', right_on = 'id', suffixes = ('_emp', '_dept'))
    df['salrank'] = df.groupby('departmentId')['salary'].rank(method = 'dense', ascending = False)
    return df[df['salrank']<=3][['name_dept', 'name_emp', 'salary']].rename(
        columns = {
            'name_dept' : 'Department',
            'name_emp' : 'Employee',
            'salary' : 'Salary'
        }
    )
```

## Leetcode 1875: Group Employees of the Same Salary
- groupby + transform is the window function in pandas
- copy is needed when we assign new columns after filtering
- sort_values with two columns!
```python
    employees['salary_count'] = employees.groupby('salary')['salary'].transform('size')
    filtered_employees = employees[employees['salary_count'] > 1].copy() #since we are assigning new columns after filtering...


    filtered_employees['team_id'] = filtered_employees['salary'].rank(method = 'dense').astype(int)
    return filtered_employees[['employee_id', 'name', 'salary', 'team_id']].sort_values(['team_id', 'employee_id'])
```

## 1. What Is a Window Function?

A **window** is a logically ordered subset of rows defined by:

- **PARTITION BY** — how to split the data into groups (like `GROUP BY`, but rows are kept separate).
- **ORDER BY** — how to sort rows within each partition.
- **Frame clause** — which rows relative to the current row are included (e.g., `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`).

The function is evaluated for every row over its window, and the original row is preserved in the output.

```
┌──────────────────────────────────────────────┐
│  Full table                                  │
│  ┌────────────┐  ┌────────────┐              │
│  │ Partition A│  │ Partition B│  ...         │
│  │  row 1     │  │  row 1     │              │
│  │  row 2  ←── current row    │              │
│  │  row 3     │  │  row 3     │              │
│  └────────────┘  └────────────┘              │
└──────────────────────────────────────────────┘
```

---

## 2. The Sample Dataset

We will use a simple sales table throughout:

| order_id | salesperson | region | sale_date  | amount |
| -------- | ----------- | ------ | ---------- | ------ |
| 1        | Alice       | East   | 2024-01-05 | 500    |
| 2        | Bob         | West   | 2024-01-07 | 300    |
| 3        | Alice       | East   | 2024-01-12 | 700    |
| 4        | Carol       | East   | 2024-01-15 | 450    |
| 5        | Bob         | West   | 2024-01-20 | 600    |
| 6        | Carol       | West   | 2024-01-22 | 200    |

**SQL — create & populate:**

```sql
CREATE TABLE sales (
    order_id    INT,
    salesperson VARCHAR(50),
    region      VARCHAR(50),
    sale_date   DATE,
    amount      INT
);

INSERT INTO sales VALUES
  (1, 'Alice', 'East', '2024-01-05', 500),
  (2, 'Bob',   'West', '2024-01-07', 300),
  (3, 'Alice', 'East', '2024-01-12', 700),
  (4, 'Carol', 'East', '2024-01-15', 450),
  (5, 'Bob',   'West', '2024-01-20', 600),
  (6, 'Carol', 'West', '2024-01-22', 200);
```

**Python — create DataFrame:**

```python
import pandas as pd

data = {
    "order_id":    [1, 2, 3, 4, 5, 6],
    "salesperson": ["Alice", "Bob", "Alice", "Carol", "Bob", "Carol"],
    "region":      ["East", "West", "East", "East", "West", "West"],
    "sale_date":   pd.to_datetime([
        "2024-01-05", "2024-01-07", "2024-01-12",
        "2024-01-15", "2024-01-20", "2024-01-22"
    ]),
    "amount":      [500, 300, 700, 450, 600, 200],
}
df = pd.DataFrame(data)
```

---

## 3. Ranking Functions

Ranking functions assign an ordinal position to each row within its partition.

| Function       | Behavior                                               |
| -------------- | ------------------------------------------------------ |
| `ROW_NUMBER()` | Unique sequential integer, no ties                     |
| `RANK()`       | Tied rows get the same rank; next rank skips           |
| `DENSE_RANK()` | Tied rows get the same rank; next rank does *not* skip |

### 3.1 SQL

```sql
SELECT
    salesperson,
    region,
    amount,
    ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) AS row_num,
    RANK()       OVER (PARTITION BY region ORDER BY amount DESC) AS rnk,
    DENSE_RANK() OVER (PARTITION BY region ORDER BY amount DESC) AS dense_rnk
FROM sales;
```

### 3.2 pandas

```python
df["row_num"] = (
    df.groupby("region")["amount"]
      .rank(method="first", ascending=False)
      .astype(int)
)

df["rnk"] = (
    df.groupby("region")["amount"]
      .rank(method="min", ascending=False)
      .astype(int)
)

df["dense_rnk"] = (
    df.groupby("region")["amount"]
      .rank(method="dense", ascending=False)
      .astype(int)
)

print(df[["salesperson", "region", "amount", "row_num", "rnk", "dense_rnk"]])
```

> **Key difference:** `rank(method="first")` → `ROW_NUMBER`, `rank(method="min")` → `RANK`, `rank(method="dense")` → `DENSE_RANK`.

---

## 4. Aggregate Window Functions

Aggregates like `SUM`, `AVG`, `MIN`, and `MAX` can be computed *over a window* so that you see both the individual row value and a group-level summary in the same result.

### 4.1 Running total and group total (SQL)

```sql
SELECT
    salesperson,
    region,
    sale_date,
    amount,
    -- total per region (no ORDER BY → whole partition)
    SUM(amount) OVER (PARTITION BY region) AS region_total,
    -- running total per region ordered by date
    SUM(amount) OVER (
        PARTITION BY region
        ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM sales;
```

### 4.2 Running total and group total (pandas)

```python
# Group total
df["region_total"] = df.groupby("region")["amount"].transform("sum")

# Running total — sort first, then cumsum within group
df_sorted = df.sort_values(["region", "sale_date"])
df_sorted["running_total"] = df_sorted.groupby("region")["amount"].cumsum()
```

### 4.3 Moving average over the last 3 rows (SQL)

```sql
SELECT
    salesperson,
    sale_date,
    amount,
    AVG(amount) OVER (
        ORDER BY sale_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3
FROM sales;
```

### 4.4 Moving average over the last 3 rows (pandas)

```python
df_sorted = df.sort_values("sale_date").reset_index(drop=True)
df_sorted["moving_avg_3"] = (
    df_sorted["amount"]
      .rolling(window=3, min_periods=1)
      .mean()
)
```

> `rolling(window=3)` corresponds to `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`. Use `min_periods=1` to avoid `NaN` at the start.

---

## 5. Offset Functions

Offset functions let you look at the value of another row **relative** to the current row—no self-join required.

| Function           | Description                                                |
| ------------------ | ---------------------------------------------------------- |
| `LAG(col, n)`      | Value of `col` from `n` rows *before* the current row      |
| `LEAD(col, n)`     | Value of `col` from `n` rows *after* the current row       |
| `FIRST_VALUE(col)` | Value of `col` from the *first* row in the partition/frame |
| `LAST_VALUE(col)`  | Value of `col` from the *last* row in the partition/frame  |

### 5.1 LAG and LEAD (SQL)

```sql
SELECT
    salesperson,
    sale_date,
    amount,
    LAG(amount,  1, 0) OVER (PARTITION BY salesperson ORDER BY sale_date) AS prev_amount,
    LEAD(amount, 1, 0) OVER (PARTITION BY salesperson ORDER BY sale_date) AS next_amount,
    amount - LAG(amount, 1, 0)
             OVER (PARTITION BY salesperson ORDER BY sale_date)           AS change
FROM sales;
```

### 5.2 LAG and LEAD (pandas)

```python
df_sorted = df.sort_values(["salesperson", "sale_date"])

df_sorted["prev_amount"] = (
    df_sorted.groupby("salesperson")["amount"].shift(1).fillna(0)
)
df_sorted["next_amount"] = (
    df_sorted.groupby("salesperson")["amount"].shift(-1).fillna(0)
)
df_sorted["change"] = df_sorted["amount"] - df_sorted["prev_amount"]
```

> `shift(1)` is `LAG(1)`, `shift(-1)` is `LEAD(1)`.

### 5.3 FIRST_VALUE and LAST_VALUE (SQL)

```sql
SELECT
    region,
    salesperson,
    sale_date,
    amount,
    FIRST_VALUE(amount) OVER (
        PARTITION BY region ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS first_sale,
    LAST_VALUE(amount) OVER (
        PARTITION BY region ORDER BY sale_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_sale
FROM sales;
```

### 5.4 FIRST_VALUE and LAST_VALUE (pandas)

```python
df_sorted = df.sort_values(["region", "sale_date"])

df_sorted["first_sale"] = df_sorted.groupby("region")["amount"].transform("first")
df_sorted["last_sale"]  = df_sorted.groupby("region")["amount"].transform("last")
```

---

## 6. NTILE — Bucketing Rows

`NTILE(n)` divides the ordered partition into `n` roughly equal buckets.

### 6.1 SQL

```sql
SELECT
    salesperson,
    amount,
    NTILE(3) OVER (ORDER BY amount DESC) AS bucket
FROM sales;
```

### 6.2 pandas

```python
df["bucket"] = pd.qcut(df["amount"], q=3, labels=[3, 2, 1]).astype(int)
```

> `pd.qcut` creates quantile-based buckets. Label `1` is assigned to the highest bucket to mimic SQL's descending order convention.

---

## 7. PERCENT_RANK and CUME_DIST

| Function         | Formula                        |
| ---------------- | ------------------------------ |
| `PERCENT_RANK()` | $(rank - 1) / (N - 1)$         |
| `CUME_DIST()`    | (number of rows ≤ current) / N |

### 7.1 SQL

```sql
SELECT
    salesperson,
    amount,
    PERCENT_RANK() OVER (ORDER BY amount) AS pct_rank,
    CUME_DIST()    OVER (ORDER BY amount) AS cume_dist
FROM sales;
```

### 7.2 pandas

```python
df["pct_rank"]  = df["amount"].rank(pct=False, method="min")
df["pct_rank"]  = (df["pct_rank"] - 1) / (len(df) - 1)

df["cume_dist"] = df["amount"].rank(pct=True, method="max")
```

---

## 8. Summary Cheat Sheet

| Operation       | SQL                                         | pandas                         |
| --------------- | ------------------------------------------- | ------------------------------ |
| Row number      | `ROW_NUMBER() OVER (...)`                   | `rank(method="first")`         |
| Rank            | `RANK() OVER (...)`                         | `rank(method="min")`           |
| Dense rank      | `DENSE_RANK() OVER (...)`                   | `rank(method="dense")`         |
| Group total     | `SUM() OVER (PARTITION BY ...)`             | `groupby().transform("sum")`   |
| Running total   | `SUM() OVER (ORDER BY ... ROWS ...)`        | `groupby().cumsum()`           |
| Moving avg      | `AVG() OVER (ROWS BETWEEN n PRECEDING ...)` | `rolling(window=n).mean()`     |
| Previous row    | `LAG(col, 1) OVER (...)`                    | `groupby().shift(1)`           |
| Next row        | `LEAD(col, 1) OVER (...)`                   | `groupby().shift(-1)`          |
| First in group  | `FIRST_VALUE(col) OVER (...)`               | `groupby().transform("first")` |
| Last in group   | `LAST_VALUE(col) OVER (...)`                | `groupby().transform("last")`  |
| Buckets         | `NTILE(n) OVER (...)`                       | `pd.qcut(..., q=n)`            |
| Percentile rank | `PERCENT_RANK() OVER (...)`                 | manual formula with `rank()`   |
| Cumulative dist | `CUME_DIST() OVER (...)`                    | `rank(pct=True, method="max")` |

---

## References
- farlowdw, [Database SQL Primer - Part 2: Window Functions](https://leetcode.com/discuss/post/1600719/database-sql-primer-part-2-window-functi-sm8m/)
- Colt Steele, [SQL Window Functions in 10 Minutes](https://youtu.be/y1KCM8vbYe4?si=TOH9VCXTSoxq8xNo
- [PostgreSQL Window Function Documentation](https://www.postgresql.org/docs/current/tutorial-window.html)
- [pandas `DataFrame.groupby` User Guide](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [pandas `DataFrame.rolling` Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html)
