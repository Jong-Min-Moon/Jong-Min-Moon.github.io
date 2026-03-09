---
layout: distill
title: "Hyperparameter Tuning for Best Subset Selection"
description: "Exploring methods for determining the optimal subset size k in best subset selection problems."
date: 2026-03-08
categories: ml_mio optimization
tags: machine-learning optimization best-subset-selection hyperparameter-tuning
project: ml_mio
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Problem Overview
  - name: "1. Adjusted R^2 (MSE)"
  - name: 2. Bayesian Information Criterion (BIC)
---

# Optimization problem

Given $m$ observations $\{(a_i, y_i)\}_{i=1}^m$, where each $a_i \in \mathbb{R}^n$ are the features of point $i$ and $y_i \in \mathbb{R}$ is the associated response, a regularization parameter $\lambda \ge 0$, and a target complexity $k$, consider the best subset selection problem:

$$
\begin{align}
\min_{x_0 \in \mathbb{R}, x \in \mathbb{R}^n} & \frac{1}{m} \sum_{i=1}^m \left(y_i - x_0 - \sum_{j=1}^n a_{ij}x_j\right)^2 + \lambda \sum_{j=1}^n c_j x_j^2 \\
\text{s.t.} & \quad \sum_{j=1}^n \mathbb{1}\{x_j \neq 0\} \le k,
\end{align}
$$

where $c_j = \sum_{i=1}^m a_{ij}^2$. In some cases, $k$ is directly given by a decision-maker (e.g., due to interpretability considerations), but in other cases it should be determined as well. Denote by $x(k)^*$ the optimal solution of the problem for a given value of $k \in \mathbb{Z}^+$.

# Hyperparamter tuning
We use the **"Communities and Crime"** dataset from [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/183/communities+and+crime). This dataset combines socio-economic data from the 1990 U.S. Census, law enforcement data from the 1990 U.S. LEMAS survey, and crime statistics from the 1995 FBI UCR.

Using this dataset, we perform hyperparameter tuning for best subset selection with respect to the maximum number of features $k$. Model performance is evaluated using two criteria: adjusted $R^2$ (based on MSE) and the Bayesian Information Criterion (BIC):
- Adjusted $R^2$ (via MSE): Focused on minimizing prediction error while adjusting for degrees of freedom.
- Bayesian Information Criterion (BIC): Focused on model parsimony, penalizing additional parameters more strictly than MSE to prevent overfitting.
  
 For simplicity, we fix the ridge regularization hyperparameter at $\lambda = 0.01$.

---

#### 1. Adjusted $R^2$ (MSE)

The mean squared error (MSE) of predictor $x(k)^*$ is given by:

$$
\text{MSE}(k) = \frac{\sum_{i=1}^m \left(y_i - x(k)^*_0 - \sum_{j=1}^n a_{ij}x(k)^*_j\right)^2}{m - \sum_{j=1}^n \mathbb{1}\{x(k)^*_j \neq 0\}}
$$

which is a proxy for the variance of the prediction errors. The estimator that minimizes the MSE is also the estimator that maximizes the adjusted $R^2$ criterion.



#### 2. Bayesian Information Criterion (BIC)

The Bayesian information criterion (BIC) of predictor $x(k)^*$ is given by:

$$
\text{BIC}(k) = m \ln \left( \frac{\sum_{i=1}^m (y_i - x(k)^*_0 - \sum_{j=1}^n a_{ij}x(k)^*_j)^2}{m} \right) + \ln(m) \sum_{j=1}^n \mathbb{1}\{x(k)^*_j \neq 0\} + K
$$

where $K$ is a constant that does not depend on the estimator $x(k)^*$. The estimator that minimizes the BIC is (under appropriate assumptions) the estimator that is a posteriori more probable.


We aim to identify the cardinality $k$ that minimizes both the MSE and BIC, and to determine the key predictors along with their associated regression coefficients.


# The result


The optimization results reveal a clear distinction between the two tuning criteria. The BIC favored a significantly simpler model, while the MSE reached its minimum with a more complex feature set.

| Metric          | Best Cardinality ($k$) | Optimal Value |
| :-------------- | :--------------------: | :------------ |
| **Minimum MSE** |           20           | 0.075729      |
| **Minimum BIC** |           9            | -5077.7054    |



## Key Observations
* **BIC Trend:** The BIC reached its global minimum early at **$k=9$**. Beyond this point, the penalty term $\ln(m)k$ outweighed the marginal gains in the Residual Sum of Squares (RSS), indicating that additional features did not provide enough explanatory power to justify the added complexity.
* **MSE Trend:** The MSE continued to improve until **$k=20$**. This suggests that while a 20-feature model captures more variance, it may be slightly over-parameterized compared to the 9-feature model favored by BIC.


## Critical Predictors Analysis

Across both models, specific socio-economic indicators emerged as the most significant drivers of crime statistics.

### Top Predictors Comparison

| Predictor Name       | MSE ($k=20$) | BIC ($k=9$) | Interpretation                                                      |
| :------------------- | :----------: | :---------: | :------------------------------------------------------------------ |
| **PctKids2Par**      |   -0.0504    |   -0.0901   | Strongest negative correlation; indicates family stability.         |
| **PctPersDenseHous** |   +0.0504    |   +0.0501   | High positive correlation; indicates crowded living conditions.     |
| **racepctblack**     |   +0.0495    |   +0.0377   | Historically significant demographic predictor in this dataset.     |
| **PctIlleg**         |   +0.0389    |   +0.0378   | Consistent positive correlation across both models.                 |
| **HousVacant**       |   +0.0331    |   +0.0378   | Indicates a positive relationship between crime and vacant housing. |


## Conclusion
For this dataset, the **BIC-optimal model ($k=9$)** is recommended if the goal is interpretability and generalization. It captures the most influential variables—family structure (`PctKids2Par`), housing density (`PctPersDenseHous`), and vacancy rates (`HousVacant`)—while maintaining a lean structure. If maximum predictive precision is required, the **MSE-optimal model ($k=20$)** provides the lowest error rate.
# The code
First, we import the necessary packages and the custom preprocessing function. We use **Gurobi (`gurobipy`)** to handle the optimization logic.
The data preprocessing script is located at the end of this post.


```python
import gurobipy as gp
from gurobipy import GRB
import sys
import os
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocess_crime_data import preprocess_crime_data
```
`GRB` is a comprehensive library of constants that tell Gurobi exactly how to behave. 
| Category               | Examples                                           | Purpose                                                                             |
| :--------------------- | :------------------------------------------------- | :---------------------------------------------------------------------------------- |
| **Variable Types**     | `GRB.CONTINUOUS`, `GRB.BINARY`, `GRB.INTEGER`      | Defines the nature of your decision variables (e.g., fractional vs. whole numbers). |
| **Constraint Senses**  | `GRB.LESS_EQUAL`, `GRB.EQUAL`, `GRB.GREATER_EQUAL` | Sets the direction of your inequalities ($\le, =, \ge$).                            |
| **Optimization Sense** | `GRB.MINIMIZE`, `GRB.MAXIMIZE`                     | Instructs the solver to find either the lowest or highest possible value.           |
| **Status Codes**       | `GRB.OPTIMAL`, `GRB.INFEASIBLE`                    | Used to interpret results and verify if a valid solution was found.                 |
|                        |

### Core Optimization: Best Subset Selection (MIQP Formulation)
Now, we will implement the core optimization logic using a Mixed-Integer Quadratic Programming (MIQP) formulation to perform Best Subset Selection.

```python
def solve_best_subset(M, features, features0, A, y, K, norm_feature, env, L=1000, lam=0.01, mip_gap=0.05):
    """
    Solves the best subset selection problem for a fixed cardinality K.
    
    This function implements the Mixed-Integer Quadratic Programming (MIQP) formulation:
    min_{x, z}  sum((y - Ax)^2) + lambda * sum(norm(A_j)*x_j^2)
    s.t.        sum(z_j) = K
                -L*z_j <= x_j <= L*z_j
                z_j in {0, 1}
    """
    
    # Initialize Gurobi Model
    model = gp.Model(f"best_subset_k{K}", env=env)
    model.setParam('OutputFlag', 0) 
    model.setParam('MIPGap', mip_gap)

    # --- DECISION VARIABLES ---
    # x: Regression coefficients (continuous)
    x = model.addVars(features, lb=-GRB.INFINITY, name="x")
    # z: Selection indicators (binary)
    z = model.addVars(features0, vtype=GRB.BINARY, name="z")
    # r: Auxiliary variables for residuals to simplify objective representation
    r = model.addVars(range(1, M+1), lb=-GRB.INFINITY, name="r")

    # --- CONSTRAINTS ---
    # 1. Residual Definition: r[i] = y[i] - sum(A[i, j] * x[j])
    model.addConstrs(
        (r[i] == y[i] - gp.quicksum(A[i, j] * x[j] for j in features)
         for i in range(1, M+1)),
        name="residual"
    )

    # 2. Sparsity (Cardinality) Constraint: Enforce exactly K features selected
    model.addConstr(gp.quicksum(z[j] for j in features0) == K, name="cardinality")

    # 3. Big-M Linking Constraints: If z_j = 0, then x_j = 0. If z_j = 1, x_j is bounded by L.
    model.addConstrs((x[j] <= L * z[j] for j in features0), name="bound1")
    model.addConstrs((x[j] >= -L * z[j] for j in features0), name="bound2")

    # --- OBJECTIVE FUNCTION ---
    # Goal: Minimize Residual Sum of Squares (RSS) + L2 Regularization
    rss_expr = gp.quicksum(r[i]**2 for i in range(1, M+1))
    reg_expr = lam * gp.quicksum(norm_feature[j] * x[j]*x[j] for j in features0)
    
    model.setObjective(rss_expr + reg_expr, GRB.MINIMIZE)

    # --- OPTIMIZATION CALL ---
    model.optimize()

    # Extract results if solution found
    if model.status == GRB.OPTIMAL or model.status == GRB.SUBOPTIMAL:
        rss_val = sum(r[i].X**2 for i in range(1, M+1))
        return rss_val, {j: x[j].X for j in features}
    else:
        return None, None
```

### HYPERPARAMETER TUNING: Iterative Cardinality Search

```python
def run_iterative_selection(csv_path, k_range=range(5, 100)):
    """
    Iterates through a range of cardinalities (k) to find the best subset 
    using fit measures like MSE and BIC.
    """
    
    # Data Preparation
    print(f"Loading and preprocessing data from {csv_path}...")
    M, features, features0, A, y, feature_names = preprocess_crime_data(csv_path)
    
    results = []
    
    # State tracking for best models
    best_mse = float('inf')
    best_mse_k = -1
    best_mse_coeffs = None
    
    best_bic = float('inf')
    best_bic_k = -1
    best_bic_coeffs = None

    # Logging UI
    header = f"{'k':>3} | {'RSS':>10} | {'MSE':>10} | {'BIC':>12}"
    print(header)
    print("-" * 30)

    # Precompute feature norms (denominator for L2 regularization)
    norm_feature = {
        j: sum(A[i, j]**2 for i in range(1, M+1))
        for j in features
    }

    print(f"Starting loop for k in {list(k_range)}")
    sys.stdout.flush()

    # --- HYPERPARAMETER TUNING LOOP ---
    try:
        with gp.Env() as env:
            for k in k_range:
                print(f"Solving for k={k}...")
                sys.stdout.flush()
                
                # Call internal optimization
                rss, coeffs = solve_best_subset(M, features, features0, A, y, K=k, norm_feature=norm_feature, env=env)
            
                if rss is not None:
                    # =========================================================
                    # 3. FIT MEASURES: Evaluation of Model Quality
                    # =========================================================
                    
                    # MSE (Mean Squared Error) adjusted for degrees of freedom: RSS / (n - k - 1)
                    mse = rss / (M - k - 1)
                    
                    # BIC (Bayesian Information Criterion): Penalizes model complexity
                    # Formula: M * ln(RSS/M) + k * ln(M)
                    bic = M * np.log(max(rss, 1e-10) / M) + k * np.log(M)
                    
                    results.append({'k': k, 'rss': rss, 'mse': mse, 'bic': bic, 'coeffs': coeffs})
                    
                    print(f"{k:>3} | {rss:>10.4f} | {mse:>10.6f} | {bic:>12.4f}")
                    sys.stdout.flush()
                    
                    # Update best markers based on fit measures
                    if mse < best_mse:
                        best_mse, best_mse_k, best_mse_coeffs = mse, k, coeffs
                    
                    if bic < best_bic:
                        best_bic, best_bic_k, best_bic_coeffs = bic, k, coeffs
                else:
                    print(f"{k:>3} | Optimization failed")
                    sys.stdout.flush()
    except Exception as env_err:
        print(f"CRITICAL ERROR in Env: {env_err}")
        sys.stdout.flush()

    # Final Summary
    print("-" * 45)
    print(f"Best Cardinality (MSE): {best_mse_k} (MSE: {best_mse:.6f})")
    print(f"Best Cardinality (BIC): {best_bic_k} (BIC: {best_bic:.4f})")

    # --- PERSISTENCE: Save results to disk ---
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "best_subset_results.txt")
    with open(output_file, "w") as f:
        f.write("Best Subset Selection Results (Full MIQP Formulation)\n")
        f.write("====================================================\n\n")
        f.write(header + "\n")
        f.write("-" * 45 + "\n")
        for res in results:
            f.write(f"{res['k']:>3} | {res['rss']:>10.4f} | {res['mse']:>10.6f} | {res['bic']:>12.4f}\n")
        
        f.write("\n" + "=" * 45 + "\n")
        f.write(f"Best Cardinality (MSE): {best_mse_k}\n")
        f.write(f"Minimum MSE: {best_mse:.6f}\n")
        f.write(f"Best Cardinality (BIC): {best_bic_k}\n")
        f.write(f"Minimum BIC: {best_bic:.4f}\n\n")
        
        # Log Coefficients for the two selected optimal models
        for criterion, k, coeffs in [("MSE", best_mse_k, best_mse_coeffs), ("BIC", best_bic_k, best_bic_coeffs)]:
            f.write(f"Critical Predictors for Best {criterion} (k={k}):\n")
            f.write(f"{'Predictor Name':<30} | {'Coefficient':>12}\n")
            f.write("-" * 45 + "\n")
            if coeffs:
                for j, val in coeffs.items():
                    if abs(val) > 1e-6:
                        name = feature_names[j-1]
                        f.write(f"{name:<30} | {val:>12.6e}\n")
            f.write("\n")
            
    print(f"\nResults saved to: {output_file}")
    sys.stdout.flush()
    
    return (best_mse_k, best_bic_k), (best_mse, best_bic), (best_mse_coeffs, best_bic_coeffs)
```

### Main Execution

To run the script, define the `DATA_PATH` variable with the correct file location for your input data.


```python
if __name__ == "__main__":
    DATA_PATH = "/Users/jmmoon/Documents/GitHub/mipml/hw1/MIP4ML/Communities_and_crime.csv"
    # Search range from 5 predictors to 40 predictors
    best_k, min_mse, coeffs = run_iterative_selection(DATA_PATH, k_range=range(5, 100))
```


### Data preprocessing

The following script reads a **CSV file** and preprocesses the data into coefficients for a **Gurobi optimization model**. 

> **Important:** Please ensure the `csv_path` variable is correctly set to your file location before running the script.

```python
import pandas as pd
import numpy as np

def preprocess_crime_data(file_path):
    """
    Loads, cleans, and standardizes the Communities and Crime dataset, 
    then formats it into 1-indexed dictionaries for Gurobi optimization.
    """
    
    # --- 1. DATA LOADING ---
    # Read the raw CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # --- 2. BASIC CLEANING ---
    # Filter only numeric columns as MIP4ML targets quantitative regression features
    df_numeric = df.select_dtypes(include=[np.number])
    
    # Target variable (the label we want to predict)
    target_col = 'ViolentCrimesPerPop'
    if target_col not in df_numeric.columns:
        raise ValueError(f"Target column {target_col} not found in numeric columns.")
        
    y_raw = df_numeric[target_col].values
    X_raw = df_numeric.drop(columns=[target_col]).values
    feature_names = df_numeric.drop(columns=[target_col]).columns.tolist()
    
    # M: Number of observations (rows)
    # num_features: Number of potential predictors (columns)
    M = len(y_raw)
    num_features = X_raw.shape[1]
    
    # --- 3. STANDARDIZATION ---
    # Scale features to mean=0 and std=1 to ensure the Big-M parameter (L) 
    # and regularization (lambda) apply uniformly across different units.
    X_mean = np.mean(X_raw, axis=0)
    X_std = np.std(X_raw, axis=0)
    
    # Prevent division by zero if a feature has zero variance
    X_std[X_std == 0] = 1.0
    X_scaled = (X_raw - X_mean) / X_std
    
    # --- 4. FORMAT FOR GUROBI (1-Indexed Mapping) ---
    # Gurobi models often use sets ranging from 1..N. Here we map 
    # observation and feature indices to 1-indexed dictionaries.
    
    # features: A list of 1-indexed feature identifiers [1, 2, ..., P]
    features = list(range(1, num_features + 1))
    features0 = features 
    
    # A: Dictionary mapping (i, j) pairs to the value of feature j for observation i
    A = {}
    for i in range(M):
        for j in range(num_features):
            # Key format: (observation_index, feature_index)
            A[(i + 1, j + 1)] = X_scaled[i, j]
            
    # y: Dictionary mapping observation index i to the target value
    y = {i + 1: y_raw[i] for i in range(M)}
    
    return M, features, features0, A, y, feature_names

if __name__ == "__main__":
    # Test script for preprocessing
    csv_path = "YOUR_PATH"
    M, features, features0, A, y, feature_names = preprocess_crime_data(csv_path)
    print(f"# Data Preprocessing Complete:")
    print(f"  Observations (M): {M}")
    print(f"  Features: {len(features)}")
    print(f"  Target sample y[1]: {y[1]:.4f}")
```
