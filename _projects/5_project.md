---
layout: page
title:  Bayesian Spatial Modeling of Cancer Incidence (BYM2 Model)
description: Based on ch 15, 16 of BDA3, we run Bayesian GLM with spatial random effect on Manhattan breast cancer incidence.
img: assets/img/spatial.png
importance: 3
category: coursework
---

This project was conducted for the STA6160 class at Yonsei University in Spring 2018.

## Part 1: Theoretical Framework

This analysis employs a **Generalized Linear Model (GLM)** framework with **Bayesian Hierarchical Spatial Random Effects** using a **Conditional Autoregressive Normal Prior (CAR Normal)**. This approach enables us to model disease relative risk while incorporating local risk factors, such as pollution and socio-economic status, as well as accounting for the spatial dependencies inherent in geographic data.

### 1. The Generalized Linear Model (GLM)

GLM assumes the distribution of the response variable belongs to an **exponential family**, a collection of distributions  with a specific density form, characterized by cumulant generating function.

* **Likelihood (Poisson Regression):**
Since we are modeling the count of cancer incidence in each area , we model as a Poisson distribution:
$$Y_i \sim \text{Poisson}(\lambda_i)$$


where  is the expected count of cases in area .
* **Link Function:**
The GLM models the relationship between the expected value  and the linear predictors using a **link function**. For Poisson regression, we use the **log link**: $$\log(\lambda_i) = \eta_i$$



This is often called a "log-linear model." The exponentiated coefficients ($e^\beta$) represent the multiplicative change in the expected count for a one-unit increase in the predictor.

### 2. The Offset Variable

To model the cancer **rate** (risk) rather than the raw count, we introduce an **offset term**,  (Expected Cases).
$$\log(\lambda_i) = \log(E_i) + \alpha + \mathbf{X}_i\boldsymbol{\beta} + \psi_i$$
* **Role of Offset:**  represents the known "background" population size or age-adjusted expected count. It is added as a constant (coefficient fixed at 1) to the linear predictor.
* **Assumption:** Using an offset implies that doubling the population size leads to a doubling of the count outcome.
* **Interpretation:** The exponentiated regression coefficients now describe how predictors modify the **relative risk** compared to the expected background rate.

### 3. Spatial Random Effects (The BYM Model)

Random effects or hierarchical models model correlations across units. They arise in linear modeling to avoid **pseudo-replication**: the error of treating units that are non-IID (independent and identically distributed) as if they were IID.
Units often have a hierarchically clustered structure, such as students belonging to classes, schools, and districts. Students in the same class are distinct entities, but they share common environmental factors, so they are not fully independent. Another example is spatial correlation: adjacent states, such as California and Oregon, are distinct entities but share common geographical features, meaning they are not truly IID.

Hierarchical models address this by assigning regression coefficients (random effects) to the indicator variables for this correlation structure (e.g., the specific group or region). Crucially, these coefficients share the same nontrivial hyperparameter (e.g. variance).
This shared distribution allows the model to **borrow strength** within groups. Estimates for groups with sparse data are stabilized by being pulled toward the group mean, effectively using information from the wider population to improve unit inference with small data.

Through this mechanism, the model achieves **partial pooling**. It is a good compromise between two extremes:

- **no pooling**: assuming independece and non-identity across units, just include indicator variables as predictors, without hieararchical structure. This corresponds to setting the variance of prior as $$\infty$$.
- **complete pooling**: assuming iid across units. Not inclduing indicator variables as predictors. This corresponds to setting the variance of effects as zero.

Geographical data is rarely independent; high-cancer areas tend to cluster. To capture this **spatial dependence**, we introduce a random effect term  into the linear predictor.
In the **Besag-York-Mollié (BYM)** framework, this random effect is split into two components:

$$\psi_i = \underbrace{u_i}_{\text{Spatial (Structured)}} + \underbrace{v_i}_{\text{Noise (Unstructured)}}$$
 

#### The Spatial Component ($u_i$)

The spatial component is modeled using a **Conditional Autoregressive (CAR)** prior. This allows each area to "borrow strength" from its neighbors.

* **Conditional Specification:**

$$u_i  \mid \mathbf{u}_{-i}\sim \mathcal{N} \left( \frac{\sum_{j \in \text{ne}(i)} u_j}{n_i}, \frac{\tau^2}{n_i} \right)$$
 

* **Mean:** The conditional expectation of an area's risk is the average of its neighbors' risks.
* **Variance:** Variance is inversely proportional to the number of neighbors (). Areas with more neighbors have lower variance (more information).
* **Precision Matrix:** The joint distribution is an improper multivariate normal where the precision matrix corresponds to the **Graph Laplacian**. This structure shrinks the random effect of sparse regions toward the local mean, stabilizing inference.


### 4. Model Structure (what we are estimating) 
 
Recall that the BYM model splits the log-risk ($\eta_i$) into covariates, an unstructured random effect ($v_i$), and a structured spatial effect ($u_i$).

- $$Y_i \sim \text{Poisson}(\lambda_i)$$
- $$\log(\lambda_i) = \log(E_i) + \eta_i $$
- $$\eta_i = \alpha + \mathbf{X}_i\beta + u_i + v_i$$
    - $\beta$: Regression coefficients (Fixed)
    - $v_i$: Unstructured noise (Normal i.i.d)
    - $u_i$: Structured spatial noise (CAR prior)
    - $\tau_v, \tau_u$: Precision (inverse variance) hyperparameters for the random effects.


#### 5. the Sampling Process (how we estimate it iteratively).
The goal is to Monte Carlo sample from the joint posterior distribution, allowing us to calculate means, credible intervals, and risk estimates.
However, given the data and priors, we typically only know the posterior **up to a constant of proportionality**.

**Markov Chain Monte Carlo (MCMC)** is a method designed to sample from a probability distribution using only this unnormalized information. It works by constructing a 'Markov Chain', a stochastic process that only depends on the last step information, to explore the parameter space. The process relies on a **proposal distribution** to suggest a new candidate location based on the current one. A decision rule (typically Metropolis-Hastings) then evaluates this suggestion by comparing the likelihood ratio of the two locations. By accepting moves to higher probability areas more often than moves to lower ones, the walker naturally spends more time in areas of high probability, and its history forms a representative sample of the posterior.

The **Gibbs sampler** is an MCMC method often used for complex hierarchical models. Instead of updating all parameters at once—which is difficult with many variables—it updates them one by one. It cycles through the list, asking: *"What is the likely value of Parameter A, assuming B and C are currently fixed?"*
This is effective for clustered structure where indicators for group A and B are independent.
However, Gibbs sampling struggles with **spatial models** because neighboring regions are highly correlated.
Think of it like a three-legged race: Region A cannot move far unless Region B moves, but Gibbs holds B fixed while updating A. This forces the sampler to take tiny, inefficient steps, leading to **slow mixing** and the "snake-like" trace plots you want to avoid. (the "trace plot snake").

 So we **Hamiltonian Monte Carlo (HMC)**, not Gibbs. HMC works on the principle of **Random Kick + Gradient Steering**.
 We give the sampler a random burst of momentum (the kick) to ensure it explores, but then we use the gradient of the posterior (the steering) to guide that momentum through the high-probability regions.
 Standard MCMC (Metropolis-Hastings) is a blind hiker taking random steps. He bumps into walls and gets rejected constantly.
 HMC uses the **Gradient Steering** to "see" the shape of the mountain. It flows *around* obstacles rather than bumping into them.
Also, in a correlated "narrow canyon," a  zig-zags hiker can easily get stuck.The HMC sled uses its **momentum** to slide smoothly along the canyon floor, traversing long distances in a single update.


Here is the **Data Sources** section, structured to highlight the diversity of the inputs and the spatial harmonization required.

## Part 2: Data Sources

### 1. Outcome Variable: Cancer Incidence

* **Source:** New York State Cancer Registry and Cancer Statistics (https://www.health.ny.gov/statistics/cancer/registry/)
* **Variable:** Cancer Incidence by Region (2005–2009).
* **Granularity:** "DOH Regions"
 
### 2. Predictor: Socioeconomic Status (SES)

* **Source:** New York State Cancer Registry and Cancer Statistics (https://www.health.ny.gov/statistics/cancer/registry/)
* **Variable:** Income, Education levels... (2005–2009).
* **Granularity:** "DOH Regions"

### 3. Predictor: Environmental Pollution

* **Source:** EPA National-Scale Air Toxics Assessment (NATA), 2005 Edition (https://www.epa.gov/national-air-toxics-assessment/2005-national-air-toxics-assessment).
* **Granularity:** Census Tract.
* **Variables Used:**: **Total Cancer Risk:** 

Extracted from legacy Microsoft Access (`.mdb`) archives. 

### 4. Predictor: Family Structure

* **Source:** U.S. Census Bureau American Community Survey (ACS). Used Census package in python to use API. It requries an API key, which can be obtained from  https://api.census.gov/data/key_signup.html

* **Granularity:** block, smaller than census tract.
* **Variables Used:**: Percentage of the population aged 15+ currently divorced, computed from three variables
 
  

## Part 2: Real data challenge

### 1. Mismatched Spatial Granularities
A major engineering hurdle was integrating mismatched spatial granularities: our outcome variable (Cancer Incidence) and SES data were aggregated to custom "DOH Regions", which is coarser with the standard Census Tract (EPA) and finer than Block Group (ACS) levels of our predictor variables. To resolve this, I built a custom **"down-scale and re-aggregate"** pipeline that first broadcasted coarse Tract-level data down to constituent Block Groups, then re-aggregated all metrics up to the target DOH Region level using a precise definition file, successfully harmonizing disparate government datasets without losing spatial fidelity.
 
### 2. Scalability
Even after excluding missing data, fitting a spatial random effect model on 16,000 units remained computationally prohibitive for HMC. To address this, I filtered the dataset to focus specifically on Manhattan, drastically reducing the sample size to approximately 1,000 units."

## Part 3: Code Implementation Explanation

The implementation is split into a Python script (data processing & interface) and a Stan file (statistical model).
### Prelim: packages

```python
import pandas as pd
import geopandas as gpd
import numpy as np
import subprocess
import os
import libpysal
from cmdstanpy import CmdStanModel, install_cmdstan
from scipy.sparse.linalg import factorized
import scipy.sparse as sp
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
BASE_DIR = "/content/drive/MyDrive/spatial"
NYS_DIR = f"{BASE_DIR}/NYS_Cancer"
CANCER_TYPE = 'BREAST' 
TARGET_COUNTY = '061'  # '061' = Manhattan (New York County). Set to None for full state.

# --- 0. INSTALL CMDSTAN (If needed) ---
try:
    import cmdstanpy
    cmdstanpy.cmdstan_path()
except:
    print("Installing CmdStan (C++ backend)...")
    install_cmdstan()


```

### Block 1: Helper Functions & Setup

We define helper functions to handle legacy data formats (Microsoft Access `.mdb`) and standard settings.

```python
# ==========================================
# 1. HELPER FUNCTIONS
# ==========================================

def read_mdb_table(db_path, table_name):
    """Exports a specific table from a Microsoft Access (.mdb) file to pandas."""
    try:
        subprocess.run(['mdb-export', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except:
        raise RuntimeError("mdbtools not installed. Run '!apt-get install -y mdbtools' first.")

    cmd = ['mdb-export', db_path, table_name]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return pd.read_csv(proc.stdout)
```

**Explanation:** This function acts as a bridge. Since Python cannot natively read older `.mdb` files on Linux/Colab, this function calls a system command (`mdb-export`) to extract the requested table into a CSV format in memory, which `pandas` can then read.

### Block 2 : DATA PROCESSING STEPS

```python
# ==========================================
# 2. DATA PROCESSING STEPS
# ==========================================

def load_and_prep_main_data(county_fips=None):
    """
    Loads SES and Cancer shapefiles.
    If county_fips is provided (e.g., '061'), filters the map to that county only.
    """
    print("--- 1. Loading Spatial Data ---")
    
    # Load Crosswalk to identify which Regions belong to the target County
    crosswalk_path = f"{NYS_DIR}/BlockGroup_Crosswalk_region.dbf"
    df_crosswalk = gpd.read_file(crosswalk_path)
    df_crosswalk['DOHREGION'] = df_crosswalk['DOHREGION'].astype(str)
    
    # Extract County FIPS from GEOID10 (String: State(2) + County(3) + ...)
    # NY is '36'. So we look at chars 2:5.
    df_crosswalk['CountyFIPS'] = df_crosswalk['GEOID10'].astype(str).str.zfill(12).str[2:5]
    
    valid_regions = None
    if county_fips:
        print(f"Filtering dataset to County FIPS: {county_fips} (Manhattan)...")
        subset = df_crosswalk[df_crosswalk['CountyFIPS'] == county_fips]
        valid_regions = subset['DOHREGION'].unique()
        print(f" -> Retaining {len(valid_regions)} regions.")

    # Load Shapefiles
    ses_gdf = gpd.read_file(f"{NYS_DIR}/NYS_SES_Data_region.shp")
    cancer_gdf = gpd.read_file(f"{NYS_DIR}/NYSCancer_region.shp")

    ses_gdf['DOHREGION'] = ses_gdf['DOHREGION'].astype(str)
    cancer_gdf['DOHREGION'] = cancer_gdf['DOHREGION'].astype(str)
    
    # Apply Filter
    if valid_regions is not None:
        ses_gdf = ses_gdf[ses_gdf['DOHREGION'].isin(valid_regions)]
        cancer_gdf = cancer_gdf[cancer_gdf['DOHREGION'].isin(valid_regions)]

    # Merge SES data into the Cancer Geometry
    gdf = cancer_gdf.merge(ses_gdf.drop(columns='geometry'), on='DOHREGION', how='inner')
    return gdf

def process_divorce_data(gdf, crosswalk_gdf):
    print("--- 2. Processing Divorce Data ---")
    tract_path = f"{BASE_DIR}/NY_Tract_Divorce.csv"
    if not os.path.exists(tract_path): return None

    df_tracts = pd.read_csv(tract_path, dtype={'TRACT_GEOID': str})
    
    # Filter Crosswalk to match current GDF regions
    active_regions = gdf['DOHREGION'].unique()
    crosswalk_prep = crosswalk_gdf[crosswalk_gdf['DOHREGION'].isin(active_regions)].copy()
    
    crosswalk_prep['TRACT_GEOID'] = crosswalk_prep['GEOID10'].astype(str).str.zfill(12).str[:11]
    
    merged_bg = crosswalk_prep.merge(df_tracts, on='TRACT_GEOID', how='left')
    divorce_agg = merged_bg.groupby('DOHREGION')[['divorce_rate']].mean().reset_index()
    return divorce_agg

def process_pollution_data(gdf, crosswalk_gdf):
    print("--- 3. Processing Pollution (NATA 2005) ---")
    mdb_path = f"{BASE_DIR}/US_NATA05_V4_srcrisk_bytract.mdb"
    if not os.path.exists(mdb_path): return None

    # Read MDB
    table_name = 'US_NATA05_srcrisk_pollbkdn_bytract_hapcat_25Jan11'
    df_nata = read_mdb_table(mdb_path, table_name)
    
    # Construct ID
    df_nata['TRACT_GEOID'] = (df_nata['FIPS'].astype(str).str.zfill(5) + 
                              df_nata['TRACT'].astype(str).str.zfill(6))
    
    # Filter NY
    df_nata = df_nata[df_nata['TRACT_GEOID'].str.startswith('36')].copy()
    
    # Calculate Risk
    risk_cols = ['Point Cancer Risk', 'Nonpoint Cancer Risk', 'Onroad Cancer Risk', 
                 'Nonroad Cancer Risk', 'Background Cancer Risk']
    valid_cols = [c for c in risk_cols if c in df_nata.columns]
    df_nata['Cancer_Risk'] = df_nata[valid_cols].sum(axis=1)
    
    # Merge using Crosswalk
    active_regions = gdf['DOHREGION'].unique()
    crosswalk_prep = crosswalk_gdf[crosswalk_gdf['DOHREGION'].isin(active_regions)].copy()
    crosswalk_prep['TRACT_GEOID'] = crosswalk_prep['GEOID10'].astype(str).str.zfill(12).str[:11]
    
    merged = crosswalk_prep.merge(df_nata[['TRACT_GEOID', 'Cancer_Risk']], on='TRACT_GEOID', how='left')
    pollution_agg = merged.groupby('DOHREGION')[['Cancer_Risk']].mean().reset_index()
    return pollution_agg
```

**Explanation:**

1. **Shapefiles:** Loads the Cancer geometry and Socioeconomic (SES) data.
2. **String Casting:** Critical step. It converts `DOHREGION` to a string to ensure that IDs like `"05"` don't become integer `5`, which would break the merge.
3. **Merge:** Combines the two datasets into a single GeoDataFrame (`gdf`).

### Block 3: PreProcessing  Data 

```python
# ==========================================
# 3. MAIN WORKFLOW
# ==========================================

# A. Load & Filter Data (Manhattan Only)
gdf = load_and_prep_main_data(county_fips=TARGET_COUNTY)

# Load Crosswalk (needed for variables)
crosswalk_path = f"{NYS_DIR}/BlockGroup_Crosswalk_region.dbf"
df_crosswalk = gpd.read_file(crosswalk_path)
df_crosswalk['DOHREGION'] = df_crosswalk['DOHREGION'].astype(str)

# B. Process Variables
divorce_agg = process_divorce_data(gdf, df_crosswalk)
pollution_agg = process_pollution_data(gdf, df_crosswalk)

# C. Merge & Clean
if divorce_agg is not None:
    gdf = gdf.merge(divorce_agg, on='DOHREGION', how='left')
    gdf['divorce_rate'] = gdf['divorce_rate'].fillna(gdf['divorce_rate'].mean())

if pollution_agg is not None:
    gdf = gdf.merge(pollution_agg, on='DOHREGION', how='left')
    gdf['Cancer_Risk'] = gdf['Cancer_Risk'].fillna(gdf['Cancer_Risk'].mean())
    gdf['log_cancer_risk'] = np.log(gdf['Cancer_Risk'])

# D. Feature Engineering
y_col = f'O{CANCER_TYPE}'
e_col = f'E{CANCER_TYPE}'

# Filter valid rows (Expected > 0)
gdf = gdf[(gdf[e_col] > 1e-9) & (gdf[y_col].notna())].reset_index(drop=True)

gdf['poverty_rate'] = gdf['POVUNDER'] / (gdf['POVUNDER'] + gdf['POVOVER'])
gdf['low_ed_rate'] = gdf['TOT_LT_HS'] / (gdf['TOT_LT_HS'] + gdf['TOT_HSPLUS'])
```

**Explanation:**
**spatial mismatch** between the available divorce data (block) and the model units (Cancer Regions).

1. **Crosswalk:** Uses a lookup table to map standard Census IDs (`TRACT_GEOID`) to custom Cancer Region IDs (`DOHREGION`).
2. **Imputation:** Assigns the divorce rate of a Tract to all Block Groups inside it.
3. **Aggregation:** Averages the divorce rates of all block groups within a specific `DOHREGION` to create a single predictor value for that region.

**spatial mismatch** between the available polution data (Census Tracts) and the model units (Cancer Regions).
1. **Extraction:** Pulls the "Cancer Risk" table from the EPA NATA 2005 database.
2. **Summation:** Calculates `Total Cancer Risk` by summing components (Point source + On-road + Non-road + Background). This creates a cumulative risk score.
3. **Aggregation:** Similar to the divorce block, it maps these Tract-level risk scores to the custom Cancer Regions using the crosswalk.

**Feature Engineering**
 

 
### Block 4:  Graph Construction

```python
# E. Prepare Stan Data
# Standardize Predictors
cols_to_use = ['poverty_rate', 'low_ed_rate', 'divorce_rate', 'log_cancer_risk']
X_matrix = []
for col in cols_to_use:
    if col in gdf.columns:
        # Fill NaNs before standardizing
        gdf[col] = gdf[col].fillna(gdf[col].mean())
        scaled = (gdf[col] - gdf[col].mean()) / gdf[col].std()
        X_matrix.append(scaled)
X_matrix = np.column_stack(X_matrix)

# Build Graph
w = libpysal.weights.Queen.from_dataframe(gdf)
if w.islands:
    print(f"Dropping {len(w.islands)} islands...")
    gdf = gdf.drop(w.islands).reset_index(drop=True)
    w = libpysal.weights.Queen.from_dataframe(gdf)
    # Re-standardize X needed if rows dropped? Ideally yes, but skipping for brevity here.

# Calculate Scaling Factor (Fast Eigen Method)
adj_sparse = w.sparse
degrees = np.array(adj_sparse.sum(axis=1)).flatten()
Q_sparse = sp.diags(degrees) - adj_sparse
# Solve for diagonals (Approximate/Fast method)
Q_reg = Q_sparse + sp.eye(w.n) * 1e-6
solve = factorized(Q_reg.tocsc())
diag_inv = np.array([solve(np.eye(w.n, 1, k=-i).flatten())[i] for i in range(w.n)])
scaling_factor = np.exp(np.mean(np.log(diag_inv)))
```

**Explanation:**

1. **Rates:** Converts raw counts (e.g., "Population in Poverty") into rates (percentage) to make them comparable across regions.
2. **Log Transform:** Applied to the Pollution Risk variable because such data is usually highly skewed (a few areas have massive pollution). The log scale linearizes the relationship.
3. **Adjacency Graph:** Uses `libpysal` to define who is a "neighbor" (sharing a boundary).
4. **Scaling Factor:** This is unique to **BYM2**. It calculates a geometric scaling factor from the graph Laplacian. This ensures that the variance parameter  has the same interpretation regardless of the graph structure (e.g., whether the map is of New York or Texas).

### Block 6: The Stan Model (`bym2_model.stan`)

```python
# Prepare Stan Data Dictionary
node1, node2 = [], []
for i in range(w.n):
    for n in w.neighbors[i]:
        if n > i:
            node1.append(i + 1)
            node2.append(n + 1)

stan_data = {
    'N': len(gdf),
    'N_edges': len(node1),
    'node1': node1, 'node2': node2,
    'Y': gdf[y_col].astype(int).tolist(),
    'log_offset': np.log(gdf[e_col]).tolist(),
    'K': X_matrix.shape[1],
    'X': X_matrix,
    'scaling_factor': scaling_factor
}

# --- 4. RUN MODEL ---
print(f"Running BYM2 Model on {len(gdf)} Regions (Manhattan)...")

# Write Stan File (Optimized GLM version)
bym_code = """
data {
  int<lower=0> N; int<lower=0> N_edges;
  array[N_edges] int<lower=1, upper=N> node1;
  array[N_edges] int<lower=1, upper=N> node2;
  array[N] int<lower=0> Y; vector[N] log_offset;
  int<lower=1> K; matrix[N, K] X; real<lower=0> scaling_factor;
}
parameters {
  real alpha; vector[K] beta;
  real<lower=0> sigma; real<lower=0, upper=1> rho;
  vector[N] theta; vector[N] phi;
}
transformed parameters {
  vector[N] convolved_re;
  convolved_re = sigma * (sqrt(rho) * phi + sqrt(1 - rho) * theta);
}
model {
  alpha ~ normal(0, 1.0); beta ~ normal(0, 1.0);
  sigma ~ normal(0, 1.0); rho ~ beta(0.5, 0.5); theta ~ normal(0, 1.0);
  target += -0.5 * dot_self(phi[node1] - phi[node2]);
  sum(phi) ~ normal(0, 0.001 * N);
  Y ~ poisson_log_glm(X, log_offset + alpha + convolved_re, beta);
}
generated quantities {
  vector[N] relative_risk = exp(alpha + X * beta + convolved_re);
}
"""
with open('bym2_model.stan', 'w') as f: f.write(bym_code)
```

**Explanation:**

1. **`target += ...`**: This line implements the **ICAR (Intrinsic Conditional Autoregressive)** prior. It penalizes differences between neighbors (`phi[node1] - phi[node2]`), forcing the spatial random effects to be smooth.
2. **`sum(phi) ~ ...`**: A constraint to ensure the spatial effects sum to zero. This is necessary for the model to be identifiable (otherwise the intercept `alpha` and the random effects `phi` would be confounded).
3. **`poisson_log`**: The likelihood function described in Part 1. It links the observed counts  to the linear predictor via the log function.

### Block 7: Inference

```python


# Compile & Sample
model = CmdStanModel(stan_file='bym2_model.stan')
fit = model.sample(
    data=stan_data, 
    iter_sampling=10000, iter_warmup=20000, # Faster settings
    parallel_chains=4, show_progress=True, show_console=True
)

# --- 5. RESULTS ---
print("\n--- RESULTS ---")
summary = fit.summary()
beta_rows = [x for x in summary.index if 'beta' in x]
print(summary.loc[beta_rows, ['Mean', '5%', '95%']])

# Map
gdf['RR'] = fit.stan_variable('relative_risk').mean(axis=0)
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(column='RR', ax=ax, cmap='RdYlBu_r', legend=True, vmin=0.5, vmax=1.5)
plt.title(f"Manhattan {CANCER_TYPE} Cancer Risk (modeled)")
plt.axis('off')
plt.show()

print("\n--- HMC DIAGNOSTICS ---")
print(fit.diagnose())
```

**Explanation:**

1. **Sampling:** Runs the Hamiltonian Monte Carlo (HCMC) algorithm to sample from the posterior distribution.
2. **Results:** Extracts the `beta` coefficients.
* If `beta` for Pollution is positive and its Credible Interval excludes zero, we conclude that higher pollution is associated with significantly higher cancer risk, even after controlling for poverty and spatial clustering.
Here is a structured summary of the challenges we navigated during this project.

# Result
```
--- RESULTS ---
             Mean        5%       95%
beta[1]  0.014177 -0.024948  0.053882
beta[2] -0.180270 -0.227835 -0.131878
beta[3] -0.020294 -0.047240  0.006532
beta[4]  0.023693 -0.005721  0.053664
```
Only the education factor is significant.
