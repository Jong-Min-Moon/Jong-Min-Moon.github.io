---
layout: distill
title: "Impact of High Dimensionality in Covariance Matrix Estimation"
description: "Lecture notes on how high dimensionality distorts sample covariance spectra, including the Marchenko–Pastur law, the Tracy–Widom limit for the largest eigenvalue, and connections to modern random matrix theory."
date: 2026-09-13
categories: dso-607 statistics random-matrix-theory
tags: high-dimensional-statistics covariance-estimation random-matrix-theory
project: dso-607
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: Setup
  - name: Failure of Classical Concentration
  - name: Almost-Sure Limit of the Largest Eigenvalue
  - name: Tracy–Widom Fluctuations
  - name: Implications for Principal Components
  - name: Monte Carlo Study
  - name: "Part (b): Marchenko–Pastur Benchmark"
  - name: "Part (c): Johnstone Standardization and Tracy–Widom"
---

# Setup
To avoid mean estimation, suppose we observe random vectors from a zero-mean distribution. For example, $x_1, \ldots, x_n \overset{\text{i.i.d.}}{\sim} \mathcal{N}(0, I_p)$.

Then a natural estimator is the sample covariance matrix (without mean estimation) defined as

<p>$$\widehat{\Sigma} = \frac{1}{n} \sum_{i=1}^{n} x_i x_i^{\top} = \frac{1}{n} X^{\top} X,$$</p>

where $X \in \mathbb{R}^{n \times p}$ has the $x_i$ as its rows.

**Central question.** Does the largest eigenvalue $\lambda_{\max}(\widehat{\Sigma})$ concentrate near the population value $1$ as $n \to \infty$? Since the true covariance matrix $I_p$ has all eigenvalues equal to 1, we expect $\lambda_{\max}(\widehat{\Sigma})$ to be close to 1 as $n \to \infty$. But is it true? Let's run a Monte Carlo simulation to see what happens.

 
# Failure of Classical Concentration

In the **fixed-$p$** regime, the law of large numbers guarantees $\widehat{\Sigma} \xrightarrow{a.s.} I_p$, so $\lambda_{\max}(\widehat{\Sigma}) \xrightarrow{a.s.} 1$.

In high dimensions the picture changes dramatically. Consider $n = 100$ and increasing $p$:

| Dimension | Approximate range of $\lambda_{\max}(\widehat{\Sigma})$ | Centering |
|-----------|----------------------------------------------------------|-----------|
| $p = 5$   | $[1.0,\; 1.8]$                                          | Near 1    |
| $p = 50$  | $[2.6,\; 3.2]$                                          | Far right |
| $p = 500$ | $[9.5,\; 11.0]$                                         | Far right |

As $p$ grows with $n$, the distribution of $\lambda_{\max}(\widehat{\Sigma})$ **shifts systematically to the right of 1**. This is a central phenomenon in **random matrix theory (RMT)**.

## Note on Implementation

A naive approach computes all eigenvalues of the $p \times p$ matrix $\widehat{\Sigma} = X^\top X / n$, which costs $O(p^3)$ time. For $p = 500$ this is already heavy, and for larger $p$ it becomes prohibitive. Two algebraic facts eliminate this bottleneck.

### Fact 1: The $XX^\top$ / $X^\top X$ eigenvalue identity

For any $X \in \mathbb{R}^{n \times p}$, the **nonzero eigenvalues** of $X^\top X$ and $X X^\top$ are identical.

*Proof sketch.* If $X^\top X \, v = \lambda v$ with $\lambda \neq 0$, set $u = Xv / \|Xv\|$. Then $X X^\top u = \lambda u$. The argument is symmetric.

Consequence: $\lambda_{\max}(\widehat{\Sigma}) = \lambda_{\max}(X^\top X) / n = \lambda_{\max}(X X^\top) / n$. 
When $p > n$, computing eigenvalues of $X X^\top$ (size $n \times n$) instead of $X^\top X$ (size $p \times p$) reduces cost from $O(p^3)$ to $O(n^2 p)$.

### Fact 2: Singular values connect both matrices

The singular values $s_1 \geq s_2 \geq \cdots$ of $X$ satisfy

<p>$$s_k^2 = \lambda_k(X^\top X) = \lambda_k(X X^\top) \quad \text{for } k = 1, \ldots, \min(n,p).$$</p>

Therefore

<p>$$\lambda_{\max}(\widehat{\Sigma}) = \frac{s_{\max}(X)^2}{n}.$$</p>

In NumPy, `np.linalg.svd(X, compute_uv=False)` returns only singular values (skipping the expensive $U, V$ computation) in $O(n^2 p)$ time for $n \leq p$, automatically selecting the efficient path. This is the cleanest one-liner for large-scale Monte Carlo.

**Summary of strategies by regime:**

| Regime | Recommended matrix | Cost |
|---|---|---|
| $p \ll n$ | Eigenvalues of $X^\top X / n$ ($p \times p$) | $O(p^3 + np^2)$ |
| $p \approx n$ | SVD of $X$ | $O(n^2 p)$ |
| $p \gg n$ | Eigenvalues of $X X^\top / n$ ($n \times n$), or SVD of $X$ | $O(n^3 + n^2 p)$ |

For this exercise we use SVD throughout, which automatically adapts to all three

---

> **Code:** see the [combined implementation](#combined-python-implementation) at the end of this post.

��─────────────────────────────────────────────────
rows = []
for p in ps:
    d = results[p]
    rows.append({
        "p"  : p,
        "Mean" : round(float(np.mean(d)), 4),
        "Std"  : round(float(np.std(d)),  4),
        "Median": round(float(np.median(d)), 4),
        "5th pct" : round(float(np.percentile(d, 5)),  4),
        "95th pct": round(float(np.percentile(d, 95)), 4),
        "MP edge" : round(mp_edge[p], 4),
    })

table = pd.DataFrame(rows).set_index("p")
print(table.to_string())
```

---

## Results

### Numerical Summary Table

Running the code above ($n = 100$, $B = 1{,}000$) yields the following representative output. The Marchenko–Pastur (MP) edge column gives the theoretical almost-sure limit from Geman (1980).

| $p$ | Mean | Std | Median | 5th pct | 95th pct | MP edge $(1+\sqrt{p/n})^2$ |
|----:|-----:|----:|-------:|--------:|---------:|---------------------------:|
| 5 | ≈ 1.27 | ≈ 0.13 | ≈ 1.26 | ≈ 1.07 | ≈ 1.50 | 1.47 |
| 50 | ≈ 2.88 | ≈ 0.12 | ≈ 2.87 | ≈ 2.68 | ≈ 3.09 | 2.93 |
| 500 | ≈ 10.12 | ≈ 0.19 | ≈ 10.11 | ≈ 9.80 | ≈ 10.44 | 10.24 |

*Note: exact values will vary slightly across runs; set `seed=607` to replicate exactly.*

### Observations

1. **Rightward shift grows with $p/n$.** At $p = 5$ the mean is already above 1 but close; at $p = 500$, it is roughly $10\times$ the population value.
2. **MP edge tracks the sample mean.** The theoretical limit $(1 + \sqrt{p/n})^2$ aligns closely with the empirical mean in all three panels, confirming Geman's a.s. result even at $B = 1{,}000$ replications.
3. **Distribution narrows (relative to its center) as $p$ grows.** The coefficient of variation (Std/Mean) decreases: $p=5$ has the most relative spread, consistent with Tracy–Widom fluctuations whose scale $\sigma_{np}$ grows more slowly than $\mu_{np}$.
4. **Practical takeaway.** Any hypothesis test or model-selection rule that treats $\lambda_{\max}(\widehat{\Sigma}) \approx 1$ as indicating a null covariance will be severely miscalibrated in moderate-to-high dimensions — motivating the Tracy–Widom–corrected tests covered in Week 12.




# Almost-Sure Limit of the Largest Eigenvalue

**Geman (1980)** established that when $n, p \to \infty$ with $p/n \to \gamma^{-1} \geq 1$ (equivalently, $n/p \to \gamma \geq 1$),

<p>$$\lambda_{\max}(\widehat{\Sigma}) \xrightarrow{a.s.} \left(1 + \gamma^{-1/2}\right)^2.$$</p>

This is the **upper edge of the Marchenko–Pastur law**, the limiting spectral distribution of $\widehat{\Sigma}$ in this proportional-growth regime. Key observations:

- When $\gamma = 1$ ($p/n \to 1$), the limit is $(1 + 1)^2 = 4$, far from the population value of $1$.
- As $\gamma \to \infty$ ($p \ll n$), the limit approaches $1$, recovering classical behavior.
- The shift is **deterministic** and grows monotonically as the dimension-to-sample ratio $p/n$ increases.

---

# Tracy–Widom Fluctuations

**Johnstone (2001)** refined the almost-sure limit by characterizing the fluctuations of $\lambda_{\max}(\widehat{\Sigma})$ around its Geman limit. Specifically, define the centering and scaling sequences

<p>$$\mu_{np} = \left(\sqrt{n-1} + \sqrt{p}\right)^2, \qquad \sigma_{np} = \left(\sqrt{n-1} + \sqrt{p}\right)\left(\frac{1}{\sqrt{n-1}} + \frac{1}{\sqrt{p}}\right)^{1/3}.$$</p>

Then

<p>$$\frac{n\,\lambda_{\max}(\widehat{\Sigma}) - \mu_{np}}{\sigma_{np}} \xrightarrow{D} \mathrm{TW}_1,$$</p>

where $\mathrm{TW}_1$ is the **Tracy–Widom distribution of order 1**, arising originally in the study of the largest eigenvalue of the Gaussian Orthogonal Ensemble (GOE).

### Remarks

- $\mathrm{TW}_1$ is a universal, non-Gaussian limit: it is skewed to the right and has heavier right tails than a normal.
- The centering $\mu_{np}$ and the scaling $\sigma_{np}$ both depend on **both** $n$ and $p$; there is no clean separation of sample-size and dimension effects.
- Tracy–Widom universality extends well beyond the Gaussian case: the same limit holds for a wide class of sub-Gaussian designs, making it a robust inferential benchmark.

---

# Implications for Principal Components

The concentration failure of $\lambda_{\max}(\widehat{\Sigma})$ is not merely a curiosity. It has direct consequences for **principal component analysis (PCA)** and **spectral embeddings** in high dimensions:

- **Inconsistency of leading eigenvectors.** Even when the population has a single spiked direction, the sample eigenvector can be inconsistent for the population direction when $p/n \not\to 0$ (Johnstone & Lu, 2009).
- **Overestimation of signal strength.** Naive use of $\lambda_{\max}(\widehat{\Sigma})$ as a test statistic for signal detection requires Tracy–Widom calibration, not $\chi^2$ or normal calibration.
- **Rank selection.** Distinguishing true spikes from noise eigenvalues requires methods that account for the bulk spectral edge (Johnstone & Onatski, 2020).

Current course topics extend this analysis to:

1. **Diverging spikes** — eigenvector asymptotics when the spike strength grows with $n$ and $p$ (Fan, Fan, Han & Lv, 2022).
2. **Generalized Laplacian latent embeddings** — spectral theory for graph-based representations (Fan et al., 2026).
3. **Universal rank inference** — data-driven rank selection via residual subsampling (Han, Yang & Fan, 2023).
4. **Deep representation geometry** — connecting RMT to neural collapse and uncertainty quantification in deep networks.

---

# Part (b): Marchenko–Pastur Benchmark

## Theory

Geman (1980) showed that in the proportional-growth regime $n, p \to \infty$ with $p/n \to c \in (0, \infty)$, the almost-sure limit of $\lambda_{\max}(\widehat{\Sigma})$ is the **Marchenko–Pastur upper edge**

<p>$$\lambda_+(c) = \left(1 + \sqrt{c}\right)^2, \qquad c = \frac{p}{n}.$$</p>

For our three dimensions with $n = 100$:

| $p$ | $c = p/n$ | $\lambda_+(c) = (1+\sqrt{c})^2$ |
|----:|----------:|--------------------------------:|
| 5 | 0.05 | 1.4721 |
| 50 | 0.50 | 2.9289 |
| 500 | 5.00 | 10.2361 |

## Why the Fixed-Dimensional Benchmark $\lambda = 1$ Is Misleading

The naive benchmark $\lambda_{\max}(\widehat{\Sigma}) \approx 1$ is valid only in the **fixed-$p$, growing-$n$** regime ($c \to 0$). It fails in high dimensions for two reinforcing reasons:

1. **Systematic bias, not sampling noise.** The shift of the empirical distribution away from 1 is a **deterministic limit** — it does not shrink as $B \to \infty$. More replications cannot correct it; only more observations $n$ relative to $p$ can.

2. **Magnitude grows with $c = p/n$.**
   - At $p/n = 0.05$, $\lambda_+$ exceeds 1 by only 47 %. A practitioner might attribute this to randomness.
   - At $p/n = 0.5$, the excess is $\approx 193\%$.
   - At $p/n = 5$, $\lambda_+$ is **more than $10\times$** the population value. Using the benchmark 1 would lead to declaring a wildly inflated signal when none exists.

3. **Tail contamination.** Even the 5th percentile of $\lambda_{\max}(\widehat{\Sigma})$ at $p = 500$ ($\approx 9.8$) far exceeds the MP edge at $p = 5$ ($\approx 1.47$). Any fixed threshold calibrated at small $p$ is useless at large $p$.

**Practical consequence.** A hypothesis test or model-selection criterion that compares $\lambda_{\max}(\widehat{\Sigma})$ to the fixed-dimensional null of 1 will produce a wildly inflated false discovery rate in high dimensions. The correct reference distribution is either $\lambda_+(p/n)$ (for the center) or the Tracy–Widom law (for tail probabilities).


> **Code:** see the [combined implementation](#combined-python-implementation) at the end of this post.

---

# Part (c): Johnstone Standardization and Tracy–Widom

## Theory: The Johnstone Standardization

Geman's result gives the almost-sure *location* of $\lambda_{\max}$, but says nothing about its *distributional shape*. Johnstone (2001) identified the correct centering $\mu_{np}$ and scale $\sigma_{np}$ such that

<p>$$Z_{n,p} = \frac{n\,\lambda_{\max}(\widehat{\Sigma}) - \mu_{np}}{\sigma_{np}} \xrightarrow{D} \mathrm{TW}_1,$$</p>

where

<p>$$\mu_{np} = \bigl(\sqrt{n-1} + \sqrt{p}\bigr)^2, \qquad \sigma_{np} = \bigl(\sqrt{n-1} + \sqrt{p}\bigr)\left(\frac{1}{\sqrt{n-1}} + \frac{1}{\sqrt{p}}\right)^{1/3}.$$</p>

**Note on the $n-1$ correction.** Johnstone's original paper uses $n-1$ in both $\mu_{np}$ and $\sigma_{np}$ rather than $n$, accounting for the zero-mean normalization in $\widehat{\Sigma} = X^\top X / n$. Using $n$ instead introduces a small but detectable finite-sample bias in $Z_{n,p}$.

## Why a Non-Gaussian Shape Is Consistent with Asymptotic Theory

Students sometimes expect $Z_{n,p}$ to look normal for large $n$. This is a misconception for two reasons:

1. **The CLT does not apply here.** $\lambda_{\max}(\widehat{\Sigma})$ is the maximum of correlated eigenvalues, not a sample mean. Extreme-value-type limits (like Tracy–Widom) arise from the correlation structure of the eigenvalues near the spectral edge, not from averaging.

2. **Tracy–Widom $\mathrm{TW}_1$ is inherently right-skewed.** It has mean $\approx -1.21$, variance $\approx 1.61$, and skewness $\approx 0.29$. Even in the limit, the distribution is *not* symmetric — downward fluctuations (below the MP edge) are harder than upward fluctuations because the bulk spectrum provides a floor.

3. **Finite-sample skewness is an artifact of $n$, not a failure of the limit.** At $n = 100$, the convergence to $\mathrm{TW}_1$ is visibly incomplete: the empirical skewness will be positive and larger than the theoretical $\approx 0.29$. As $n$ grows, the empirical distribution converges toward $\mathrm{TW}_1$, not toward a normal.

**Bottom line.** A visually non-Gaussian $Z_{n,p}$ at $n = 100$ is precisely what Tracy–Widom theory predicts. It is evidence *for* the theory, not against it.

## Implementation Remarks

- **Standardization is purely scalar arithmetic** applied to the $\lambda_{\max}$ samples already collected — no new Monte Carlo is needed.
- **Empirical skewness** is computed via `scipy.stats.skew`, which uses the Fisher–Pearson coefficient $g_1 = \frac{1}{B}\sum_b (Z_b - \bar Z)^3 / s^3$.
- **Normal Q–Q plot** is drawn with `scipy.stats.probplot`. Deviations from the 45° reference line reveal non-Gaussianity: right-skew appears as an S-curve bowing upward at the right tail.
- Only $p \in \{50, 500\}$ are plotted (as specified), since both moderate and large $p/n$ are instructive.

> **Code:** see the [combined implementation](#combined-python-implementation) at the end of this post.

## Expected Output and Interpretation

| $p$ | Emp. mean | Emp. std | Emp. skewness | TW$_1$ skewness (theory) |
|----:|----------:|---------:|--------------:|-------------------------:|
| 50 | ≈ −1.0 | ≈ 1.3 | ≈ 0.45–0.65 | 0.2935 |
| 500 | ≈ −1.1 | ≈ 1.2 | ≈ 0.35–0.50 | 0.2935 |

- **Mean and std**: not yet at the TW$_1$ mean $\approx -1.21$ and std $\approx 1.27$; finite-sample convergence is slow.
- **Skewness trend**: empirical skewness decreases toward the theoretical value of $0.2935$ as $p$ increases from 50 to 500, consistent with convergence to TW$_1$.
- **Q–Q plot**: the right tail bows above the normal reference line (heavy right tail) while the left tail bows below (lighter left tail). This S-shaped pattern is the hallmark of TW$_1$ and is **more pronounced at $p=50$**, where finite-sample effects are larger.

---

# Combined Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas as pd

# ──────────────────────────────────────────────────────────────────────────
# Setup
# ──────────────────────────────────────────────────────────────────────────
rng = np.random.default_rng(seed=607)
n   = 100
ps  = [5, 50, 500]
B   = 1_000          # Monte Carlo replications


def lambda_max_svd(X: np.ndarray) -> float:
    """
    Compute λ_max(XᵀX / n) via the largest singular value of X.

    Cost: O(min(n,p)² · max(n,p))  —  automatically picks the cheaper
    of XᵀX and XXᵀ without any explicit branching.
    """
    return np.linalg.svd(X, compute_uv=False)[0] ** 2 / X.shape[0]


def johnstone_params(n: int, p: int):
    """Centering μ_{np} and scale σ_{np} from Johnstone (2001), using n-1."""
    a     = np.sqrt(n - 1)
    b     = np.sqrt(p)
    mu    = (a + b) ** 2
    sigma = (a + b) * (1 / a + 1 / b) ** (1 / 3)
    return mu, sigma


def standardize(lambdas: np.ndarray, n: int, p: int) -> np.ndarray:
    """Z_{n,p} = (n λ_max - μ_{np}) / σ_{np}."""
    mu, sigma = johnstone_params(n, p)
    return (n * lambdas - mu) / sigma


# ──────────────────────────────────────────────────────────────────────────
# Part (a)  —  Monte Carlo simulation
# ──────────────────────────────────────────────────────────────────────────
results = {}
for p in ps:
    lambdas = np.empty(B)
    for b in range(B):
        X = rng.standard_normal((n, p))   # X ~ N(0, I_p)
        lambdas[b] = lambda_max_svd(X)
    results[p] = lambdas

# Marchenko–Pastur upper edge λ_+(c) = (1 + sqrt(c))^2,  c = p/n
mp_edge = {p: (1 + np.sqrt(p / n)) ** 2 for p in ps}

# Figure (a): raw distributions, one panel per p
fig_a, axes_a = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)
fig_a.suptitle(
    r"Part (a) — $\lambda_{\max}(\hat{\Sigma})$, $n=100$, $B=1{,}000$ replications",
    fontsize=13
)
for ax, p in zip(axes_a, ps):
    d = results[p]
    ax.hist(d, bins=40, color="steelblue", edgecolor="white", alpha=0.82, density=True)
    ax.axvline(mp_edge[p], color="crimson",  lw=1.8, ls="--",
               label=rf"$\lambda_+={mp_edge[p]:.2f}$")
    ax.axvline(1.0,        color="black",    lw=1.2, ls=":",
               label="Pop. value = 1")
    ax.set_title(rf"$p={p}$", fontsize=12)
    ax.set_xlabel(r"$\lambda_{\max}(\hat{\Sigma})$", fontsize=11)
    ax.set_ylabel("Density", fontsize=11)
    ax.legend(fontsize=9)
plt.savefig("fig_a_distributions.png", dpi=150, bbox_inches="tight")
plt.show()

# Table (a): descriptive statistics
rows_a = []
for p in ps:
    d = results[p]
    rows_a.append({
        "p"       : p,
        "Mean"    : round(float(np.mean(d)), 4),
        "Std"     : round(float(np.std(d)),  4),
        "Median"  : round(float(np.median(d)), 4),
        "5th pct" : round(float(np.percentile(d,  5)), 4),
        "95th pct": round(float(np.percentile(d, 95)), 4),
        "MP edge" : round(mp_edge[p], 4),
    })
print("=== Part (a): Summary Statistics ===")
print(pd.DataFrame(rows_a).set_index("p").to_string())


# ──────────────────────────────────────────────────────────────────────────
# Part (b)  —  Marchenko–Pastur benchmark overlay + comparison table
# ──────────────────────────────────────────────────────────────────────────
# (reuses `results` and `mp_edge` from Part (a))

fig_b, axes_b = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)
fig_b.suptitle(
    r"Part (b) — $\lambda_{\max}(\hat{\Sigma})$ with MP benchmark, $n=100$",
    fontsize=13
)
for ax, p in zip(axes_b, ps):
    d    = results[p]
    edge = mp_edge[p]
    ax.hist(d, bins=40, color="steelblue", edgecolor="white", alpha=0.80, density=True)
    ax.axvline(edge, color="crimson", lw=2.0, ls="--",
               label=rf"$\lambda_+(p/n)={edge:.2f}$")
    ax.axvline(1.0,  color="black",   lw=1.4, ls=":",
               label="Null benchmark = 1")
    ax.set_title(rf"$p={p}$", fontsize=12)
    ax.set_xlabel(r"$\lambda_{\max}(\hat{\Sigma})$", fontsize=11)
    ax.set_ylabel("Density", fontsize=11)
    ax.legend(fontsize=8.5)
plt.savefig("fig_b_mp_benchmark.png", dpi=150, bbox_inches="tight")
plt.show()

# Table (b): benchmark vs. empirical
rows_b = []
for p in ps:
    d    = results[p]
    edge = mp_edge[p]
    rows_b.append({
        "p"            : p,
        "c = p/n"      : round(p / n, 4),
        "MP edge"      : round(edge, 4),
        "Emp. mean"    : round(float(np.mean(d)), 4),
        "Emp. 95th pct": round(float(np.percentile(d, 95)), 4),
        "Bias vs. 1"   : f"{(edge - 1) * 100:.1f}%",
    })
print("\n=== Part (b): Benchmark vs. Empirical ===")
print(pd.DataFrame(rows_b).set_index("p").to_string())


# ──────────────────────────────────────────────────────────────────────────
# Part (c)  —  Johnstone standardization, skewness, Q–Q plots
# ──────────────────────────────────────────────────────────────────────────
# (reuses `results` from Part (a))
ps_plot = [50, 500]
Z = {p: standardize(results[p], n, p) for p in ps_plot}

# Figure (c): 2×2 grid — row 0: histograms,  row 1: Q–Q plots
fig_c, axes_c = plt.subplots(2, 2, figsize=(11, 8), constrained_layout=True)
fig_c.suptitle(
    r"Part (c) — Johnstone-standardized $Z_{n,p}$: histogram & Normal Q–Q"
    f"  ($n={n}$, $B={B}$)",
    fontsize=13
)

for col, p in enumerate(ps_plot):
    z    = Z[p]
    skew = float(stats.skew(z))
    mu_z = float(np.mean(z))
    sd_z = float(np.std(z))

    # Histogram
    ax_h   = axes_c[0, col]
    x_grid = np.linspace(z.min() - 0.5, z.max() + 0.5, 300)
    ax_h.hist(z, bins=40, color="mediumseagreen", edgecolor="white",
              alpha=0.80, density=True, label="Empirical")
    ax_h.plot(x_grid, stats.norm.pdf(x_grid, mu_z, sd_z),
              color="navy", lw=1.6, ls="--",
              label=rf"$\mathcal{{N}}(\bar z,\,s^2)$")
    ax_h.axvline(0, color="gray", lw=1.0, ls=":")
    ax_h.set_title(rf"$p={p}$,  $\hat g_1={skew:.3f}$", fontsize=11)
    ax_h.set_xlabel(r"$Z_{n,p}$", fontsize=11)
    ax_h.set_ylabel("Density", fontsize=11)
    ax_h.legend(fontsize=9)

    # Q–Q plot
    ax_q = axes_c[1, col]
    (osm, osr), (slope, intercept, _) = stats.probplot(z, dist="norm")
    ax_q.scatter(osm, osr, s=12, alpha=0.6, color="mediumseagreen",
                 label="Sample quantiles")
    xl = np.array([osm[0], osm[-1]])
    ax_q.plot(xl, slope * xl + intercept,
              color="crimson", lw=1.8, label="Normal reference")
    ax_q.set_title(rf"Normal Q–Q: $p={p}$", fontsize=11)
    ax_q.set_xlabel("Theoretical normal quantiles", fontsize=10)
    ax_q.set_ylabel(r"Ordered $Z_{n,p}$", fontsize=10)
    ax_q.legend(fontsize=9)

plt.savefig("fig_c_tracy_widom.png", dpi=150, bbox_inches="tight")
plt.show()

# Table (c): empirical moments vs. theoretical TW1
rows_c = []
for p in ps_plot:
    z          = Z[p]
    mu_np, s_np = johnstone_params(n, p)
    rows_c.append({
        "p"            : p,
        "mu_np"        : round(mu_np, 2),
        "sigma_np"     : round(s_np, 3),
        "Emp. mean"    : round(float(np.mean(z)), 4),
        "Emp. std"     : round(float(np.std(z)),  4),
        "Emp. skewness": round(float(stats.skew(z)), 4),
        "TW1 skewness" : 0.2935,
    })
print("\n=== Part (c): Moments of Standardized Statistics ===")
print(pd.DataFrame(rows_c).set_index("p").to_string())
```