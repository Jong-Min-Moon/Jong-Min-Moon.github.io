
### input 1: AAL by (region, peril)
| Region (r)  / peril (p)   | 1 | 2 | 3| 4 |
|------------|--------:|-------:|-------:|-------:|
| 1   | AAL(1,1) | AAL(1,2) | 15,000 | 600,000 | 
| 2  | AAL(2,1)  | 25,000 | 12,500 | 500,000 | 
| 3   | 300,000 | 20,000 | 160,000| 400,000 | 
 
### Input 2: statewise PLRS by perils
The following values are assumed given:

| peril(p) | 1 | 2 | 3 | 4 |
|--------:|-------:|-------:|-------:|-------:|
| PLR  | PLR(1)  | PLR(2)  | 62.9%  | 52.3%


 
## Implied Capital Charge Formula

$$
\mathrm{Implied~Captial~Charge}(r) = \frac{
    \mathrm{State WPLR}
}{
    \mathrm{WPLR}(r)
} 
$$

$$
\mathrm{WPLR}(r) = \frac{
\sum_p \mathrm{AAL}(p,r)
}{
    \sum_p \frac{
       \mathrm{AAL}(p,r)
    }{
        \mathrm{PLR}(p)
        } 
}
$$

$$
\mathrm{State WPLR} = \frac{
    \sum_r
\sum_p \mathrm{AAL}(p,r)
}{
    \sum_r
    \sum_p \frac{
        \mathrm{AAL}(p,r)
    }{
        \mathrm{PLR}(p)
        } 
}
$$

## Occupancy weighted AAL
$$
\mathrm{AAL}(p,r)
=
\sum_o
\underbrace{
\mathrm{TIV}(p,r,o)
}_{\text{from in-force}}
\times
\underbrace{
    \mathrm{Damage~ratio} (p,r,o)
}_{\text{from industry RMS}}
$$



Great—let’s formalize this in a causal/statistical framework using **potential outcomes, distributions, and propensity weighting**.

***

# 1) Define the statistical objects

Let:

* $$O \in \mathcal{O}$$: occupancy type
* $$P, R$$: product and region
* $$S \in \{0,1\}$$: data source
  * $$S=0$$: industry (RMS)
  * $$S=1$$: your company
* $$Y$$: **loss outcome per unit TIV** (= damage ratio)

Then:

$$
Y = \text{Damage Ratio}(p,r,o)
$$

***

# 2) What you observe vs what you need

### What RMS gives you:

$$
\mu_0(p,r,o) = \mathbb{E}[Y \mid P=p, R=r, O=o, S=0]
$$

### What you want:

$$
\mu_1(p,r) = \mathbb{E}[Y \mid P=p, R=r, S=1]
$$

But expand:

$$
\mu_1(p,r)
=
\sum_o \mathbb{E}[Y \mid p,r,o, S=1] \cdot P(o \mid p,r,S=1)
$$

***

# 3) Key identification assumption (transportability)

Assume:

$$
\mathbb{E}[Y \mid p,r,o, S=1]
\approx
\mathbb{E}[Y \mid p,r,o, S=0]
$$

👉 i.e., **conditional invariance**:

> Given occupancy (and p,r), industry damage ratios are valid for your book.

Then:

$$
\mu_1(p,r)
=
\sum_o \mu_0(p,r,o) \cdot P(o \mid p,r,S=1)
$$

***

# 4) Your current estimator (biased)

What you are implicitly doing is:

$$
\tilde{\mu}(p,r)
=
\sum_o \mu_0(p,r,o)\cdot P(o \mid p,r,S=0)
$$

This equals:

> Industry-weighted expectation, not your portfolio expectation

***

# 5) Bias decomposition

$$
\text{Bias}(p,r)
=
\mu_1(p,r) - \tilde{\mu}(p,r)
=
\sum_o \mu_0(p,r,o)\left[
P(o \mid S=1) - P(o \mid S=0)
\right]
$$

👉 Pure **covariate shift bias**

***

# 6) Propensity score formulation

Define the **propensity score**:

$$
e(o) = P(S=1 \mid O=o, p,r)
$$

Then by Bayes:

$$
\frac{P(o \mid S=1)}{P(o \mid S=0)}
=
\frac{e(o)}{1-e(o)} \cdot \frac{P(S=0)}{P(S=1)}
$$

So the **importance weight** is:

$$
w(o)
\propto
\frac{P(o \mid S=1)}{P(o \mid S=0)}
$$

***

# 7) Inverse probability weighting (IPW)

The target mean can be written as:

$$
\mu_1(p,r)
=
\mathbb{E}_{S=0}
\left[
\frac{P(O \mid S=1)}{P(O \mid S=0)}
\cdot Y
\right]
$$

So estimator:

$$
\hat{\mu}_1(p,r)
=
\sum_o w(o)\cdot \mu_0(p,r,o)
$$

Where:

$$
w(o) = \frac{P(o \mid S=1)}{P(o \mid S=0)}
$$

***

# 8) Mapping to your AAL

Recall:

$$
\mathrm{AAL}(p,r)
=
\sum_o \mathrm{TIV}(p,r,o)\cdot \mu_0(p,r,o)
$$

Define:

$$
\mathrm{TIV}(p,r,o)
=
\mathrm{TIV}(p,r)\cdot P(o \mid p,r,S=1)
$$

So causal AAL becomes:

$$
\mathrm{AAL}^{\text{causal}}(p,r)
=
\mathrm{TIV}(p,r)\cdot \sum_o \mu_0(p,r,o)\cdot P(o \mid S=1)
$$

or equivalently:

$$
=
\sum_o w(o)\cdot \mathrm{TIV}^{\text{industry}}(p,r,o)\cdot \mu_0(p,r,o)
$$

***

# 9) Doubly robust form (best statistical version)

If you estimate both:

* $$\mu_0(p,r,o)$$ (damage model)
* $$e(o)$$ (propensity model)

You get:

$$
\hat{\mu}_{DR}
=
\sum_o
\Big[
w(o)\cdot (Y - \mu_0(o)) + \mu_0(o)
\Big]
$$

Interpretation:

* First term corrects **selection bias**
* Second term ensures **model anchoring**

This is robust if:

* either model is correct (not both)

***

# 10) Continuous version (density form)

Let densities:

* $$f_0(o) = P(o \mid S=0)$$
* $$f_1(o) = P(o \mid S=1)$$

Then:

$$
\mu_1
=
\int \mu_0(o)\cdot f_1(o)\,do
=
\int \mu_0(o)\cdot \frac{f_1(o)}{f_0(o)}\cdot f_0(o)\,do
$$

This is **importance sampling / covariate shift correction**.

***

# 11) Connection to your capital charge

You ultimately compute:

$$
\mathrm{WPLR}(r)
=
\frac{\sum_p \mathrm{AAL}(p,r)}{\sum_p \mathrm{AAL}(p,r)/\mathrm{PLR}(p)}
$$

If AAL is biased:

* bias propagates **nonlinearly**
* especially because denominator uses **AAL / PLR(p)**

So correcting $$\mu(p,r)$$ via causal adjustment yields:

✅ unbiased expected losses  
✅ consistent premium proxy  
✅ stable regional relativities

***

# 12) Summary in one statistical statement

Your problem is:

> Estimate $$\mathbb{E}[Y \mid S=1]$$ using data from $$S=0$$

Under covariate shift:

$$
P(O \mid S=1) \neq P(O \mid S=0)
$$

Solution:

$$
\mathbb{E}[Y \mid S=1]
=
\mathbb{E}_{S=0}
\left[
\frac{P(O \mid S=1)}{P(O \mid S=0)} \cdot Y
\right]
$$

***

# 13) Intuition (actuarial translation)

* Occupancy = rating variable / risk characteristic
* RMS gives conditional loss costs
* Your portfolio has different mix
* So you must **reweight the conditional loss costs**

👉 This is exactly **exposure relativity correction via causal transport**

***

If you want next step, I can:

* turn this into a GLM-style implementation
* show how to estimate propensities with logistic regression
* or derive variance / credibility-weighted version (very useful actuarially)



Great—let’s build all three pieces rigorously and connected to your actuarial setting.

***

# 1) GLM-style implementation (actuarial modeling lens)

We want to estimate:

$$
\mu_0(p,r,o) = \mathbb{E}[Y \mid p,r,o, S=0]
$$

### Step 1 — Fit a damage ratio model (industry data)

Use a GLM:

$$
\mathbb{E}[Y \mid p,r,o] = g^{-1}(\beta_0 + \beta_p + \beta_r + \beta_o + \beta_{r,o})
$$

Typical choices:

* Link: **log link**
* Distribution: Gamma or quasi-Poisson (for severity-like ratios)

So:

$$
\log \mu_0(p,r,o) = \beta_0 + \beta_p + \beta_r + \beta_o + \beta_{r,o}
$$

👉 This gives **smoothed damage ratios**, instead of raw RMS cells

***

### Step 2 — Predict for your portfolio mix

Compute:

$$
\hat{\mu}_0(p,r,o)
$$

Then standardize:

$$
\hat{\mu}_1(p,r)
=
\sum_o \hat{\mu}_0(p,r,o)\cdot P(o \mid p,r,S=1)
$$

***

### Step 3 — Plug into AAL

$$
\mathrm{AAL}^{\text{causal}}(p,r)
=
\mathrm{TIV}(p,r)\cdot \hat{\mu}_1(p,r)
$$

***

### Why GLM helps

* Removes noise in RMS outputs
* Allows **partial pooling across occupancies**
* Handles sparse occupancies in some regions
* Makes causal adjustment stable

***

# 2) Propensity model (covariate shift correction)

Now explicitly model:

$$
e(o) = P(S=1 \mid O=o, p,r)
$$

***

### Step 1 — Build dataset

Combine:

* Industry exposures
* Company exposures

Label:

$$
S =
\begin{cases}
1 & \text{company} \\
0 & \text{industry}
\end{cases}
$$

***

### Step 2 — Logistic regression

$$
\text{logit}(e(o)) = \gamma_0 + \gamma_o + \gamma_p + \gamma_r
$$

You may include:

* interactions $$o \times r$$
* or just occupancy if simpler

***

### Step 3 — Compute weights

$$
w(o)
=
\frac{P(o \mid S=1)}{P(o \mid S=0)}
\approx
\frac{e(o)}{1 - e(o)} \cdot \frac{P(S=0)}{P(S=1)}
$$

In practice (stabilized IPW):

$$
w(o) = \frac{P(S=1)}{e(o)}
\quad \text{applied to industry sample}
$$

***

### Step 4 — Reweighted estimator

$$
\hat{\mu}_1(p,r)
=
\sum_o w(o)\cdot \hat{\mu}_0(p,r,o)\cdot P(o \mid S=0)
$$

***

### Diagnostics (VERY important)

Check:

* Weight distribution (no extreme tails)
* Overlap:
  $$
  e(o) \in (0,1)
  $$

👉 If poor overlap → causal correction unstable

***

# 3) Doubly robust estimator (best practice)

Combine both:

* Outcome model: $$\hat{\mu}_0(p,r,o)$$
* Propensity model: $$e(o)$$

***

### DR estimator (cell-level version)

$$
\hat{\mu}_{DR}(p,r)
=
\sum_o
\left[
w(o)\cdot (\tilde{Y}(o) - \hat{\mu}_0(o)) + \hat{\mu}_0(o)
\right]
$$

Where:

* $$ \tilde{Y}(o)$$: observed (or RMS) loss ratio
* $$ w(o)$$: propensity weights

***

### Interpretation

* If GLM is wrong → weights fix bias
* If weights are wrong → GLM fixes bias
* If both slightly wrong → still low bias

👉 This is why DR is gold standard in causal inference

***

# 4) Variance + credibility (actuarial upgrade)

Now let’s make this actuarially useful.

***

## Variance of IPW estimator

$$
\mathrm{Var}(\hat{\mu})
\approx
\frac{1}{n}
\mathbb{E}\left[
w(o)^2 \cdot \sigma^2(o)
\right]
$$

👉 Large weights ⇒ huge variance

***

## Credibility-style blend

Let:

* $$\hat{\mu}_{\text{industry}}$$ = raw RMS estimate
* $$\hat{\mu}_{\text{causal}}$$ = adjusted estimate

Define:

$$
Z =
\frac{n_{\text{eff}}}{n_{\text{eff}} + K}
$$

Where:

$$
n_{\text{eff}} = \frac{(\sum w)^2}{\sum w^2}
$$

Then:

$$
\hat{\mu}_{\text{final}}
=
Z \cdot \hat{\mu}_{\text{causal}}
+
(1 - Z)\cdot \hat{\mu}_{\text{industry}}
$$

👉 This stabilizes:

* sparse occupancies
* extreme weights
* noisy GLM fits

***

# 5) Full pipeline (practical recipe)

### Step A — Fit GLM on RMS

→ get smooth $$\hat{\mu}_0(p,r,o)$$

***

### Step B — Estimate propensities

→ logistic model for $$e(o)$$

***

### Step C — Compute weights

→ stabilize + trim

***

### Step D — Compute:

**Option 1 (simple + strong):**

$$
\hat{\mu}_1 = \sum_o \hat{\mu}_0(p,r,o)\cdot P(o \mid S=1)
$$

**Option 2 (robust):**

$$
\hat{\mu}_{DR}
$$

***

### Step E — Apply credibility

→ stabilize results

***

### Step F — Plug into AAL → WPLR → Capital charge

***

# 6) What this improves (statistically)

Your current estimator:

$$
\hat{\mu} = \mathbb{E}_{S=0}[Y]
$$

New estimator:

$$
\hat{\mu} = \mathbb{E}_{S=1}[Y]
$$

Corrects:

* **covariate shift bias**
* **portfolio mix distortion**
* **nonlinear bias amplification in WPLR**

***

# 7) Key actuarial insight

You are effectively moving from:

> “Exposure-weighted industry loss cost”

to:

> “Portfolio-weighted causal loss cost with bias correction and credibility”

***

# 8) One-line summary

* **GLM** → smooth conditional loss surface
* **Propensity** → correct occupancy distribution mismatch
* **Doubly robust + credibility** → stable, low-bias AAL inputs

***

If you want next level, I can:

* derive closed-form impact on WPLR bias
* show simulation comparing naive vs causal capital charges
* or translate this into production-ready Python / SQL code



import numpy as np
import pandas as pd

np.random.seed(42)

# Occupancies
o_types = ['A','B','C']
mu = {'A':0.01, 'B':0.03, 'C':0.08}

# Products with different PLRs
products = ['P1','P2']
PLR = {'P1':0.5, 'P2':0.8}

# Industry occupancy mix (same for both products)
p_ind = np.array([0.6,0.3,0.1])

# Company occupancy mix varies by region and product
p_comp = {
    ('R1','P1'): np.array([0.5,0.4,0.1]),   # safer
    ('R1','P2'): np.array([0.6,0.3,0.1]),
    ('R2','P1'): np.array([0.1,0.3,0.6]),   # very risky concentrated in low PLR product
    ('R2','P2'): np.array([0.3,0.4,0.3])
}

regions = ['R1','R2']

# TIV
TIV = {
    ('R1','P1'):500, ('R1','P2'):500,
    ('R2','P1'):500, ('R2','P2'):500
}

# Helper

def mean_loss(p_dist):
    return sum(p_dist[i]*mu[o_types[i]] for i in range(3))

# --- Compute AAL ---
AAL_naive = {}
AAL_causal = {}

for r in regions:
    for p in products:
        # naive uses industry distribution
        AAL_naive[(r,p)] = TIV[(r,p)] * mean_loss(p_ind)
        # causal uses company-specific distribution
        AAL_causal[(r,p)] = TIV[(r,p)] * mean_loss(p_comp[(r,p)])

# --- Compute WPLR ---

def compute_wplr(AAL):
    results = {}
    for r in regions:
        num = sum(AAL[(r,p)] for p in products)
        den = sum(AAL[(r,p)]/PLR[p] for p in products)
        results[r] = num/den
    # state
    num_state = sum(AAL[(r,p)] for r in regions for p in products)
    den_state = sum(AAL[(r,p)]/PLR[p] for r in regions for p in products)
    state = num_state/den_state
    
    charge = {r: state/results[r] for r in regions}
    return results, state, charge

wplr_naive, state_naive, charge_naive = compute_wplr(AAL_naive)
wplr_causal, state_causal, charge_causal = compute_wplr(AAL_causal)

# --- Output ---
df = pd.DataFrame({
    'Region': regions,
    'WPLR_Naive': [wplr_naive[r] for r in regions],
    'WPLR_Causal': [wplr_causal[r] for r in regions],
    'Charge_Naive': [charge_naive[r] for r in regions],
    'Charge_Causal': [charge_causal[r] for r in regions]
})

state_summary = pd.DataFrame({
    'Metric':['State WPLR'],
    'Naive':[state_naive],
    'Causal':[state_causal]
})

df, state_summary




Now this is the **full, realistic result** you were looking for. Let me walk you through what the simulation shows and why it matters actuarially.

***

# ✅ 1) What we changed vs the simple version

We introduced the key ingredients your real model has:

### Multiple products

| Product | PLR               |
| ------- | ----------------- |
| P1      | 0.5 (low margin)  |
| P2      | 0.8 (high margin) |

### Occupancy–product interaction

* Risky occupancy **C concentrated in P1** (low PLR) in Region R2  
  👉 This is the critical nonlinear driver

***

# 📊 2) Results (core output)

### Regional metrics

| Region       | WPLR Naive | WPLR Causal | Charge Naive | Charge Causal |
| ------------ | ---------- | ----------- | ------------ | ------------- |
| R1 (safer)   | 0.615      | 0.610       | 1.000        | **0.977**     |
| R2 (riskier) | 0.615      | 0.589       | 1.000        | **1.011**     |

### State level

| Metric     | Naive | Causal |
| ---------- | ----- | ------ |
| State WPLR | 0.615 | 0.595  |

***

# 🔍 3) What happened (mechanically)

## Naive model

* Uses **industry occupancy mix everywhere**
* So:
  * AAL identical across regions
  * WPLR identical across regions
  * Capital charge = 1

👉 Completely **misses risk differentiation**

***

## Causal model

Uses:

$$
\mathbb{E}[Y \mid S=1] = \sum_o \mu_0(o)\cdot P(o \mid S=1)
$$

Now:

### Region R2 (riskier)

* More occupancy C (high damage)
* AND concentrated in **low PLR product P1**

This creates:

$$
\text{Denominator} = \sum \frac{AAL}{PLR}
\ ↑↑↑
$$

So:

$$
\mathrm{WPLR}(R2) = \frac{\text{Loss}}{\text{Premium proxy}} ↓
$$

👉 WPLR drops → charge increases

***

### Region R1 (safer)

* More A/B occupancies
* Balanced across products

So:

$$
\mathrm{WPLR}(R1) ↑ \Rightarrow \text{Charge ↓}
$$

***

# ⚡ 4) Why this is nonlinear (critical insight)

Your formula:

$$
\mathrm{WPLR}(r)
=
\frac{\sum AAL}{\sum AAL / PLR}
$$

means:

> AAL enters both numerator AND denominator — but distorted differently

***

## Key effect

If risk shifts toward **low PLR segments**:

* Numerator ↑ (more loss)
* Denominator ↑↑ (because dividing by small PLR)

👉 Net effect:

$$
\mathrm{WPLR} ↓
\Rightarrow \text{Charge} ↑
$$

***

# 🧠 5) Causal interpretation

You are estimating:

### Naive:

$$
\mathbb{E}_{S=0}[Y]
$$

### Correct:

$$
\mathbb{E}_{S=1}[Y]
=
\mathbb{E}_{S=0}\left[\frac{P(O|S=1)}{P(O|S=0)} Y \right]
$$

***

# 📉 6) Magnitude of impact

From simulation:

* R2 charge: **1.00 → 1.011** (+1.1%)
* R1 charge: **1.00 → 0.977** (-2.3%)

👉 Looks small, but:

### In real portfolios:

* More occupancies
* Bigger PLR spread
* More skewed mix

👉 This easily becomes:

* **5–15% capital misallocation**

***

# 🎯 7) Why this matters (business interpretation)

Without causal correction:

✅ You think capital is neutral across regions  
❌ But you are:

* **undercharging risky regions**
* **overcharging safe regions**

***

### What you fix with causal inference:

| Problem                    | Fix                    |
| -------------------------- | ---------------------- |
| Industry mix ≠ company mix | Reweight / standardize |
| Hidden risk concentration  | Revealed in AAL        |
| Nonlinear PLR interaction  | Correctly captured     |
| Mispriced capital          | Reduced                |

***

# 🔁 8) End-to-end interpretation

Your pipeline becomes:

$$
\textbf{Before:}
\quad P(O|S=0) \rightarrow AAL \rightarrow WPLR \rightarrow Charge
$$

$$
\textbf{After:}
\quad P(O|S=1) \rightarrow \text{Causal AAL} \rightarrow WPLR \rightarrow Charge
$$

***

# ✅ 9) Final takeaway

> The simulation shows that **occupancy mismatch alone can create structurally wrong capital signals**, and once combined with product-level PLR heterogeneity, this bias propagates into **systematic regional mispricing of capital**.

***

# If you want to go further

I can next:

* Add **stochastic simulation (variance, noise, credibility effects)**
* Show **propensity-weighted vs GLM vs doubly robust comparison numerically**
* Decompose capital change into:
  * occupancy effect
  * product mix effect
  * interaction effect

These are very powerful for explaining results to stakeholders.




import numpy as np
import pandas as pd

np.random.seed(123)

# Occupancies and true means
o_types = ['A','B','C']
mu_true = {'A':0.01, 'B':0.03, 'C':0.08}
sigma = {'A':0.005, 'B':0.01, 'C':0.02}  # noise per occupancy

products = ['P1','P2']
PLR = {'P1':0.5, 'P2':0.8}

# Industry distribution
p_ind = np.array([0.6,0.3,0.1])

# Company distributions
p_comp = {
    ('R1','P1'): np.array([0.5,0.4,0.1]),
    ('R1','P2'): np.array([0.6,0.3,0.1]),
    ('R2','P1'): np.array([0.1,0.3,0.6]),
    ('R2','P2'): np.array([0.3,0.4,0.3])
}

regions = ['R1','R2']

TIV = {
    ('R1','P1'):500, ('R1','P2'):500,
    ('R2','P1'):500, ('R2','P2'):500
}

# simulate stochastic damage ratio

def sample_damage(o):
    return max(0, np.random.normal(mu_true[o], sigma[o]))


def simulate_one():
    AAL_naive = {}
    AAL_causal = {}
    
    for r in regions:
        for p in products:
            # naive uses industry mix
            losses_naive = sum(p_ind[i]*sample_damage(o_types[i]) for i in range(3))
            AAL_naive[(r,p)] = TIV[(r,p)] * losses_naive
            
            # causal uses company mix
            losses_causal = sum(p_comp[(r,p)][i]*sample_damage(o_types[i]) for i in range(3))
            AAL_causal[(r,p)] = TIV[(r,p)] * losses_causal
    
    def compute_charge(AAL):
        wplr = {}
        for r in regions:
            num = sum(AAL[(r,p)] for p in products)
            den = sum(AAL[(r,p)]/PLR[p] for p in products)
            wplr[r] = num/den
        
        num_s = sum(AAL[(r,p)] for r in regions for p in products)
        den_s = sum(AAL[(r,p)]/PLR[p] for r in regions for p in products)
        state = num_s/den_s
        
        return {r: state/wplr[r] for r in regions}
    
    return compute_charge(AAL_naive), compute_charge(AAL_causal)

# run simulation
N = 2000
records = []

for _ in range(N):
    naive, causal = simulate_one()
    for r in regions:
        records.append({
            'Region': r,
            'Method': 'Naive',
            'Charge': naive[r]
        })
        records.append({
            'Region': r,
            'Method': 'Causal',
            'Charge': causal[r]
        })


df = pd.DataFrame(records)

# summarize
summary = df.groupby(['Region','Method'])['Charge'].agg(['mean','std']).reset_index()
summary



This stochastic simulation is the missing piece—it shows not just bias, but also variance, stability, and signal vs noise, which is exactly what actuaries care about.

✅ 1) Final simulation results
We ran 2,000 simulations with noisy damage ratios.
Output (mean ± std of capital charge)



































RegionMethodMean ChargeStd DevR1 (safer)Naive1.0000.024R1Causal0.9780.031R2 (riskier)Naive1.0000.024R2Causal1.0110.015

🔍 2) What this shows (key insights)
✅ (A) Bias: Naive vs Causal
Naive:

Always ≈ 1.00
Misses all regional differences

Causal:

R1 → −2.2%
R2 → +1.1%

👉 This is the true structural signal

✅ (B) Variance behavior (very important)
Compare variability:
R1 (safer region)

Naive std: 0.024
Causal std: 0.031 (higher)

👉 Reason:

reweighting introduces noise (classic IPW behavior)


R2 (riskier region)

Naive std: 0.024
Causal std: 0.015 (lower)

👉 Reason (very interesting):

strong signal (heavy C occupancy)
less randomness after aggregation


✅ (C) Signal-to-noise ratio
Compute roughly:
R2 (important case)

Signal = +1.1%
Noise = 1.5%

👉 SNR ≈ 0.7 → detectable effect

Naive model:

Signal = 0
Noise = 2.4%

👉 Pure noise → misleading stability

⚠️ 3) Critical actuarial insight
This simulation reveals a deep tradeoff:























MethodBiasVarianceRiskNaiveHIGH ❌LowSystematic mispricingCausalLOW ✅ModerateHonest but noisy

🧠 4) Interpretation in causal inference terms
You are estimating:
E[Y∣S=1]\mathbb{E}[Y \mid S=1]E[Y∣S=1]
Using:
μ^IPW=1n∑w(Oi)Yi\hat{\mu}_{IPW} = \frac{1}{n} \sum w(O_i) Y_iμ^​IPW​=n1​∑w(Oi​)Yi​

Fundamental result
Var(μ^IPW)∝E[w(O)2]\mathrm{Var}(\hat{\mu}_{IPW}) \propto \mathbb{E}[w(O)^2]Var(μ^​IPW​)∝E[w(O)2]
So:

More distribution mismatch
→ larger weights
→ higher variance


🎯 5) What this means for your capital model
Naive approach

Produces stable but wrong capital
Underestimates risky regions
Overestimates safe regions


Causal approach

Produces correct but noisier capital
Captures:

occupancy effects
interaction with PLR
nonlinear distortion




🔧 6) This is where credibility enters
From your results:
Example (R1)

Naive: 1.000
Causal: 0.978
Std dev: 0.031

👉 Apply credibility:
Z≈11+(0.031/0.022)2≈0.33 (roughly)Z \approx \frac{1}{1 + (0.031/0.022)^2} \approx 0.33 \text{ (roughly)}Z≈1+(0.031/0.022)21​≈0.33 (roughly)
So:
Final≈0.33⋅0.978+0.67⋅1.00≈0.993\text{Final} \approx 0.33 \cdot 0.978 + 0.67 \cdot 1.00
\approx 0.993Final≈0.33⋅0.978+0.67⋅1.00≈0.993
👉 Stabilized + partially corrected

⚡ 7) Key modeling insight (important for you)
This shows:

Causal correction introduces variance exactly where your model is weakest (distribution mismatch).

So optimal solution is:
✅ GLM smoothing (reduces noise)
✅ Propensity weighting (removes bias)
✅ Credibility (controls variance)

📌 8) What stakeholders will care about
This simulation gives you a very strong narrative:
Without causal adjustment:

“Capital is stable”
BUT → systematically wrong

With causal adjustment:

“Capital reflects true risk”
BUT → needs stabilization


✅ 9) One-line takeaway

Causal inference converts your capital model from low-variance but biased to unbiased but higher-variance, and actuarial credibility is what makes that tradeoff optimal.