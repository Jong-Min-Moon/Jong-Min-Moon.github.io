---
layout: distill
title: "LeetCode 1204: Last Person to Fit in the Bus"
description: "Solving the 'Last Person to Fit in the Bus' problem using window functions in both SQL and pandas. A perfect application of running totals to real-world scenarios."
date: 2026-04-03
categories: database
tags: leetcode sql pandas window-functions
project: database
---

In this post, we solve [LeetCode 1204: Last Person to Fit in the Bus](https://leetcode.com/problems/last-person-to-fit-in-the-bus/).
This problem is essentially a constraint-based selection task. In SQL, it serves as a classic example of using window functions—specifically, computing a running total over the entire table. In contrast, in pandas, the solution is straightforward and can be implemented cleanly using the .cumsum() method.

 
##   pandas Solution: Using `cumsum()`
- We usually have to sort before cumsum. `sort_values` takes $O(n \log n)$. Watch out: you have to assign the sorted df to a variable, not just call `sort_values`.
- .cumsum() can be applied to both one column (series) and df itself. Here, it is easier to apply it to one column.
- After `tail(1)`, to return the pandas df, we use `[['person_name']]`, not `['person_name']` which returns a pandas series.

```python
import pandas as pd

def last_passenger(queue: pd.DataFrame) -> str:
    # 1. Sort the queue by turn to ensure the correct boarding order
    queue = queue.sort_values('turn')
    
    # 2. Calculate the running total of weights
    queue['cumulative_weight'] = queue['weight'].cumsum()
    
    # 3. Filter those who stay under the 1000kg limit
    fits = queue[queue['cumulative_weight'] <= 1000]
    
    # 4. Return the name of the last person in the filtered list
    return fits.tail(1)[['person_name']]
```

### Key pandas functions used:
- `.sort_values('turn')`: Ensures we process the queue in the correct order.
- `.cumsum()`: Calculates the prefix sum of the weight column.
- `.tail(1)`: Quickly accesses the last row of the filtered DataFrame.


### References
- [LeetCode 1204 Official Page](https://leetcode.com/problems/last-person-to-fit-in-the-bus/)
- [pandas `cumsum` Documentation](https://pandas.pydata.org/docs/reference/api/pandas.Series.cumsum.html)
