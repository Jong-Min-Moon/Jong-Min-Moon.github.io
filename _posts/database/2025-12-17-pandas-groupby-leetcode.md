---
layout: distill
title: "pandas merge and groupby"
description: 
date: 2025-12-17
categories: database
tags: pandas python leetcode data-handling
project: database
---


# Merge
Merge is so basic that it rarely shows up as a standalone problem. It is usually a part of a more complex problem. The most frequent pattern is merge + groupby.

- basic syntax: `pd.merge(A, B, on= 'aaa')` where two tables have the same column name 'aaa'.
- merge on different columns: `pd.merge(A, B, left_on = 'aaa', right_on = 'bbb')`
- left join is the one used most at work. 60% of the times. we keep all rows from the left df. we keep only the matching row from the right df. the info that is not in the right df will be filled with NaN. `pd.merge(A, B, left_on = 'aaa', right_on = 'bbb', how = 'left')` Forget right join. Industry standard is left join.
- inner join used 30% of the times. it keeps the intersection so there will be no NA. `pd.merge(A, B, left_on = 'aaa', right_on = 'bbb', how = 'inner')`
- full outer join keeps all rows in both tables. there will be many NA. Good for finding missing values. [Leetcode 1965: Employees With Missing Information](https://leetcode.com/problems/employees-with-missing-information/description/) is a good example.

 

# Groupby


## Summary Cheat Sheet

| SQL                   | pandas                                     | 설명                           |
| --------------------- | ------------------------------------------ | ------------------------------ |
| `GROUP BY col`        | `.groupby('col')`                          | starts with groupby()          |
| | `.reset_index(name = 'new_col')` |  usually the submission ends with this
| `COUNT(*)`            | `.size()`                                  | counts all rows in each group  |
| `COUNT(DISTINCT col)` | `.nunique()`                               | counts unique values in each group |
| `SUM(col)`            | `.sum()`                                   | 합계                           |
| `AVG(col)`            | `.mean()`                                  | 평균                           |
| `AS new_col`          | `.reset_index(name='new_col')` or `.agg()` | 결과 컬럼명 지정               |
| `GROUP_CONCAT`        | `.agg(lambda x: ','.join(...))`            | 여러 행의 문자열을 하나로 통합 |

### [2356. Number of Unique Subjects Taught by Each Teacher](https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/description/)

 `.groupby()`, `.nunique()`, `.reset_index()`, `rename(columns={})`

```python
import pandas as pd

def count_unique_subjects(teacher: pd.DataFrame) -> pd.DataFrame:
    return teacher.groupby('teacher_id')['subject_id'].nunique().reset_index(name = 'cnt')
```

### [1693. Daily Leads and Partners](https://leetcode.com/problems/daily-leads-and-partners/description/)

`groupby` with two indices, dictionary aggregator (named aggregation)

```python
import pandas as pd

def daily_leads_and_partners(daily_sales: pd.DataFrame) -> pd.DataFrame:
    return daily_sales.groupby(['date_id', 'make_name']).agg(
        unique_leads=('lead_id', 'nunique'),
        unique_partners=('partner_id', 'nunique')
    ).reset_index()
```

### [1741. Find Total Time Spent by Each Employee](https://leetcode.com/problems/find-total-time-spent-by-each-employee/description/)

Mutate (add column) and then `agg`

```python
import pandas as pd

def total_time(employees: pd.DataFrame) -> pd.DataFrame:
    employees['time_spent'] = employees['out_time'] - employees['in_time']
    return employees.groupby(['event_day', 'emp_id'])['time_spent'].sum().reset_index(name = 'total_time')[['event_day', 'emp_id', 'total_time']].rename(
        columns = {
            'event_day' : 'day'
        }
    ) 
```

### [1484. Group Sold Products By The Date](https://leetcode.com/problems/group-sold-products-by-the-date/description/)

`agg` by tuple with `lambda x` for complex string joining
- one column, two aggregation: use list of tuples
- use lambda for complicated aggregation
- Series.unique() outputs a python list
- sorted(list)

```python
import pandas as pd

def categorize_products(activities: pd.DataFrame) -> pd.DataFrame:
    return activities.groupby('sell_date')['product'].agg(
        [
            ('num_sold', 'nunique'),
            ('products', lambda x: ','.join(sorted(x.unique())))
            # to Series.unique() outputs a python list
            # sorted(list)
        ]
    ).reset_index()
```

# Merge + Groupby
TBD.

always think of null when merging


- 1587. groupby + merge + query

- 610: triangle judgement.
  - mutation is vector arithmetic. max(axis=1)
  - .map can change datatype
.replace cannot change datatype.
  - .map({True: 'Yes', False: 'No'})  
- 181. Employees Earning More Than Their Managers
  - self merge. left on, right on
- 1661. Average Time of Process per Machine
  - agg paired quantities in one column
  - pivot
- 1280. Students and Examinations
  - merge(..., how = 'cross') to make cross product
- 3570. Find Books with No Available Copies
  - merge (right=groupby), agg two, filter with two aggregated function
- 1084 groupby.filter.  lambda x date.min drop.duplicates
- 3642 multiple aggregation for same column.


# Pandas `groupby()` 완벽 이해하기

Pandas의 `groupby()`는 데이터를 특정 키(컬럼)를 기준으로 그룹으로 나누고(**Split**), 각 그룹에 대해 함수를 적용해(**Apply**) 결과를 통합하는(**Combine**) 강력한 기능입니다. SQL의 `GROUP BY`와 유사하며, 요약 통계(평균, 합계, 개수 등)를 계산할 때 필수적으로 사용됩니다.

## 1. 기본 원리: S-A-C 패턴
`groupby()`는 데이터를 분할하고, 연산하고, 합치는 **Split-Apply-Combine** 과정을 거칩니다.

1.  **Split (분할):** 지정된 키(컬럼)의 동일한 값을 가진 행들을 하나의 그룹으로 나눕니다.
2.  **Apply (적용):** 각 그룹에 집계 함수(`sum()`, `mean()`, `count()`, `agg()` 등)를 적용하여 데이터를 변환하거나 계산합니다.
3.  **Combine (통합):** 적용된 결과를 새로운 데이터프레임이나 시리즈 형태로 합쳐서 반환합니다.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/pandas_groupby_sac.png" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    Split-Apply-Combine pattern: Grouping data, applying a function (like mean), and combining results.
</div>

---

## 2. 주요 사용 예시와 LeetCode 실전 문제

### 2.1 기초 집계: `.nunique()`와 `.reset_index()`
데이터의 고유값 개수를 세는 `nunique()`는 실무에서 매우 자주 쓰입니다. `groupby`를 수행하면 그룹 키가 **인덱스(Index)**로 가기 때문에, 다시 일반 컬럼으로 돌려주는 `reset_index()`가 거의 세트처럼 따라다닙니다.

#### [LeetCode 2356: Number of Unique Subjects Taught by Each Teacher](https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/)

**SQL:**
```sql
SELECT teacher_id, COUNT(DISTINCT subject_id) AS cnt
FROM Teacher
GROUP BY teacher_id;
```

**Pandas:**
```python
import pandas as pd

def count_unique_subjects(teacher: pd.DataFrame) -> pd.DataFrame:
    return teacher.groupby('teacher_id')['subject_id'].nunique().reset_index(name='cnt')
```

---

# .agg() with multiple columns
여러 컬럼을 기준으로 그룹을 묶고, 각 집계 결과에 이름을 바로 붙여줄 때 유용합니다. `agg(새컬럼명=('대상컬럼', '함수'))` 형태의 튜플 구조를 사용합니다.

#### [LeetCode 1693: Daily Leads and Partners](https://leetcode.com/problems/daily-leads-and-partners/)

**SQL:**
```sql
SELECT date_id, make_name, 
       COUNT(DISTINCT lead_id) AS unique_leads, 
       COUNT(DISTINCT partner_id) AS unique_partners
FROM DailySales
GROUP BY date_id, make_name;
```

**Pandas:**
```python
def daily_leads_and_partners(daily_sales: pd.DataFrame) -> pd.DataFrame:
    return daily_sales.groupby(['date_id', 'make_name']).agg(
        unique_leads=('lead_id', 'nunique'),
        unique_partners=('partner_id', 'nunique')
    ).reset_index()
```


### [Leetcode 1867. Orders With Maximum Quantity Above Average](https://leetcode.com/problems/orders-with-maximum-quantity-above-average/description/)

<!--
Table: OrdersDetails

+-------------+------+
| Column Name | Type |
+-------------+------+
| order_id    | int  |
| product_id  | int  |
| quantity    | int  |
+-------------+------+
(order_id, product_id) is the primary key (combination of columns with unique values) for this table.
A single order is represented as multiple rows, one row for each product in the order.
Each row of this table contains the quantity ordered of the product product_id in the order order_id.
 

You are running an e-commerce site that is looking for imbalanced orders. An imbalanced order is one whose maximum quantity is strictly greater than the average quantity of every order (including itself).

The average quantity of an order is calculated as (total quantity of all products in the order) / (number of different products in the order). The maximum quantity of an order is the highest quantity of any single product in the order.

Write a solution to find the order_id of all imbalanced orders.

Return the result table in any order.

The result format is in the following example.

 

Example 1:

Input: 
OrdersDetails table:
+----------+------------+----------+
| order_id | product_id | quantity |
+----------+------------+----------+
| 1        | 1          | 12       |
| 1        | 2          | 10       |
| 1        | 3          | 15       |
| 2        | 1          | 8        |
| 2        | 4          | 4        |
| 2        | 5          | 6        |
| 3        | 3          | 5        |
| 3        | 4          | 18       |
| 4        | 5          | 2        |
| 4        | 6          | 8        |
| 5        | 7          | 9        |
| 5        | 8          | 9        |
| 3        | 9          | 20       |
| 2        | 9          | 4        |
+----------+------------+----------+
Output: 
+----------+
| order_id |
+----------+
| 1        |
| 3        |
+----------+
Explanation: 
The average quantity of each order is:
- order_id=1: (12+10+15)/3 = 12.3333333
- order_id=2: (8+4+6+4)/4 = 5.5
- order_id=3: (5+18+20)/3 = 14.333333
- order_id=4: (2+8)/2 = 5
- order_id=5: (9+9)/2 = 9

The maximum quantity of each order is:
- order_id=1: max(12, 10, 15) = 15
- order_id=2: max(8, 4, 6, 4) = 8
- order_id=3: max(5, 18, 20) = 20
- order_id=4: max(2, 8) = 8
- order_id=5: max(9, 9) = 9

Orders 1 and 3 are imbalanced because they have a maximum quantity that exceeds the average quantity of every order.
-->

- all groupby uses one index (order_id) so window function is redundant. aggregation suffices.

```python
def orders_above_average(orders_details: pd.DataFrame) -> pd.DataFrame:
    order_stats = orders_details.groupby('order_id').agg(
        total_qty=('quantity', 'sum'),
        # Use 'nunique' for unique products, or 'size' for total rows
        product_count=('product_id', 'nunique'), 
        max_qty=('quantity', 'max')
    ).reset_index()
    
    # 2. Safely calculate your custom weighted average
    order_stats['custom_avg'] = order_stats['total_qty'] / order_stats['product_count']
    
    # 3. Find the highest average
    global_max_avg = order_stats['custom_avg'].max()
    
    # 4. Filter and return
    valid_orders = order_stats[order_stats['max_qty'] > global_max_avg]
    return valid_orders[['order_id']]
```

### 2.3 Mutate (컬럼 추가) 후 Aggregation
그룹핑 전에 데이터를 먼저 가공(예: 시간 차이 계산)한 뒤 집계하는 패턴입니다.

#### [LeetCode 1741: Find Total Time Spent by Each Employee](https://leetcode.com/problems/find-total-time-spent-by-each-employee/)

**SQL:**
```sql
SELECT event_day AS day, emp_id, SUM(out_time - in_time) AS total_time
FROM Employees
GROUP BY event_day, emp_id;
```

**Pandas:**
```python
def total_time(employees: pd.DataFrame) -> pd.DataFrame:
    # 1. 먼저 각 행별로 시간 차이 계산 (Mutate)
    employees['total_time'] = employees['out_time'] - employees['in_time']
    
    # 2. 그룹핑 및 합계 계산
    result = employees.groupby(['emp_id', 'event_day'])['total_time'].sum().reset_index()
    
    # 3. 컬럼명 정리
    return result.rename(columns={'event_day': 'day'})
```

---

### 2.4 Lambda를 활용한 복합 집계
단순한 합계나 평균이 아니라, "문자열을 콤마로 이어 붙이기" 같은 특수한 로직이 필요할 때 `lambda`와 `agg`를 조합합니다.

#### [LeetCode 1484: Group Sold Products By The Date](https://leetcode.com/problems/group-sold-products-by-the-date/)

**SQL (MySQL):**
```sql
SELECT sell_date, 
       COUNT(DISTINCT product) AS num_sold, 
       GROUP_CONCAT(DISTINCT product ORDER BY product ASC SEPARATOR ',') AS products
FROM Activities
GROUP BY sell_date
ORDER BY sell_date;
```

**Pandas:**
```python
def categorize_products(activities: pd.DataFrame) -> pd.DataFrame:
    # agg 내에서 튜플과 lambda를 사용하여 복합 로직 적용
    return activities.groupby('sell_date')['product'].agg([
        ('num_sold', 'nunique'),
        ('products', lambda x: ','.join(sorted(set(x))))
    ]).reset_index().sort_values('sell_date')
```



Pandas의 `groupby()`를 마스터하면 SQL에서 가능했던 모든 데이터 요약 작업을 파이썬에서도 효율적으로 처리할 수 있습니다!



# Reference
- 
[Master Python Pandas Merge: The Ultimate Guide to Combining DataFrames](https://youtu.be/Fl3VGL3BuAA?si=yK36yxdVzC53Xlj8)