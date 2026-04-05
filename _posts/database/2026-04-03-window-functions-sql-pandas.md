---
layout: distill
title: "Window Functions in SQL and Pandas"
description: "A practical guide to window functions—ranking, aggregation, and offset operations computed over a sliding frame—demonstrated side-by-side in SQL and Python's pandas library."
date: 2026-04-03
categories: database
tags: sql pandas python data-handling
project: database
---

# Window function = data analysis step

After the database server has completed all of the steps necessary to evaluate a query, including joining, filtering, grouping, and sorting, the result set is complete and ready to be returned to the caller. Imagine if you could pause the query execution at this point and take a walk through the result set while it is still held in memory; what types of analysis might you want to do? If your result set contains sales data, perhaps you might want to generate rankings for salespeople or regions, or calculate percentage differences between one time period and another. If you are generating results for a financial report, perhaps you would like to calculate subtotals for each report section, and a grand total for the final section. Using analytic functions, you can do all of these things and more.

Window functions let you compute aggregations, rankings, or offsets **across a set of rows that are related to the current row**—without collapsing the result into a single row the way `GROUP BY` does. They are one of the most powerful tools for data analysis in both SQL and pandas.

# Summary Cheat Sheet

| Operation       | SQL                                         | pandas                         |
| --------------- | ------------------------------------------- | ------------------------------ |
| Dense rank      | `DENSE_RANK() OVER (...)`                   | `rank(method="dense")`         |
| Rank            | `RANK() OVER (...)`                         | `rank(method="min")`           |
| Group total     | `SUM() OVER (PARTITION BY ...)`             | `groupby().transform("sum")`   |
| Row number      | `ROW_NUMBER() OVER (...)`                   | `rank(method="first")`         |
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

# Ranking

Ranking functions assign an ordinal position to each row within its partition.

| Function       | Behavior                                               |
| -------------- | ------------------------------------------------------ |
| `DENSE_RANK()` | Tied rows get the same rank; next rank does *not* skip |
| `ROW_NUMBER()` | Unique sequential integer, no ties                     |
| `RANK()`       | Tied rows get the same rank; next rank skips           |

## .rank() function
`
DataFrame.rank(axis=0, method='average', numeric_only=False, na_option='keep', ascending=True, pct=False)
`

- rank is a window function: it does not collapse rows. 
- If just used, it ranks among all rows
- If used with groupby, it ranks among groups

### Key options

- method
  - average: average rank of the group. can be float. e.g. rank 2.5 (think of 1.5tier journals)
  - min: lowest rank in the group (think of equal contribution co autuors)
  - max: highest rank in the group 
  - first: ranks assigned in order they appear in the array
  - dense: like ‘min’, but rank always increases by 1 between groups.

- ascending
  - True: smallest values is rank 1 (think of running)
  - False: largest values is rank 1. Think of test score or salary. This is more common.


## Dense ranking


### Leetcode 178: Rank Scores
This is a almost a tutorial for rank function.

```python
def order_scores(scores: pd.DataFrame) -> pd.DataFrame:
    scores['rank'] = scores['score'].rank(method = 'dense', ascending = False)
    return scores.sort_values(by = 'score', ascending = False)[['score', 'rank']]
```

### Leetcode 184: Department Highest salary
Dense rank is used here.
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

### Leetcode 185: Department Top Three Salaries
Dense rank is used here.

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

### Leetcode 1875: Group Employees of the Same Salary
- Dense rank is used here.
- groupby + transform is the window function in pandas
- copy is needed when we assign new columns after filtering
- sort_values with two columns!
```python
    employees['salary_count'] = employees.groupby('salary')['salary'].transform('size')
    filtered_employees = employees[employees['salary_count'] > 1].copy() #since we are assigning new columns after filtering...


    filtered_employees['team_id'] = filtered_employees['salary'].rank(method = 'dense').astype(int)
    return filtered_employees[['employee_id', 'name', 'salary', 'team_id']].sort_values(['team_id', 'employee_id'])
```

## Ranking with ties
- rank(method = 'min'): first rank with ties

### Leetcode 512: Game Play Analysis II

```python
def game_analysis(activity: pd.DataFrame) -> pd.DataFrame:
activity['event_date_rank'] = activity.groupby('player_id')['event_date'].rank(method = 'min')
return activity[activity['event_date_rank']==1][['player_id', 'device_id']]
```

### Leetcode 586: Customer Placing the Largest Number of Orders
- Follow up: What if more than one customer has the largest number of orders, can you find all the customer_number in this case?

- first rank with ties
- When you do orders.groupby('customer_number').size(), Pandas makes customer_number the index of the new DataFrame, not a column.
- in pandas, no .count(). it's .size()
- aggregation removes anything other than group variable and aggregated variable. group variable is turned into index. use reset_index() to make it a column.

```python
def largest_orders(orders: pd.DataFrame) -> pd.DataFrame:
order_count = orders.groupby('customer_number').size().reset_index(name='order_count') #result is two columns
order_count['count_rank'] = order_count['order_count'].rank(method = 'min', ascending = False)
return order_count[order_count['count_rank'] == 1][['customer_number']]
```

### Leetcode 1070: Product Sales Analysis III
```python
def sales_analysis(sales: pd.DataFrame) -> pd.DataFrame:
sales['year_rank'] = sales.groupby('product_id')['year'].rank(method = 'min')
return sales[sales['year_rank']==1][['product_id', 'year', 'quantity', 'price']].rename(
columns = {'year': 'first_year'}
)
```

### Leetcode 1082: Sales Analysis I

<!--
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| product_id   | int     |
| product_name | varchar |
| unit_price   | int     |
+--------------+---------+
product_id is the primary key (column with unique values) of this table.
Each row of this table indicates the name and the price of each product.
Table: Sales

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| seller_id   | int     |
| product_id  | int     |
| buyer_id    | int     |
| sale_date   | date    |
| quantity    | int     |
| price       | int     |
+-------------+---------+
This table can have repeated rows.
product_id is a foreign key (reference column) to the Product table.
Each row of this table contains some information about one sale.
 

Write a solution that reports the best seller by total sales price, If there is a tie, report them all.

Return the result table in any order.

The result format is in the following example.

 

Example 1:

Input: 
Product table:
+------------+--------------+------------+
| product_id | product_name | unit_price |
+------------+--------------+------------+
| 1          | S8           | 1000       |
| 2          | G4           | 800        |
| 3          | iPhone       | 1400       |
+------------+--------------+------------+
Sales table:
+-----------+------------+----------+------------+----------+-------+
| seller_id | product_id | buyer_id | sale_date  | quantity | price |
+-----------+------------+----------+------------+----------+-------+
| 1         | 1          | 1        | 2019-01-21 | 2        | 2000  |
| 1         | 2          | 2        | 2019-02-17 | 1        | 800   |
| 2         | 2          | 3        | 2019-06-02 | 1        | 800   |
| 3         | 3          | 4        | 2019-05-13 | 2        | 2800  |
+-----------+------------+----------+------------+----------+-------+
Output: 
+-------------+
| seller_id   |
+-------------+
| 1           |
| 3           |
+-------------+
Explanation: Both sellers with id 1 and 3 sold products with the most total price of 2800.
-->

- first rank with ties

```python
def sales_analysis(sales: pd.DataFrame, product: pd.DataFrame) -> pd.DataFrame:
    sales_record = sales.merge(product, on = 'product_id', how = 'left')
    revenue = sales_record.groupby('seller_id')['price'].sum().reset_index(name = 'revenue') 
    revenue['revenue_rank'] = revenue['revenue'].rank(method = 'min', ascending = False)
    return revenue[revenue['revenue_rank'] == 1][['seller_id']]
```

### Leetcode 1112: Highest Grade For Each Student

<!--
Table: Enrollments

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| student_id    | int     |
| course_id     | int     |
| grade         | int     |
+---------------+---------+
(student_id, course_id) is the primary key (combination of columns with unique values) of this table.
grade is never NULL.
 

Write a solution to find the highest grade with its corresponding course for each student. In case of a tie, you should find the course with the smallest course_id.

Return the result table ordered by student_id in ascending order.

The result format is in the following example.

 

Example 1:

Input: 
Enrollments table:
+------------+-------------------+
| student_id | course_id | grade |
+------------+-----------+-------+
| 2          | 2         | 95    |
| 2          | 3         | 95    |
| 1          | 1         | 90    |
| 1          | 2         | 99    |
| 3          | 1         | 80    |
| 3          | 2         | 75    |
| 3          | 3         | 82    |
+------------+-----------+-------+
Output: 
+------------+-------------------+
| student_id | course_id | grade |
+------------+-----------+-------+
| 1          | 2         | 99    |
| 2          | 2         | 95    |
| 3          | 3         | 82    |
+------------+-----------+-------+
-->

- .rank cannot handle multiple columns.
- Insteand, use sort_values() and then .drop_duplicates()

```python
def highest_grade(enrollments: pd.DataFrame) -> pd.DataFrame:
    sorted_df = enrollments.sort_values(
        by = ['student_id', 'grade', 'course_id'],
        ascending = [True, False, True]
    )
    
    top_grades = sorted_df.drop_duplicates(subset = ['student_id'], keep ='first')
    return top_grades[['student_id', 'course_id', 'grade']]
```
## Row number: unique integers


### Leetcode 601. Human Traffic of Stadium
- https://leetcode.com/problems/human-traffic-of-stadium/description/
- hard. skip for now
### Leetcode 618. Students Report By Geography
- https://leetcode.com/problems/students-report-by-geography/description/
- hard. skip for now


# AVG, MAX, MIN groupby + transform('mean', 'max', 'min')

 
### [Leetcode 615](https://leetcode.com/problems/average-salary-departments-vs-company/). Average Salary: Departments VS Company

<!--
Table: Salary

+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| employee_id | int  |
| amount      | int  |
| pay_date    | date |
+-------------+------+
In SQL, id is the primary key column for this table.
Each row of this table indicates the salary of an employee in one month.
employee_id is a foreign key (reference column) from the Employee table.
 

Table: Employee

+---------------+------+
| Column Name   | Type |
+---------------+------+
| employee_id   | int  |
| department_id | int  |
+---------------+------+
In SQL, employee_id is the primary key column for this table.
Each row of this table indicates the department of an employee.
 

Find the comparison result (higher/lower/same) of the average salary of employees in a department to the company's average salary.

Return the result table in any order.

The result format is in the following example.

 

Example 1:

Input: 
Salary table:
+----+-------------+--------+------------+
| id | employee_id | amount | pay_date   |
+----+-------------+--------+------------+
| 1  | 1           | 9000   | 2017/03/31 |
| 2  | 2           | 6000   | 2017/03/31 |
| 3  | 3           | 10000  | 2017/03/31 |
| 4  | 1           | 7000   | 2017/02/28 |
| 5  | 2           | 6000   | 2017/02/28 |
| 6  | 3           | 8000   | 2017/02/28 |
+----+-------------+--------+------------+
Employee table:
+-------------+---------------+
| employee_id | department_id |
+-------------+---------------+
| 1           | 1             |
| 2           | 2             |
| 3           | 2             |
+-------------+---------------+
Output: 
+-----------+---------------+------------+
| pay_month | department_id | comparison |
+-----------+---------------+------------+
| 2017-02   | 1             | same       |
| 2017-03   | 1             | higher     |
| 2017-02   | 2             | same       |
| 2017-03   | 2             | lower      |
+-----------+---------------+------------+
Explanation: 
In March, the company's average salary is (9000+6000+10000)/3 = 8333.33...
The average salary for department '1' is 9000, which is the salary of employee_id '1' since there is only one employee in this department. So the comparison result is 'higher' since 9000 > 8333.33 obviously.
The average salary of department '2' is (6000 + 10000)/2 = 8000, which is the average of employee_id '2' and '3'. So the comparison result is 'lower' since 8000 < 8333.33.

With he same formula for the average salary comparison in February, the result is 'same' since both the department '1' and '2' have the same average salary with the company, which is 7000. 
-->

- transform + mean to get dept average and total average
- drop duplicate to get department version dataframe. This is simpler than groupby.
- use np.select() to create the comparison column: requires list of two boolean arrays and list of two values and a default value.

```python
import pandas as pd
import numpy as np
def average_salary(salary: pd.DataFrame, employee: pd.DataFrame) -> pd.DataFrame:
# 1. Merge tables
    df = salary.merge(employee, on='employee_id')
    
    # 2. Format the date as a string 'YYYY-MM' (safer than to_period)
    df['pay_month'] = df['pay_date'].dt.strftime('%Y-%m')

    
    # 3. Calculate the averages using your transform logic
    df['salary_avg'] = df.groupby('pay_month')['amount'].transform('mean')
    df['salary_avg_dept'] = df.groupby(['pay_month', 'department_id'])['amount'].transform('mean')
    

    # 4. Drop duplicates to get unique month-department combinations
    df = df.drop_duplicates(
        subset=['pay_month', 'department_id'], keep='first'
    ).sort_values(['pay_month', 'department_id']).copy()
    
    # 5. Create the exact 'higher', 'lower', 'same' comparison
    conditions = [
        df['salary_avg_dept'] > df['salary_avg'],
        df['salary_avg_dept'] < df['salary_avg']
    ]
    choices = ['higher', 'lower']
    df['comparison'] = np.select(conditions, choices, default='same')
    
    # 6. Return only the requested columns
    return df[['pay_month', 'department_id', 'comparison']]
```
### [Leetcode 1084](https://leetcode.com/problems/sales-analysis-iii/description/). Sales Analysis III

<!--
Table: Product

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| product_id   | int     |
| product_name | varchar |
| unit_price   | int     |
+--------------+---------+
product_id is the primary key (column with unique values) of this table.
Each row of this table indicates the name and the price of each product.
Table: Sales

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| seller_id   | int     |
| product_id  | int     |
| buyer_id    | int     |
| sale_date   | date    |
| quantity    | int     |
| price       | int     |
+-------------+---------+
This table can have duplicate rows.
product_id is a foreign key (reference column) to the Product table.
Each row of this table contains some information about one sale.
 

Write a solution to report the products that were only sold in the first quarter of 2019. That is, between 2019-01-01 and 2019-03-31 inclusive.

Return the result table in any order.

The result format is in the following example.

 

Example 1:

Input: 
Product table:
+------------+--------------+------------+
| product_id | product_name | unit_price |
+------------+--------------+------------+
| 1          | S8           | 1000       |
| 2          | G4           | 800        |
| 3          | iPhone       | 1400       |
+------------+--------------+------------+
Sales table:
+-----------+------------+----------+------------+----------+-------+
| seller_id | product_id | buyer_id | sale_date  | quantity | price |
+-----------+------------+----------+------------+----------+-------+
| 1         | 1          | 1        | 2019-01-21 | 2        | 2000  |
| 1         | 2          | 2        | 2019-02-17 | 1        | 800   |
| 2         | 2          | 3        | 2019-06-02 | 1        | 800   |
| 3         | 3          | 4        | 2019-05-13 | 2        | 2800  |
+-----------+------------+----------+------------+----------+-------+
Output: 
+-------------+--------------+
| product_id  | product_name |
+-------------+--------------+
| 1           | S8           |
+-------------+--------------+
Explanation: 
The product with id 1 was only sold in the spring of 2019.
The product with id 2 was sold in the spring of 2019 but was also sold after the spring of 2019.
The product with id 3 was sold after spring 2019.
We return only product 1 as it is the product that was only sold in the spring of 2019.
-->

- can use window function or groupby aggregation, both win `min`
- I tested both: since the result requires returning the product name, groupby aggregation is very slow because it requires groupby with respect to string. 
- numbers: window funciton beats 50%, aggregation beats 25%

```python
import pandas as pd

def sales_analysis(product: pd.DataFrame, sales: pd.DataFrame) -> pd.DataFrame:
    df = sales.merge(product, on= 'product_id')
    df['is_first_quarter'] = df['sale_date'].between('2019-01-01', '2019-03-31')
    df['is_only_first_quarter'] = df.groupby('product_id')['is_first_quarter'].transform('min')
    return df[df['is_only_first_quarter'] == True].drop_duplicates(subset = ['product_id'])[['product_id', 'product_name']]
```

### [Leetcode 1867. Orders With Maximum Quantity Above Average](https://leetcode.com/problems/orders-with-maximum-quantity-above-average/description/)
MAX()





LAG()

1709. Biggest Window Between Visits
LEAD()

1811. Find Interview Candidates

 
 



# Group cumulative sum: groupby + cumsum
- this corresponds to SUM() OVER (PARTITION BY ...) in SQL.

## Leetcode 534. Game Play Analysis III
- original problem: https://leetcode.com/problems/game-play-analysis-iii/description/
<!--
Table: Activity

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| player_id    | int     |
| device_id    | int     |
| event_date   | date    |
| games_played | int     |
+--------------+---------+
(player_id, event_date) is the primary key (combination of columns with unique values) of this table.
This table shows the activity of players of some games.
Each row is a record of a player who logged in and played a number of games (possibly 0) before logging out on someday using some device.
 

Write a solution to report the device that is first logged in for each player.

Return the result table in any order.

The result format is in the following example.

 

Example 1:

Input: 
Activity table:
+-----------+-----------+------------+--------------+
| player_id | device_id | event_date | games_played |
+-----------+-----------+------------+--------------+
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-05-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |
+-----------+-----------+------------+--------------+
Output: 
+-----------+-----------+
| player_id | device_id |
+-----------+-----------+
| 1         | 2         |
| 2         | 3         |
| 3         | 1         |
+-----------+-----------+
-->

- pandas seems to be not good at window functions with multiple conditions.
- so first sort and then use cumsum. always sort before using cumsum.

```python
def game_play_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    activity = activity.sort_values(by = ['player_id', 'event_date'])
    activity['games_played_so_far'] = activity.groupby('player_id')['games_played'].cumsum()
    return activity[['player_id', 'event_date', 'games_played_so_far']]
```

## Leetcode 579. Find Cumulative Salary of an Employee
- hard. skip for now.

## Leetcode 1308. Running Total for Different Genders
- original problem is [here](https://leetcode.com/problems/running-total-for-different-genders/
description/)
- always sort_values before using cumsum
- always lose one granularity when using cumsum

<!--
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| player_name   | varchar |
| gender        | varchar |
| day           | date    |
| score_points  | int     |
+---------------+---------+
(gender, day) is the primary key (combination of columns with unique values) for this table.
A competition is held between the female team and the male team.
Each row of this table indicates that a player_name and with gender has scored score_point in someday.
Gender is 'F' if the player is in the female team and 'M' if the player is in the male team.
 

Write a solution to find the total score for each gender on each day.

Return the result table ordered by gender and day in ascending order.

The result format is in the following example.

 

Example 1:

Input: 
Scores table:
+-------------+--------+------------+--------------+
| player_name | gender | day        | score_points |
+-------------+--------+------------+--------------+
| Aron        | F      | 2020-01-01 | 17           |
| Alice       | F      | 2020-01-07 | 23           |
| Bajrang     | M      | 2020-01-07 | 7            |
| Khali       | M      | 2019-12-25 | 11           |
| Slaman      | M      | 2019-12-30 | 13           |
| Joe         | M      | 2019-12-31 | 3            |
| Jose        | M      | 2019-12-18 | 2            |
| Priya       | F      | 2019-12-31 | 23           |
| Priyanka    | F      | 2019-12-30 | 17           |
+-------------+--------+------------+--------------+
Output: 
+--------+------------+-------+
| gender | day        | total |
+--------+------------+-------+
| F      | 2019-12-30 | 17    |
| F      | 2019-12-31 | 40    |
| F      | 2020-01-01 | 57    |
| F      | 2020-01-07 | 80    |
| M      | 2019-12-18 | 2     |
| M      | 2019-12-25 | 13    |
| M      | 2019-12-30 | 26    |
| M      | 2019-12-31 | 29    |
| M      | 2020-01-07 | 36    |
+--------+------------+-------+
Explanation: 
For the female team:
The first day is 2019-12-30, Priyanka scored 17 points and the total score for the team is 17.
The second day is 2019-12-31, Priya scored 23 points and the total score for the team is 40.
The third day is 2020-01-01, Aron scored 17 points and the total score for the team is 57.
The fourth day is 2020-01-07, Alice scored 23 points and the total score for the team is 80.

For the male team:
The first day is 2019-12-18, Jose scored 2 points and the total score for the team is 2.
The second day is 2019-12-25, Khali scored 11 points and the total score for the team is 13.
The third day is 2019-12-30, Slaman scored 13 points and the total score for the team is 26.
The fourth day is 2019-12-31, Joe scored 3 points and the total score for the team is 29.
The fifth day is 2020-01-07, Bajrang scored 7 points and the total score for the team is 36.
-->

```python
def running_total_for_different_genders(scores: pd.DataFrame) -> pd.DataFrame:
    scores = scores.sort_values(by = ['gender', 'day'])
    scores['total'] = scores.groupby('gender')['score_points'].cumsum()
    return scores[['gender', 'day', 'total']]
```

## Leetcode 180. Consecutive Numbers
- https://leetcode.com/problems/consecutive-numbers/
- An SQl guru categorized this as a row number problem, but this is also a cumsum problem
- use shift and cumsum to detect changepoint




## Leetcode 180. Consecutive Numbers

<!--
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+
In SQL, id is the primary key for this table.
id is an autoincrement column starting from 1.
 

Find all numbers that appear at least three times consecutively.

Return the result table in any order.

The result format is in the following example.

 

Example 1:

Input: 
Logs table:
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |
+----+-----+
Output: 
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
Explanation: 1 is the only number that appears consecutively for at least three times.
-->
- very sophisticated way of detecting changepoint. 
- Don't think this is a generaliable skill...

```python
def consecutive_numbers(logs: pd.DataFrame) -> pd.DataFrame:
# 1. Sort by Id to ensure we are looking at the rows in sequential order
    logs['block_indicator'] = (logs['num'] != logs['num'].shift()).fillna(True).cumsum()
    logs['consec_counts'] = logs.groupby('block_indicator').transform('size')
    # groupby includes num because the output contains num; num is not used for grouping
    return logs[logs['consec_counts'] >=3].drop_duplicates(
        subset = ['num'], keep = 'first'
    )[['num']].rename(
        columns = {'num': 'ConsecutiveNums'}
    )
 ```
 
# COUNT = .groupby.transform('size')

## Leetcode 1303: Find the Team Size

```python
def team_size(employee: pd.DataFrame) -> pd.DataFrame:
employee['team_size'] = employee.groupby('team_id')['team_id'].transform('size')
return employee[['employee_id', 'team_size']]
```

# AVG() = 

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



## References
- farlowdw, [Database SQL Primer - Part 2: Window Functions](https://leetcode.com/discuss/post/1600719/database-sql-primer-part-2-window-functi-sm8m/)
- Colt Steele, [SQL Window Functions in 10 Minutes](https://youtu.be/y1KCM8vbYe4?si=TOH9VCXTSoxq8xNo
- [PostgreSQL Window Function Documentation](https://www.postgresql.org/docs/current/tutorial-window.html)
- [pandas `DataFrame.groupby` User Guide](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [pandas `DataFrame.rolling` Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html)
