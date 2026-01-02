---
layout: page
title:  Bayesian Spatial Modeling of Cancer Incidence (BYM2 Model)
description: a project with a background image
img: assets/img/spatial.png
importance: 3
category: fun
---
 
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


 

## Part 2: Code Implementation Explanation

The implementation is split into a Python script (data processing & interface) and a Stan file (statistical model).

### Block 1: Helper Functions & Setup

We define helper functions to handle legacy data formats (Microsoft Access `.mdb`) and standard settings.

```python
def read_mdb_table(db_path, table_name):
    # ... uses 'mdb-export' to convert Access tables to CSV ...

```

**Explanation:** This function acts as a bridge. Since Python cannot natively read older `.mdb` files on Linux/Colab, this function calls a system command (`mdb-export`) to extract the requested table into a CSV format in memory, which `pandas` can then read.

### Block 2: Data Loading & Geometry (`load_and_prep_main_data`)

```python
def load_and_prep_main_data():
    ses_gdf = gpd.read_file(".../NYS_SES_Data_region.shp")
    cancer_gdf = gpd.read_file(".../NYSCancer_region.shp")
    # ... casting IDs to string ...
    gdf = cancer_gdf.merge(ses_gdf, on='DOHREGION', ...)

```

**Explanation:**

1. **Shapefiles:** Loads the Cancer geometry and Socioeconomic (SES) data.
2. **String Casting:** Critical step. It converts `DOHREGION` to a string to ensure that IDs like `"05"` don't become integer `5`, which would break the merge.
3. **Merge:** Combines the two datasets into a single GeoDataFrame (`gdf`).

### Block 3: Processing Divorce Data (`process_divorce_data`)

```python
def process_divorce_data(crosswalk_gdf):
    df_tracts = pd.read_csv(".../NY_Tract_Divorce.csv")
    # ... crosswalk logic ...
    merged_bg = crosswalk_prep.merge(df_tracts, on='TRACT_GEOID', ...)
    divorce_agg = merged_bg.groupby('DOHREGION').mean()

```

**Explanation:**
This block handles the **spatial mismatch** between the available divorce data (Census Tracts) and the model units (Cancer Regions).

1. **Crosswalk:** Uses a lookup table to map standard Census IDs (`TRACT_GEOID`) to custom Cancer Region IDs (`DOHREGION`).
2. **Imputation:** Assigns the divorce rate of a Tract to all Block Groups inside it.
3. **Aggregation:** Averages the divorce rates of all block groups within a specific `DOHREGION` to create a single predictor value for that region.

### Block 4: Processing Pollution Data (`process_pollution_data`)

```python
def process_pollution_data(crosswalk_gdf):
    df_nata = read_mdb_table(..., 'US_NATA05_srcrisk...')
    # ... filter for NY (FIPS 36) ...
    df_nata['Cancer_Risk'] = df_nata[risk_cols].sum(axis=1)
    # ... merge and aggregate ...

```

**Explanation:**

1. **Extraction:** Pulls the "Cancer Risk" table from the EPA NATA 2005 database.
2. **Summation:** Calculates `Total Cancer Risk` by summing components (Point source + On-road + Non-road + Background). This creates a cumulative risk score.
3. **Aggregation:** Similar to the divorce block, it maps these Tract-level risk scores to the custom Cancer Regions using the crosswalk.

### Block 5: Feature Engineering & Graph Construction

```python
# Create Predictors
gdf['poverty_rate'] = gdf['POVUNDER'] / (gdf['POVUNDER'] + gdf['POVOVER'])
# ... log transforms ...

# Build Graph
w = libpysal.weights.Queen.from_dataframe(gdf)
# ... Scaling Factor Calculation ...
scaling_factor = np.exp(np.mean(np.log(diag_inv)))

```

**Explanation:**

1. **Rates:** Converts raw counts (e.g., "Population in Poverty") into rates (percentage) to make them comparable across regions.
2. **Log Transform:** Applied to the Pollution Risk variable because such data is usually highly skewed (a few areas have massive pollution). The log scale linearizes the relationship.
3. **Adjacency Graph:** Uses `libpysal` to define who is a "neighbor" (sharing a boundary).
4. **Scaling Factor:** This is unique to **BYM2**. It calculates a geometric scaling factor from the graph Laplacian. This ensures that the variance parameter  has the same interpretation regardless of the graph structure (e.g., whether the map is of New York or Texas).

### Block 6: The Stan Model (`bym2_model.stan`)

```stan
model {
  // Priors
  target += -0.5 * dot_self(phi[node1] - phi[node2]); // The CAR prior
  sum(phi) ~ normal(0, 0.001 * N); // Soft sum-to-zero constraint
  
  // Likelihood (GLM)
  Y ~ poisson_log(log_offset + alpha + X * beta + convolved_re);
}

```

**Explanation:**

1. **`target += ...`**: This line implements the **ICAR (Intrinsic Conditional Autoregressive)** prior. It penalizes differences between neighbors (`phi[node1] - phi[node2]`), forcing the spatial random effects to be smooth.
2. **`sum(phi) ~ ...`**: A constraint to ensure the spatial effects sum to zero. This is necessary for the model to be identifiable (otherwise the intercept `alpha` and the random effects `phi` would be confounded).
3. **`poisson_log`**: The likelihood function described in Part 1. It links the observed counts  to the linear predictor via the log function.

### Block 7: Inference

```python
model = CmdStanModel(stan_file='bym2_model.stan')
fit = model.sample(...)
summary = fit.summary()

```

**Explanation:**

1. **Sampling:** Runs the Hamiltonian Monte Carlo (HCMC) algorithm to sample from the posterior distribution.
2. **Results:** Extracts the `beta` coefficients.
* If `beta` for Pollution is positive and its Credible Interval excludes zero, we conclude that higher pollution is associated with significantly higher cancer risk, even after controlling for poverty and spatial clustering.
Here is a structured summary of the challenges we navigated during this project.

 

### 1. Data Engineering Challenges (The "Messy Real-World Data" Story)

**Challenge: Integrating Mismatched Spatial Granularities ( The "Crosswalk" Problem)**

* **The Situation:** Our outcome variable (Cancer Incidence) was aggregated to custom "DOH Regions" (clusters of block groups) to protect patient privacy. However, our predictor variables came from disparate government sources at different levels: Census Tracts (Divorce, NATA Pollution) and Block Groups (SES).
* **The Action:** I built a custom **Spatial Crosswalk Pipeline**.
* I loaded a definition file linking Block Groups to Cancer Regions.
* I engineered a "down-scale and re-aggregate" logic: Data at the Tract level was broadcast down to constituent Block Groups, then re-aggregated (averaged) up to the custom Cancer Region level.


* **The Result:** Successfully merged three disparate datasets into a single analytical dataframe without losing spatial fidelity.

**Challenge: Accessing Legacy Infrastructure (The ".mdb" Problem)**

* **The Situation:** The specific pollution data required for the study period (2005 NATA) was only available in an archived Microsoft Access Database (`.mdb`) format, which is not natively supported in modern Linux/Python CI/CD environments (like Colab).
* **The Action:** I implemented a workaround using the `mdbtools` system utility.
* I wrote a Python wrapper function that subprocessed shell commands to extract specific tables from the proprietary database into memory as CSVs, bypassing the need for a Windows environment.


* **The Result:** Automated the extraction of 2005-era pollution risk data, enabling the inclusion of a critical environmental predictor that would have otherwise been inaccessible.

**Challenge: Handling Missing and Zero-Inflated Data (The "NaN" Crash)**

* **The Situation:** The Stan MCMC engine kept crashing with `Log probability is NaN`.
* **The Action:** I diagnosed two root causes:
* **Division by Zero:** Some areas had 0 population, causing `Count / Pop` calculations to explode to Infinity.
* **Log(0):** Calculating `log(Expected_Cases)` for areas with 0 expected cases resulted in `-Infinity`.
* I implemented a robust **Data Cleaning & Imputation Step** prior to modeling, replacing infinities with NaNs, imputing missing values with column means, and filtering out invalid rows.



---

### 2. Statistical Modeling Challenges (The "Rigorous Science" Story)

**Challenge: Accounting for Spatial Autocorrelation (Why Standard Regression Failed)**

* **The Situation:** A standard Poisson regression assumes that cancer rates in one neighborhood are independent of its neighbors. In reality, environmental risks and demographics cluster spatially.
* **The Action:** I implemented a **BYM2 (Besag-York-Mollié)** Bayesian hierarchical model.
* This separates the error term into two components: an **Unstructured Random Effect** (pure noise) and a **Structured Spatial Effect** (where  is conditional on neighbors).
* I used an **ICAR (Intrinsic Conditional Autoregressive)** prior to allow regions to "borrow strength" from their neighbors, smoothing the estimates in low-population areas.



**Challenge: Graph Connectivity (The "Island" Problem)**

* **The Situation:** The spatial graph (adjacency matrix) contained "islands"—regions with no neighbors. This makes the ICAR prior mathematically impossible (division by zero neighbors).
* **The Action:** I used `libpysal` to detect disconnected components in the graph and filtered them out before passing the adjacency matrix to the Bayesian sampler.

---
 



**Challenge: MCMC Convergence Speed (Hours vs. Minutes)**

* **The Situation:** Running a full Hamiltonian Monte Carlo (HCMC) sampling on 13,000 regions with complex spatial priors was taking hours and exceeding available compute resources.
* **The Action:** I applied a two-tiered optimization strategy:
1. **Algorithmic:** I rewrote the Stan model to use `poisson_log_glm`, which uses AVX-optimized matrix algebra for the likelihood function (10x speedup).
2. **Strategic:** I implemented a filtering mechanism to subset the data by County (e.g., focusing on FIPS 061/Manhattan) to validate the model pipeline on ~300 regions before attempting a full-state run.





Every project has a beautiful feature showcase page.
It's easy to include images in a flexible 3-column grid format.
Make your photos 1/3, 2/3, or full width.

To give your project a background in the portfolio page, just add the img tag to the front matter like so:

    ---
    layout: page
    title: project
    description: a project with a background image
    img: /assets/img/12.jpg
    ---

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/1.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/3.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/5.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Caption photos easily. On the left, a road goes through a tunnel. Middle, leaves artistically fall in a hipster photoshoot. Right, in another hipster photoshoot, a lumberjack grasps a handful of pine needles.
</div>
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/5.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    This image can also have a caption. It's like magic.
</div>

You can also put regular text between your rows of images.
Say you wanted to write a little bit about your project before you posted the rest of the images.
You describe how you toiled, sweated, *bled* for your project, and then... you reveal its glory in the next row of images.


<div class="row justify-content-sm-center">
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.html path="assets/img/6.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.html path="assets/img/11.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    You can also have artistically styled 2/3 + 1/3 images, like these.
</div>


The code is simple.
Just wrap your images with `<div class="col-sm">` and place them inside `<div class="row">` (read more about the <a href="https://getbootstrap.com/docs/4.4/layout/grid/">Bootstrap Grid</a> system).
To make images responsive, add `img-fluid` class to each; for rounded corners and shadows use `rounded` and `z-depth-1` classes.
Here's the code for the last row of images above:

{% raw %}
```html
<div class="row justify-content-sm-center">
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.html path="assets/img/6.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.html path="assets/img/11.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
```
{% endraw %}
