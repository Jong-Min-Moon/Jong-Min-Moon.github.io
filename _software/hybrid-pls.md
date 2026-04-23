---
layout: page
title: FSHybridPLS: Functional and Scalar Hybrid Partial Least Squares
description: Code for hybrid partial least squares.
importance: 2
---

[https://github.com/Jong-Min-Moon/FShybridPLS](https://github.com/Jong-Min-Moon/FShybridPLS)

**FSHybridPLS** is an R package designed to perform Partial Least Squares (PLS) regression on "hybrid" predictors. A hybrid predictor is a single mathematical object containing both **functional data** (curves, time-series represented as `fd` objects) and **scalar covariates** (standard numeric matrices).

This package defines a joint Hilbert space $\mathcal{H} = \mathcal{F} \times \mathbb{R}^p$ and implements the arithmetic and algorithms necessary to perform penalized PLS directly on this space.
This package provides an R implementation and simulation replications of my paper, “Hybrid Partial Least Squares Regression with Multiple Functional and Scalar Predictors,” co-authored with Professor Jeong Hoon Jang of the University of Texas Medical Branch.

## Installation

This package is generated using `litr`, a literate programming tool developed by Jacob Bien and Patrick Vossler (https://jacobbien.github.io/litr-project/). I used litr to build the package and you don't have to install litr just to use the package. To install the package:

```r
devtools::install("your_downloaded_directory/FSHybridPLS")
```



-----
 
 

#### Table of Contents
- [FSHybridPLS: Functional and Scalar Hybrid Partial Least Squares](#fshybridpls-functional-and-scalar-hybrid-partial-least-squares)
  - [Installation](#installation)
      - [Table of Contents](#table-of-contents)
- [Helper Functions](#helper-functions)
    - [compute\_gram\_matrix](#compute_gram_matrix)
    - [is\_same\_basis](#is_same_basis)
    - [are\_all\_gram\_matrices\_identical](#are_all_gram_matrices_identical)
    - [rep\_fd](#rep_fd)
- [Hybrid predictor class](#hybrid-predictor-class)
  - [Class definition and constructor](#class-definition-and-constructor)
    - [predictor\_hybrid](#predictor_hybrid)
    - [predictor\_hybrid\_from\_coef](#predictor_hybrid_from_coef)
  - [Basic arithmetic](#basic-arithmetic)
    - [add.predictor\_hybrid](#addpredictor_hybrid)
    - [subtr.predictor\_hybrid](#subtrpredictor_hybrid)
    - [scalar\_mul.predictor\_hybrid](#scalar_mulpredictor_hybrid)
    - [inprod.predictor\_hybrid](#inprodpredictor_hybrid)
    - [inprod\_pen.predictor\_hybrid](#inprod_penpredictor_hybrid)
    - [subset\_predictor\_hybrid](#subset_predictor_hybrid)
    - [replace\_obs\_hybrid](#replace_obs_hybrid)
    - [add\_broadcast (Matrix)](#add_broadcast-matrix)
    - [subtr\_broadcast (Matrix)](#subtr_broadcast-matrix)
- [One iteration](#one-iteration)
  - [small functions](#small-functions)
    - [get\_gram\_matrix\_block](#get_gram_matrix_block)
    - [get\_smoothing\_param\_hybrid](#get_smoothing_param_hybrid)
  - [PLS component computation](#pls-component-computation)
    - [get\_xi\_hat\_linear\_pen](#get_xi_hat_linear_pen)
    - [get\_rho](#get_rho)
  - [Response Residualization](#response-residualization)
    - [get\_nu](#get_nu)
    - [residualize\_y](#residualize_y)
  - [Predictor Residualization](#predictor-residualization)
    - [get\_delta](#get_delta)
    - [residualize\_predictor](#residualize_predictor)
- [Main algorithm](#main-algorithm)
    - [fit.hybridPLS](#fithybridpls)
- [Simulation tools](#simulation-tools)
  - [sample splitting](#sample-splitting)
    - [create\_idx\_train\_test](#create_idx_train_test)
    - [get\_idx\_train](#get_idx_train)
    - [create\_idx\_kfold](#create_idx_kfold)
    - [n\_sample.fd](#n_samplefd)
    - [split.all](#splitall)
  - [normalization](#normalization)
    - [curve\_normalize](#curve_normalize)
    - [curve\_normalize\_train\_test](#curve_normalize_train_test)
    - [scalar\_normalize](#scalar_normalize)
    - [scalar\_normalize\_train\_test](#scalar_normalize_train_test)
    - [btwn\_normalize\_train\_test](#btwn_normalize_train_test)
    - [split\_and\_normalize.all](#split_and_normalizeall)
  - [Baseline methods](#baseline-methods)
    - [fit\_hybrid\_pcr\_iterative](#fit_hybrid_pcr_iterative)
      - [1. Dimensionality Reduction](#1-dimensionality-reduction)
      - [2. Iterative Model Fitting](#2-iterative-model-fitting)
    - [fit\_pfr](#fit_pfr)
- [Kidney Data Preprocessing Pipeline](#kidney-data-preprocessing-pipeline)
- [Numerical Studies](#numerical-studies)
    - [1. `6_1_geometric_validation.R`](#1-6_1_geometric_validationr)
    - [2. `6_2_beta_estimation.R`](#2-6_2_beta_estimationr)
    - [3. `6_3_1_scenario_1.R`](#3-6_3_1_scenario_1r)
    - [4. `6_3_2_scenario_2.R`](#4-6_3_2_scenario_2r)
    - [5. `6_4_kidney_single_rep.R`](#5-6_4_kidney_single_repr)
 

# Helper Functions

### compute_gram_matrix

**Description:**
Calculates the Gram matrix for a given functional basis. The Gram matrix $G$ is a symmetric positive semi-definite matrix containing the inner products of the basis functions. Specifically, the entry $(i, j)$ corresponds to the integral of the product of the $i$-th and $j$-th basis functions over the domain:
$$G_{ij} = \langle b_i, b_j \rangle = \int b_i(t) b_j(t) \, dt$$

**Inputs:**

- `basis`: A basis object of class `basisfd` (typically created using the `fda` package).

**Output:**

- Returns a square numeric matrix where the entry at row $i$ and column $j$ is the inner product of basis functions $i$ and $j$.

```{r}
#' Compute the Gram matrix for a basis object
#'
#' This function calculates the inner product of a basis with itself to form
#' the Gram matrix.
#'
#' @param basis A basis object of class `basisfd` from the `fda` package.
#' @return A square matrix where entry (i,j) is the inner product of basis functions i and j.
#' @export
compute_gram_matrix <- function(basis) {
  # Ensure the input is a valid basis object from the fda package
  stopifnot(inherits(basis, "basisfd"))
  
  # Compute the inner product of the basis with itself
  # This calculates the integral of b_i(t) * b_j(t) using the metric defined on the basis
  fda::inprod(basis, basis) 
}
```

 


### is_same_basis

**Description:**
Checks if two composite functional data objects (represented as lists containing functional data) share the exact same basis functions. It verifies that both lists have the same length and that the basis for every corresponding element is identical.

**Inputs:**

- `input`: A list containing functional data objects (expected to have a `$functional_list` structure).
- `other`: Another list containing functional data objects to compare against.

**Output:**

- Returns `TRUE` if both lists have the same length and every corresponding basis is equivalent; otherwise returns `FALSE`.

```{r}
#' Check if two functional data lists share the same basis
#'
#' @description
#' Checks if two composite functional data objects share the exact same basis functions
#' by comparing their internal list structures.
#'
#' @param input A list containing functional data objects (expected to have a `$functional_list` structure).
#' @param other Another list containing functional data objects to compare against.
#' @return `TRUE` if both lists have the same length and every corresponding basis is equivalent; otherwise `FALSE`.
#' @export
is_same_basis <- function(input, other) {
  all(
    # Check if both lists have the same number of functional elements
    length(input$functional_list) == length(other$functional_list),
    
    # Check if the basis for each corresponding element is identical
    all(
      mapply(function(fd1, fd2) {
        # Use fda package function to check basis equality
        fda::is.eqbasis(fd1$basis, fd2$basis)
      }, input$functional_list, other$functional_list)
    )
  )
}
```

### are_all_gram_matrices_identical

**Description:**
Iterates through a list of matrices to verify if they are all numerically identical to the first matrix in the list. This function handles floating-point inaccuracies by using a tolerance parameter.

**Inputs:**

- `gram_list`: A list containing matrix objects to be compared.
- `tolerance` (Optional): A numeric value defining the tolerance for floating-point comparison. Defaults to the square root of machine epsilon.

**Output:**

- Returns `TRUE` if the list is empty, has one element, or if all matrices are identical to the first. Returns `FALSE` if any matrix differs.

```{r}
#' Check if all matrices in a list are identical (with tolerance for numeric comparison)
#'
#' This function iterates through a list of matrices and checks if all subsequent
#' matrices are numerically identical to the first matrix in the list.
#' It uses `all.equal` for robust comparison of numeric matrices, which accounts
#' for small floating-point differences.
#'
#' @param gram_list A list of matrices.
#' @param tolerance A numeric tolerance for comparing floating-point numbers.
#'                  Defaults to `sqrt(.Machine$double.eps)`.
#' @return A logical value: `TRUE` if all matrices are identical, `FALSE` otherwise.
#' @export
are_all_gram_matrices_identical <- function(gram_list, tolerance = sqrt(.Machine$double.eps)) {
  # Handle edge cases: empty list or list with a single matrix
  if (length(gram_list) == 0) {
    message("The input list is empty. Returning TRUE as there are no differences.")
    return(TRUE)
  }
  if (length(gram_list) == 1) {
    message("The input list contains only one matrix. Returning TRUE.")
    return(TRUE)
  }
  
  # Get the first matrix as the reference
  first_matrix <- gram_list[[1]]
  
  # Ensure the first element is a matrix
  if (!is.matrix(first_matrix)) {
    stop("The first element of 'gram_list' is not a matrix.")
  }
  
  # Iterate from the second matrix onwards and compare with the first
  for (i in 2:length(gram_list)) {
    current_matrix <- gram_list[[i]]
    
    # Ensure current element is a matrix
    if (!is.matrix(current_matrix)) {
      stop(paste("Element", i, "of 'gram_list' is not a matrix."))
    }
    
    # Compare the current matrix with the first matrix
    # all.equal returns TRUE if identical, or a character string describing differences
    # We convert the result to a logical TRUE/FALSE
    if (!isTRUE(all.equal(first_matrix, current_matrix, tolerance = tolerance))) {
      # If not equal, return FALSE immediately
      message(paste("Matrices at index 1 and", i, "are not identical."))
      return(FALSE)
    }
  }
  
  # If the loop completes, all matrices are identical
  return(TRUE)
}
```

 
### rep_fd

**Description:**
Takes a list of functional data objects (where each object represents a single sample/curve) and broadcasts them by replicating their coefficients. This creates new functional objects containing $n$ identical copies of the original curve.

**Inputs:**

- `fd_list`: A list of `fd` objects (functional data objects). Each object must have exactly one column of coefficients (a single sample).
- `n`: An integer specifying the number of replications desired.

**Output:**

- Returns a list of `fd` objects, where each object now contains $n$ replications of the original coefficients.

```{r}
#' Replicate a list of single-sample fd objects multiple times
#'
#' This function broadcasts a list of single-sample functional predictors
#' by replicating their coefficient columns.
#'
#' @param fd_list A list of `fd` objects, each representing a single sample.
#' @param n The number of replications desired.
#'
#' @return A list of `fd` objects, each with `n` replications.
#' @export
rep_fd <- function(fd_list, n) {
  # Validate input: must be a list of 'fd' objects
  if (!is.list(fd_list) || any(!vapply(fd_list, inherits, logical(1), "fd"))) {
    stop("Input must be a list of 'fd' objects.")
  }
  
  lapply(fd_list, function(fd_obj) {
    coef_mat <- fd_obj$coefs
    
    # Ensure the object represents a single sample (one column of coefficients)
    if (is.null(dim(coef_mat)) || ncol(coef_mat) != 1) {
      stop("Each fd object in the list must have one column of coefficients.")
    }
    
    # Create a new coefficient matrix by repeating the column 'n' times
    new_coefs <- matrix(rep(coef_mat, n), nrow = nrow(coef_mat), ncol = n)
    
    # Return a new fd object with the replicated coefficients and original basis
    fd(coef = new_coefs, basisobj = fd_obj$basis)
  })
}
```

# Hybrid predictor class

## Class definition and constructor
### predictor_hybrid

**Description:**
The `predictor_hybrid` class represents a hybrid random object $\mathbf{W} = (X, \mathbf{Z})$ that combines functional and scalar covariates into a unified Hilbert space structure.

- **Functional Part:** Let $\{X^{(k)}\}_{k=1, \ldots, K}$ be a collection of random functions defined on unit interval $\mathcal{T}_k := [0,1]$. Each $X^{(k)}$ belongs to $L^2([0,1])$, a Hilbert space of square-integrable functions. The multivariate functional object $X$ resides in the cartesian product space $\mathcal{F} = L^2([0,1]) \times \cdots \times L^2([0,1])$.
- **Hybrid Object:** We define the hybrid object $\mathbf{W} = (X, \mathbf{Z})$, where $\mathbf{Z}$ is a $p$-dimensional scalar covariate vector. This object belongs to the product space $\mathcal{H} = \mathcal{F} \times \mathbb{R}^p$.
- **Vector Notation:** The object can be evaluated at a multi-dimensional argument $\mathbf{t}$ as a $(K+p)$-dimensional vector: $\mathbf{W}[\mathbf{t}] = (X(\mathbf{t}), \mathbf{Z})^\top$.
- **Implementation:** The class is implemented as an S3 object containing a matrix for scalar parts, a list of `fd` objects for functional parts, and pre-computed Gram matrices to facilitate Hilbert space operations.

**Inputs:**

- `Z`: A numeric matrix of dimension $n/_sample /times n/_scalar$ representing the scalar predictors.
- `functional_list`: A list of functional predictors (typically `fd` objects from the `fda` package).
- `eval_point`: A specification for evaluation points (stored as metadata).

**Output:**

- Returns an object of class `predictor_hybrid`, which includes the original data, pre-computed Gram matrices, and roughness penalty matrices.

```{r Create a predictor_hybrid object}
#' Create a predictor_hybrid object
#'
#' @param Z Numeric matrix (n_sample x n_scalar).
#' @param functional_list List of 'fd' objects.
#' @param eval_point Evaluation points.
#' @param penalty_order Integer. Derivative order for roughness penalty (default 2).
#'
#' @export
predictor_hybrid <- function(Z, functional_list, eval_point, penalty_order = 2) {
  stopifnot(is.matrix(Z), is.numeric(Z), is.list(functional_list))
  
  n_sample <- nrow(Z)
  n_functional <- length(functional_list)
  
  gram_list <- vector("list", n_functional)
  gram_deriv_list <- vector("list", n_functional)
  n_basis_list <- numeric(n_functional)
  
  for (i in seq_len(n_functional)) {
    fd_i <- functional_list[[i]]
    basis_i <- fd_i$basis
    
    # 1. Validation
    if (ncol(fd_i$coefs) != n_sample) {
      stop(sprintf("Functional predictor %d sample count mismatch.", i))
    }
    
    # 2. Pre-compute Gram Matrix (Inner product of basis functions)
    # This is the "J" matrix: J_ij = <phi_i, phi_j>
    gram_list[[i]] <- fda::eval.penalty(basis_i, Lfdobj = 0)
    
    # 3. Pre-compute Penalty Matrix
    # This is the "R" matrix: R_ij = <D^2 phi_i, D^2 phi_j>
    gram_deriv_list[[i]] <- fda::eval.penalty(basis_i, Lfdobj = penalty_order)
    
    n_basis_list[i] <- basis_i$nbasis
  }
  
  structure(
    list(
      Z = Z,
      functional_list = functional_list,
      gram_list = gram_list,            # J matrices
      gram_deriv_list = gram_deriv_list, # R matrices
      eval_point = eval_point,
      n_basis_list = n_basis_list,
      n_sample = n_sample,
      n_functional = n_functional,
      n_scalar = ncol(Z)
    ),
    class = "predictor_hybrid"
  )
}
```



### predictor_hybrid_from_coef

**Description:**
An alternative constructor that creates a single-sample `predictor_hybrid` object from a flat numeric coefficient vector. It reconstructs both the functional and scalar components by mapping the coefficients back onto the basis functions defined in a template `format` object.

**Important:** This function strictly assumes that all functional predictors in the `format` object share the same number of basis functions (). It verifies this assumption before proceeding.

**Inputs:**

- `format`: A `predictor_hybrid` object serving as a template. It must contain the necessary basis information (`functional_list`) and structural metadata (`n_scalar`, `n_functional`).
- `coef`: A numeric vector of length , where:
-  is the number of functional predictors.
-  is the number of basis functions (strictly enforced to be identical across all functional predictors).
-  is the number of scalar predictors.



**Output:**

- Returns a `predictor_hybrid` object representing a single sample (`n_sample = 1`), containing:
- Functional predictors rebuilt from the first  coefficients.
- A scalar predictor matrix `Z` derived from the remaining  coefficients.

```{r}
#' Construct a Single-Sample Predictor Hybrid Object from Coefficients
#'
#' Reconstructs a \code{predictor_hybrid} object representing one observation, using a numeric
#' coefficient vector. This alternative constructor maps the coefficients back into their functional
#' and scalar predictor representations based on the structure of a template \code{predictor_hybrid} object.
#'
#' @param format A \code{predictor_hybrid} object that provides the structure and basis information.
#' @param coef A numeric vector containing coefficients for both functional and scalar predictors.
#'
#' @return A \code{predictor_hybrid} object with updated \code{functional_list}, \code{Z}, and \code{n_sample = 1}.
#' @export
predictor_hybrid_from_coef <- function(format, coef) {
  # Extract metadata from the template
  basis_counts <- format$n_basis_list
  
  # Check if all functional predictors have the same number of basis functions
  if (length(unique(basis_counts)) != 1) {
    stop("All functional predictors must have the same number of basis functions (M).")
  }
  
  M <- basis_counts[1]  # Number of basis functions (identical across predictors)
  K <- format$n_functional # Number of functional predictors
  
  # Reconstruct each functional predictor
  for (ii in 1:K) {
    # Calculate indices for the current functional predictor in the flat vector
    start_idx <- (ii - 1) * M + 1
    end_idx   <- ii * M
    
    # Create a new fd object using the sliced coefficients and original basis
    format$functional_list[[ii]] <- fd(
      coef = as.matrix(coef[start_idx:end_idx]),
      basisobj = format$functional_list[[ii]]$basis
    )
  }
  
  # Reconstruct the scalar predictor part (Z)
  # The remaining coefficients after K*M belong to the scalar predictors
  scalar_start_idx <- K * M + 1
  format$Z <- t(as.matrix(coef[scalar_start_idx:length(coef)]))
  
  # Update sample count to 1 as this constructor creates a single observation
  format$n_sample <- 1
  
  return(format)
}
```


 

## Basic arithmetic

### add.predictor_hybrid

**Description:**
Performs element-wise addition of two `predictor_hybrid` objects. Functional predictors are combined using `plus.fd()` and `times.fd()` from the `fda` package.

**Usage:**
```r
add.predictor_hybrid(input, other, alpha = 1)
```

**Arguments:**

- `input`: A `predictor_hybrid` object.
- `other`: Another `predictor_hybrid` object to be added.
- `alpha`: A scalar multiplier applied to `other` before addition (default is 1).

**Value:**

- Returns a new `predictor_hybrid` object representing the result of the addition.

**Details:**

- This function assumes both objects have the same number and structure of functional and scalar predictors.
- Functional parts are scaled by `alpha` using `times.fd()` and then summed using `plus.fd()`.
- Scalar predictors are added using standard matrix addition.
- Supports broadcasting if one object represents a single sample (`n_sample = 1`) and the other represents multiple samples.

```{r}
#' Add two predictor_hybrid objects
#'
#' Performs element-wise addition of two \code{predictor_hybrid} objects. 
#' Supports broadcasting if one object is a single sample.
#'
#' @param xi_1 A \code{predictor_hybrid} object.
#' @param xi_2 Another \code{predictor_hybrid} object to be added.
#' @param alpha A scalar multiplier applied to \code{xi_2} before addition (default is 1).
#'
#' @return A new \code{predictor_hybrid} object representing the result of the addition.
#' @export
add.predictor_hybrid <- function(xi_1, xi_2, alpha = 1) {
  # Safe access to is.eqbasis() from the fda namespace
  is_eqbasis <- getFromNamespace("is.eqbasis", "fda")
  
  # Type checks
  if (!inherits(xi_1, "predictor_hybrid") || !inherits(xi_2, "predictor_hybrid")) {
    stop("Both inputs must be of class 'predictor_hybrid'.")
  }
  
  # Structural checks: Number of functional and scalar predictors must match
  if (xi_1$n_functional != xi_2$n_functional) {
    stop("Mismatch in number of functional predictors.")
  }
  if (xi_1$n_scalar != xi_2$n_scalar) {
    stop("Mismatch in number of scalar predictors.")
  }
  
  # Basis checks: Ensure corresponding functional predictors share the same basis
  for (i in seq_len(xi_1$n_functional)) {
    if (!is_eqbasis(xi_1$functional_list[[i]]$basis, xi_2$functional_list[[i]]$basis)) {
      stop("Functional predictors must have the same basis.")
    }
  }
  
  # Broadcasting Logic:
  # Ensure xi_1 is always the larger object (or equal) to simplify broadcasting
  if (xi_1$n_sample == 1 && xi_2$n_sample > 1) {
    tmp <- xi_1
    xi_1 <- xi_2
    xi_2 <- tmp
  }
  
  n1 <- xi_1$n_sample
  n2 <- xi_2$n_sample
  
  # Validate sample compatibility
  if (!(n1 == n2 || n2 == 1)) {
    stop("Sample sizes are incompatible for broadcasting.")
  }
  
  # Prepare components
  f1 <- xi_1$functional_list
  f2 <- xi_2$functional_list
  Z1 <- xi_1$Z
  Z2 <- xi_2$Z
  
  # Replicate fd and Z if broadcasting is needed (n2 == 1)
  if (n2 == 1 && n1 > 1) {
    f2 <- rep_fd(f2, n1)
    Z2 <- matrix(rep(c(Z2), n1), nrow = n1, byrow = TRUE)
  }
  
  # Combine functional predictors: f1 + alpha * f2
  new_functional_list <- Map(
    function(fd1, fd2) plus.fd(fd1, times.fd(alpha, fd2)),
    f1,
    f2
  )
  
  # Combine scalar predictors: Z1 + alpha * Z2
  new_Z <- Z1 + alpha * Z2
  
  # Construct and return the new predictor_hybrid object
  # Note: eval_point is carried over from the first object
  predictor_hybrid(Z = new_Z, functional_list = new_functional_list, eval_point = xi_1$eval_point)
}
```

### subtr.predictor_hybrid

**Description:**
Performs element-wise subtraction of two `predictor_hybrid` objects. Internally uses `add.predictor_hybrid` to compute the result by negating the second operand.

**Usage:**
```r
subtr.predictor_hybrid(input, other, alpha = 1)
```

**Arguments:**

- `input`: A `predictor_hybrid` object.
- `other`: Another `predictor_hybrid` object to be subtracted.
- `alpha`: A scalar multiplier applied to `other` before subtraction (default is 1).

**Value:**

- Returns a new `predictor_hybrid` object representing the result of the subtraction.

**Details:**

- This function assumes both objects have the same number and structure of functional and scalar predictors.
- It performs subtraction by internally calling `add.predictor_hybrid()` with `-alpha`.
- Functional parts are scaled using `times.fd()` and subtracted via `plus.fd()` with a negated factor.
- Scalar predictors are subtracted using standard matrix arithmetic.

```{r}
#' Subtract two predictor_hybrid objects
#'
#' Performs element-wise subtraction of two `predictor_hybrid` objects.
#' Internally uses `add.predictor_hybrid(input, other, alpha = -1)`.
#'
#' @param input A `predictor_hybrid` object.
#' @param other Another `predictor_hybrid` object to subtract.
#' @param alpha A scalar multiplier applied to `other` before subtraction (default is 1).
#'
#' @return A new `predictor_hybrid` object representing the result of subtraction.
#' @export
subtr.predictor_hybrid <- function(input, other, alpha = 1) {
  
  add.predictor_hybrid(input, other, alpha = -alpha)
}
```

 

### scalar_mul.predictor_hybrid

**Description:**
Multiplies all components of a `predictor_hybrid` object by a scalar. Functional components are scaled using `times.fd()` from the `fda` package, and scalar predictors are multiplied directly using matrix operations.

**Usage:**
```r
scalar_mul.predictor_hybrid(input, scalar)

```

**Arguments:**

- `input`: A `predictor_hybrid` object.
- `scalar`: A numeric value used to scale both scalar and functional components.

**Value:**

- Returns a new `predictor_hybrid` object with all components scaled by `scalar`.

**Details:**

- Functional predictors are scaled using `times.fd(scalar, fd_obj)` for each element.
- Scalar predictors (the matrix `Z`) are scaled elementwise using matrix multiplication.

```{r}
#' Multiply a predictor_hybrid object by a scalar
#'
#' Performs scalar multiplication on both the scalar and functional components
#' of a `predictor_hybrid` object. Functional predictors are scaled using
#' `times.fd()` from the `fda` package.
#'
#' @param input A `predictor_hybrid` object.
#' @param scalar A numeric value to multiply all components by.
#'
#' @return A new `predictor_hybrid` object scaled by `scalar`.
#' @export
scalar_mul.predictor_hybrid <- function(input, scalar) {
  if (!inherits(input, "predictor_hybrid")) {
    stop("Input must be of class 'predictor_hybrid'.")
  }
  if (!is.numeric(scalar) || length(scalar) != 1) {
    stop("Scalar must be a single numeric value.")
  }

  # Scale functional components
  new_functional_list <- lapply(input$functional_list, function(fd_obj) {
    times.fd(scalar, fd_obj)
  })

  # Scale scalar predictors
  new_Z <- scalar * input$Z

  # Reconstruct hybrid object
  # Passing eval_point from the original input to maintain metadata
  predictor_hybrid(
    Z = new_Z,
    functional_list = new_functional_list,
    eval_point = input$eval_point
  )
}
```


### inprod.predictor_hybrid

**Description:**
Computes the inner product between two `predictor_hybrid` objects. The inner product in the hybrid space  is defined as the sum of the inner products of the functional components in  and the scalar components in :

**Inputs:**

- `xi_1`: A `predictor_hybrid` object.
- `xi_2`: (Optional) Another `predictor_hybrid` object. Defaults to `xi_1` (computes norm squared if `xi_1` is a single sample).

**Output:**

- A numeric vector of inner products. If both inputs are single samples, returns a scalar.

**Details:**

- Supports broadcasting: if one input has a single observation (`n_sample = 1`) and the other has multiple, the single observation is broadcast across the others.
- Uses `fda::inprod` for functional integration and matrix multiplication for scalar parts.
```{r}
#' Algebraic Inner Product for Hybrid Objects
#' 
#' Uses pre-computed Gram matrices to calculate inner products 
#' without numerical integration.
#'
#' @export
inprod.predictor_hybrid <- function(xi_1, xi_2 = NULL) {
  if (is.null(xi_2)) xi_2 <- xi_1
  
  # --- 1. Identify Broadcasting Case ---
  n1 <- xi_1$n_sample
  n2 <- xi_2$n_sample
  
  # Case A: 1-to-1 (Self-norm or pair-wise)
  # Case B: N-to-1 (Broadcasting / Projection)
  is_broadcasting <- (n2 == 1 && n1 > 1)
  
  if (n1 != n2 && !is_broadcasting) {
    # Attempt to swap if the user passed (1, N) instead of (N, 1)
    if (n1 == 1 && n2 > 1) {
       tmp <- xi_1; xi_1 <- xi_2; xi_2 <- tmp
       n1 <- xi_1$n_sample; n2 <- xi_2$n_sample
       is_broadcasting <- TRUE
    } else {
       stop("Incompatible sample sizes.")
    }
  }

  # --- 2. Scalar Component ---
  # Z1: (N x P), Z2: (N x P) or (1 x P)
  if (is_broadcasting) {
    # Project rows of Z1 onto single vector Z2
    # Result: (N x 1) -> vector
    term_scalar <- as.vector(xi_1$Z %*% t(xi_2$Z)) 
  } else {
    # Element-wise row sums
    term_scalar <- rowSums(xi_1$Z * xi_2$Z)
  }
  
  # --- 3. Functional Component (Algebraic) ---
  term_functional <- numeric(n1)
  
  for (k in seq_len(xi_1$n_functional)) {
    J <- xi_1$gram_list[[k]]       # (M x M)
    C1 <- xi_1$functional_list[[k]]$coefs # (M x N)
    C2 <- xi_2$functional_list[[k]]$coefs # (M x N) or (M x 1)
    
    # Calculate weighted coefficients: J * C2
    J_C2 <- J %*% C2 # (M x N) or (M x 1)
    
    if (is_broadcasting) {
      # Proj = C1^T * J * c2
      # Dimension: (N x M) * (M x 1) = (N x 1)
      term_functional <- term_functional + as.vector(t(C1) %*% J_C2)
    } else {
      # Pairwise = diag(C1^T * J * C2)
      # Efficiently: colSums(C1 * (J * C2))
      # This calculates dot product of each column pair
      term_functional <- term_functional + colSums(C1 * J_C2)
    }
  }
  
  return(term_scalar + term_functional)
}
```

 
### inprod_pen.predictor_hybrid

**Description:**
Computes the penalized inner product between two `predictor_hybrid` objects. This adds a roughness penalty term to the standard inner product, typically used for regularization.


**Inputs:**

- `xi_1`: A `predictor_hybrid` object.
- `xi_2`: (Optional) Another `predictor_hybrid` object.
- `lambda`: A numeric vector of length  (number of functional predictors) specifying the smoothing parameter for each function.

**Output:**

- A numeric vector (or scalar) representing the penalized inner product.
```{r Penalized Inner Product}
#' Penalized Inner Product (Algebraic)
#'
#' @export
inprod_pen.predictor_hybrid <- function(xi_1, xi_2 = NULL, lambda) {
  # 1. Base Inner Product (Unpenalized)
  base_val <- inprod.predictor_hybrid(xi_1, xi_2)
  
  if (is.null(xi_2)) xi_2 <- xi_1
  
  # Determine dimensions for manual penalty calculation
  n1 <- xi_1$n_sample
  n2 <- xi_2$n_sample
  is_broadcasting <- (n2 == 1 && n1 > 1)
  # Handle the swap if inprod swapped them, or just rely on logic
  if (n1 == 1 && n2 > 1) {
     tmp <- xi_1; xi_1 <- xi_2; xi_2 <- tmp
     n1 <- xi_1$n_sample; n2 <- xi_2$n_sample
     is_broadcasting <- TRUE
  }

  penalty_val <- numeric(n1)

  # 2. Add Roughness Penalty
  for (k in seq_len(xi_1$n_functional)) {
    if (lambda[k] == 0) next # Skip if no penalty
    
    R  <- xi_1$gram_deriv_list[[k]] # (M x M) - The penalty matrix
    C1 <- xi_1$functional_list[[k]]$coefs
    C2 <- xi_2$functional_list[[k]]$coefs
    
    R_C2 <- R %*% C2
    
    if (is_broadcasting) {
      term <- as.vector(t(C1) %*% R_C2)
    } else {
      term <- colSums(C1 * R_C2)
    }
    
    penalty_val <- penalty_val + (lambda[k] * term)
  }
  
  return(base_val + penalty_val)
}
```


### subset_predictor_hybrid

**Description:**
Extracts a specific observation from a multi-sample `predictor_hybrid` object and returns it as a new, single-sample `predictor_hybrid` object.

**Inputs:**

- `W`: A `predictor_hybrid` object containing multiple samples.
- `i`: Integer index of the sample to extract.

**Output:**

- A `predictor_hybrid` object containing only the -th observation.

```{r}
#' Extract a single observation from a predictor_hybrid object
#'
#' @param W A predictor_hybrid object with multiple samples.
#' @param i Integer index of the sample to extract.
#' @return A single-sample predictor_hybrid object.
#' @export
subset_predictor_hybrid <- function(W, i) {
  # Extract the i-th row of the scalar matrix
  new_Z <- matrix(W$Z[i, ], nrow = 1)
  
  # Extract the i-th column of coefficients for each functional object
  new_functional_list <- lapply(W$functional_list, function(fdobj) {
    fd(coef = matrix(coef(fdobj)[, i], ncol = 1), basisobj = fdobj$basis)
  })
  
  # Construct new object
  new_predictor <- predictor_hybrid(
    Z = new_Z, 
    functional_list = new_functional_list,
    eval_point = W$eval_point
  )
  
  return(new_predictor)
}
```



### replace_obs_hybrid

**Description:**
Replaces a specific observation within a `predictor_hybrid` object with a new single-sample hybrid object. This effectively updates the -th row of the scalar matrix and the -th column of the functional coefficients.

**Inputs:**

- `W`: The target `predictor_hybrid` object.
- `i`: The integer index of the observation to replace.
- `new_W`: The source `predictor_hybrid` object (must be a single sample).

**Output:**

- The modified `W` object.

```{r}
#' Replace a single observation in a predictor_hybrid object
#'
#' Replaces the i-th observation of a predictor_hybrid object with a new
#' single-sample predictor_hybrid object.
#'
#' @param W A predictor_hybrid object with one or more samples.
#' @param i An integer index specifying the observation to replace.
#' @param new_W A single-sample predictor_hybrid object to use for replacement.
#'
#' @return A predictor_hybrid object with the i-th observation replaced.
#' @export
replace_obs_hybrid <- function(W, i, new_W) {
  # Input validation
  if (!inherits(W, "predictor_hybrid") || !inherits(new_W, "predictor_hybrid")) {
    stop("Both W and new_W must be of class 'predictor_hybrid'.")
  }
  if (new_W$n_sample != 1) {
    stop("new_W must be a single-sample predictor_hybrid object.")
  }
  if (i < 1 || i > W$n_sample) {
    stop(paste("Index i must be between 1 and", W$n_sample))
  }
  if (W$n_scalar != new_W$n_scalar) {
    stop("Mismatch in number of scalar predictors.")
  }
  if (W$n_functional != new_W$n_functional) {
    stop("Mismatch in number of functional predictors.")
  }

  # Check for compatible basis objects
  is_eqbasis <- getFromNamespace("is.eqbasis", "fda")
  for (j in seq_len(W$n_functional)) {
    if (!is_eqbasis(W$functional_list[[j]]$basis, new_W$functional_list[[j]]$basis)) {
      stop("Functional predictors must have the same basis objects.")
    }
  }

  # Replace the i-th observation in the scalar matrix Z
  W$Z[i, ] <- new_W$Z[1, ]

  # Replace the i-th observation in each functional predictor
  for (j in seq_along(W$functional_list)) {
    # The coefficients are stored as a matrix, with columns corresponding to samples
    W$functional_list[[j]]$coefs[, i] <- new_W$functional_list[[j]]$coefs[, 1]
  }

  return(W)
}
```


### add_broadcast (Matrix)

**Description:**
A function that performs row-wise addition of a vector to a matrix. It broadcasts a single observation (vector) across all rows of the target matrix, verifying that the input is a matrix and the operand is a single observation.

**Inputs:**

- `input`: A numeric matrix.
- `other`: A numeric vector or a 1-row matrix to be added to every row of `input`.
- `alpha`: A scalar multiplier applied to `other` before addition.

**Output:**

- A matrix of the same dimensions as `input`.

```{r}
#' Broadcast Addition for Matrices
#'
#' Adds a single observation (vector) to every row of a matrix.
#' Checks that the input is a matrix and the operand is a single observation.
#'
#' @param input A numeric matrix.
#' @param other A numeric vector or a 1-row matrix.
#' @param alpha A scalar multiplier (default 1).
#' @return A matrix with the broadcasted addition applied.
#' @export
add_broadcast <- function(input, other, alpha = 1) {
  
  # 1. Type Check: Ensure input is a matrix
  if (!is.matrix(input)) {
    stop("Argument 'input' must be a matrix.")
  }

  # 2. Structural Check: Ensure RHS is a single observation.
  # This uses length() for vectors, and dim()[1] for matrices.
  is_matrix_other <- is.matrix(other)
  if (is_matrix_other && dim(other)[1] > 1) {
    stop("Argument 'other' must be a vector or a single-row matrix.")
  }

  # 3. Conversion: Convert a single-row matrix into a vector for broadcasting.
  # If 'other' is already a vector, this does nothing.
  if (is_matrix_other) {
    other <- as.vector(other)
  }
  
  # 4. Dimension Check: Ensure vector length matches matrix columns
  if (length(other) != ncol(input)) {
    stop("Length of 'other' must match number of columns in 'input'.")
  }

  # 5. Native Arithmetic: Use simple R arithmetic for high performance.
  # R broadcasts the vector 'other' across the rows of the matrix 'input'.
  # Transposing twice (t(t(...) ...)) ensures correct column-wise recycling 
  # logic is applied to rows.
  return(t(t(input) + alpha * other))
}
```
 

### subtr_broadcast (Matrix)

**Description:**
A function that performs row-wise subtraction of a vector from a matrix. It is a wrapper around `add_broadcast` that applies a negative multiplier.

**Inputs:**

- `input`: A numeric matrix.
- `other`: A numeric vector or a 1-row matrix to subtract from every row of `input`.
- `alpha`: A scalar multiplier applied to `other` (default 1).

**Output:**

- A matrix of the same dimensions as `input`.

```{r}
#' Broadcast Subtraction for Matrices
#'
#' Subtracts a single observation (vector) from every row of a matrix.
#'
#' @param input A numeric matrix.
#' @param other A numeric vector or a 1-row matrix.
#' @param alpha A scalar multiplier (default 1).
#' @return A matrix with the broadcasted subtraction applied.
#' @export
subtr_broadcast <- function(input, other, alpha = 1) {
  # Reuse add_broadcast with negated alpha
  add_broadcast(input, other, (-1 * alpha))
}
```

# One iteration

## small functions

### get_gram_matrix_block

**Description:**
Constructs the block-diagonal Gram matrix  for a hybrid predictor object. This matrix represents the inner product structure of the combined functional and scalar space. It is defined as:



where:

-  is the Gram matrix of the basis functions for the -th functional predictor, with entries .
-  is the identity matrix corresponding to the  scalar predictors (implying a standard Euclidean inner product for the scalar part).

**Inputs:**

- `obj`: A `predictor_hybrid` object containing the pre-computed Gram matrices (`gram_list`) and metadata.

**Output:**

- A sparse block-diagonal matrix (class `dgCMatrix` from the `Matrix` package) representing the global Gram matrix.
```{r}
#' Construct block-diagonal Gram matrix for hybrid predictor
#'
#' Creates a unified Gram matrix by placing the pre-computed functional Gram matrices
#' and a scalar identity matrix into a block-diagonal structure.
#'
#' @param obj A `predictor_hybrid` object.
#'
#' @return A sparse block-diagonal matrix of size `(total_dim x total_dim)`, where
#' `total_dim` is the sum of all functional basis sizes plus the number of scalar predictors.
#' @export
get_gram_matrix_block <- function(obj) {
  # Input validation
  if (!inherits(obj, "predictor_hybrid")) {
    stop("Input must be of class 'predictor_hybrid'.")
  }

  # 1. Retrieve the list of functional Gram matrices (pre-computed in the object)
  #    These correspond to the J^(k) blocks.
  gram_blocks <- obj$gram_list
  
  # 2. Append the Identity matrix for the scalar components
  #    This corresponds to the I_p block.
  #    We use 'diag' to create an Identity matrix of size n_scalar x n_scalar.
  gram_blocks[[length(gram_blocks) + 1]] <- diag(obj$n_scalar)
  
  # 3. Construct the sparse block-diagonal matrix
  #    Matrix::bdiag efficiently handles the block construction.
  Matrix::bdiag(gram_blocks)
}
```


### get_smoothing_param_hybrid

**Description:**
Constructs the block-diagonal smoothing parameter matrix . This matrix defines the regularization penalties applied to the coefficients. It is defined as:



where:

-  is the smoothing parameter for the -th functional predictor.
-  is the identity matrix of size  (the number of basis functions for predictor ).
-  is a zero matrix, indicating that the scalar predictors are not penalized in this step.

**Inputs:**

- `W`: A `predictor_hybrid` object providing dimension information.
- `lambda`: A numeric vector of length  (number of functional predictors). Each entry represents the penalty weight .

**Output:**

- A sparse block-diagonal matrix where the diagonal blocks contain the penalty weights for functional parts and zeros for the scalar part.
```{r}
#' Construct block-diagonal smoothing parameter matrix
#'
#' Generates a block-diagonal matrix containing regularization parameters. 
#' Functional coefficients are penalized by scaled identity matrices, while 
#' scalar coefficients receive zero penalty.
#'
#' @param W A `predictor_hybrid` object.
#' @param lambda A numeric vector of smoothing parameters, one for each functional predictor.
#'
#' @return A sparse block-diagonal matrix. The top-left blocks are `lambda[k] * I`, 
#' and the bottom-right block is a zero matrix for scalar covariates.
#' @export
get_smoothing_param_hybrid <- function(W, lambda) {
  # Input validation
  if (!inherits(W, "predictor_hybrid")) {
    stop("Input W must be of class 'predictor_hybrid'.")
  }
  if (length(lambda) != W$n_functional) {
    stop("Length of lambda must match the number of functional predictors.")
  }

  # 1. Create penalty blocks for functional predictors
  #    For each predictor k, create a scaled identity matrix: lambda[k] * I_Mk
  lambda_blocks <- lapply(seq_len(W$n_functional), function(ii) {
    nb <- W$functional_list[[ii]]$basis$nbasis
    lambda[ii] * diag(nb)
  })

  # 2. Create zero block for scalar predictors
  #    Scalar predictors are not penalized in this matrix, so we append a p x p zero matrix.
  lambda_blocks[[W$n_functional + 1]] <- matrix(0, nrow = W$n_scalar, ncol = W$n_scalar)

  # 3. Construct the sparse block-diagonal matrix
  Matrix::bdiag(lambda_blocks)
}
```

## PLS component computation 
 

### get_xi_hat_linear_pen

**Description:**
Computes the penalized PLS weight vector (direction) , represented as a `predictor_hybrid` object. This function solves for the coefficients that maximize the covariance between the predictor and the response , subject to a roughness penalty.

The optimization problem leads to a system of linear equations for each functional component :



where:

-  is the Gram matrix (`gram_list`).
-  is the penalty matrix (`gram_deriv_list`).
-  are the basis coefficients of the functional data.
-  are the coefficients for the -th functional weight.

For the scalar part, the weights are simply the inner products . The final coefficient vector is normalized by the -norm (defined by the penalized inner product structure).

**Inputs:**

- `W`: A `predictor_hybrid` object containing the predictors.
- `y`: A numeric vector of response values (length ).
- `lambda`: A numeric vector of smoothing parameters (one for each functional predictor).

**Output:**

- A single-sample `predictor_hybrid` object representing the estimated direction .

```{r}
#' Compute Penalized PLS Weight Vector (Linear)
#'
#' Solves for the PLS weight direction xi that maximizes the covariance with y,
#' subject to roughness penalties on the functional components.
#'
#' @param W A `predictor_hybrid` object.
#' @param y A numeric vector of response values.
#' @param lambda A numeric vector of smoothing parameters.
#'
#' @return A single-sample `predictor_hybrid` object representing the weight direction xi.
#' @export
get_xi_hat_linear_pen <- function(W, y, lambda) {
  
  n <- W$n_sample
  K <- W$n_functional
  u <- gamma <- list()

  # --- Scalar Component ---
  # Compute scalar weights: v = Z^T * y
  v <- t(W$Z) %*% y
  
  # Initialize squared norm q with scalar part contribution
  # q = ||xi||^2_pen = sum(v^2) + functional_parts
  q <- sum(v^2)

  # --- Functional Components ---
  for (j in 1:K) {
    # Theta_t: coefficient matrix of the functional data (basis x samples)
    Theta_t <- W$functional_list[[j]]$coefs
    
    # B: Gram matrix for the j-th basis
    B <- W$gram_list[[j]]
    
    # Compute RHS of the linear system: u = B * Theta * y
    # This represents the unpenalized gradient term
    u[[j]] <- B %*% Theta_t %*% y

    # Linear System Matrix: R = Gram + lambda * Penalty
    R <- W$gram_list[[j]] + lambda[j] * W$gram_deriv_list[[j]]
    
    # Solve for gamma_j: (Gram + Penalty) * gamma = Gram * Theta * y
    gamma[[j]] <- solve(R, u[[j]])

    # Update squared norm q:
    # Add contribution gamma^T * R * gamma (penalized norm of functional weight)
    q <- q + sum(gamma[[j]] * (R %*% gamma[[j]]))
  }
  
  # --- Combine and Normalize ---
  # Flatten gamma list and append scalar weights v
  d_vec <- c(do.call(c, gamma), v)
  
  # Normalize the vector to have unit penalized norm
  d_vec <- d_vec / sqrt(q)
  
  # Reconstruct the result as a predictor_hybrid object
  xi_hat <- predictor_hybrid_from_coef(format = W, coef = d_vec)
  
  return(xi_hat)
}
```
 

### get_rho

**Description:**
Computes the vector of PLS scores  by projecting the hybrid predictor data  onto the weight direction vector  (which represents ).

The projection is computed as:



where:

-  is the coefficient matrix for the -th functional predictor ().
-  is the Gram matrix ().
-  are the coefficients for the -th functional weight.
-  are the coefficients for the scalar weight.

**Inputs:**

- `d_vec`: A numeric vector containing the concatenated coefficients for all functional and scalar weights.
- `W`: A `predictor_hybrid` object providing the data and Gram matrices.

**Output:**

- A numeric vector of length  containing the PLS scores.

```{r}
#' Exact Hybrid Inner Product
#' Computes <W, xi> using basis inner product matrices.
#' @param W The hybrid predictor object (contains coefs for N samples)
#' @param xi The hybrid weight object (contains coefs for 1 direction)
#' @return A vector of scores (length N)
get_rho <- function(W, xi) {
  
  # 1. Scalar Part (Standard dot product)
  # (N x p_scalar) %*% (p_scalar x 1)
  scores <- as.matrix(W$Z) %*% as.matrix(xi$Z)
  
  # 2. Functional Part (Basis Matrix Algebra)
  # Loop through each functional variable
  for(k in seq_along(W$functional_list)) {
    
    # Extract basis and coefficients
    # Coefs_W is (Basis_Dim x N)
    # Coefs_xi is (Basis_Dim x 1)
    fd_W  <- W$functional_list[[k]]
    fd_xi <- xi$functional_list[[k]]
    
    # A. Compute J Matrix (Basis Inner Product)
    # J[i,j] = Integral(phi_i(t) * phi_j(t) dt)
    # Note: computed once per variable, very fast for B-splines
    J <- fda::inprod(fd_W$basis, fd_W$basis)
    
    # B. Compute Integral via Matrix Multiplication
    # Formula: Score = Coefs_W^T * J * Coefs_xi
    # Dimensions: (N x B) * (B x B) * (B x 1) -> (N x 1)
    
    # Optimization: Pre-multiply J * xi to get a "weighted weight"
    weighted_xi <- J %*% fd_xi$coefs 
    
    # Project data onto this weighted weight
    scores <- scores + t(fd_W$coefs) %*% weighted_xi
  }
  
  return(as.vector(scores))
}
```


 
 

## Response Residualization

### get_nu

**Description:**
Calculates the scalar regression coefficient  obtained by regressing the response vector  onto the PLS score vector . This minimizes the least squares error .


**Inputs:**

- `y`: A numeric vector of response values.
- `rho`: A numeric vector of PLS scores.

**Output:**

- A scalar value .
```{r}
#' Compute scalar regression coefficient (nu)
#'
#' Calculates the projection coefficient of the response vector y onto the score vector rho.
#'
#' @param y A numeric vector of response values.
#' @param rho A numeric vector of PLS scores.
#'
#' @return A scalar regression coefficient.
#' @export
get_nu <- function(y, rho) {
  # Compute numerator: inner product of y and rho
  # Compute denominator: squared norm of rho
  nu <- sum(y * rho) / sum(rho * rho)
  return(nu)
}
```
 

### residualize_y

**Description:**
Computes the residual of the response vector  after removing the component explained by the current PLS score .


**Inputs:**

- `y`: The current response vector.
- `rho`: The current PLS score vector.
- `nu`: The regression coefficient computed by `get_nu`.

**Output:**

- A numeric vector of residuals.

```{r}
#' Residualize the response vector
#'
#' Subtracts the projection of y onto rho from y.
#'
#' @param y The current response vector.
#' @param rho The current PLS score vector.
#' @param nu The regression coefficient.
#'
#' @return The residualized response vector.
#' @export
residualize_y <- function(y, rho, nu) {
  y_next <- y - nu * rho
  return(y_next)
}
```
 
 

## Predictor Residualization

### get_delta

**Description:**
Computes the hybrid regression coefficient  for regressing the predictor  onto the PLS scores .  is a single-sample `predictor_hybrid` object representing the direction in the predictor space that corresponds to .


**Inputs:**

- `W`: A `predictor_hybrid` object containing  samples.
- `rho`: A numeric vector of PLS scores (length ).

**Output:**

- A single-sample `predictor_hybrid` object .
```{r}
#' Compute hybrid regression coefficient (delta)
#'
#' Calculates the weighted average of the predictor observations W_i,
#' weighted by the scores rho_i.
#'
#' @param W A `predictor_hybrid` object.
#' @param rho A numeric vector of PLS scores.
#'
#' @return A single-sample `predictor_hybrid` object representing delta.
#' @export
get_delta <- function(W, rho) {
  # Initialize delta with the first weighted observation: rho[1] * W[1]
  delta <- scalar_mul.predictor_hybrid(subset_predictor_hybrid(W, 1), rho[1])
  
  # Iteratively add the remaining weighted observations: delta += rho[i] * W[i]
  for (i in 2:length(rho)) {
    W_i <- subset_predictor_hybrid(W, i)
    delta <- add.predictor_hybrid(delta, W_i, rho[i])
  }
  
  # Normalize by the squared norm of rho
  delta <- scalar_mul.predictor_hybrid(delta, 1 / sum(rho * rho))
  
  return(delta)
}
```



### residualize_predictor

**Description:**
Computes the residuals of the predictor object  by subtracting the component explained by .


**Inputs:**

- `W`: The current `predictor_hybrid` object.
- `rho`: The current PLS score vector.
- `delta`: The hybrid regression coefficient (from `get_delta`).

**Output:**

- A `predictor_hybrid` object containing the residualized predictors.
```{r}
#' Residualize the hybrid predictor
#'
#' Updates each observation in W by subtracting the projection onto rho (rho_i * delta).
#'
#' @param W The current `predictor_hybrid` object.
#' @param rho The current PLS score vector.
#' @param delta The hybrid regression coefficient (single-sample object).
#'
#' @return The residualized `predictor_hybrid` object.
#' @export
residualize_predictor <- function(W, rho, delta) {
  n <- length(rho)
  W_res <- W
  
  # Iterate through each sample to compute residuals
  for (i in 1:n) {
    # Extract the i-th observation
    W_i <- subset_predictor_hybrid(W, i)
    
    # Calculate residual: W_i_new = W_i - rho[i] * delta
    W_res_i <- subtr.predictor_hybrid(W_i, delta, rho[i])
    
    # Replace the observation in the result object
    W_res <- replace_obs_hybrid(W_res, i, W_res_i)
  }
  
  return(W_res)
}
```

 
# Main algorithm

### fit.hybridPLS

**Description:**
Implements the Hybrid Penalized Partial Least Squares (PLS) algorithm. This function iteratively extracts latent components that maximize the covariance between the hybrid predictors and the response, subject to roughness penalties.

**Algorithm Steps:**
For each iteration :

1. **Weight Direction ():** Computes the penalized weight vector that maximizes covariance with the current response residual .
2. **Scores ():** Projects the current predictor residuals  onto the weight direction to obtain PLS scores.
3. **loadings ():** Computes the regression coefficients for projecting  and  onto the scores .
4. **Deflation:** Updates the predictor  and response  by removing the variance explained by the current component (residualization).
5. **Coefficient Update:** Computes the "whitened" direction  (transforming weights back to the original predictor space) and updates the cumulative regression coefficient .

**Inputs:**

- `W`: Initial `predictor_hybrid` object.
- `y`: Numeric vector of response values.
- `n_iter`: Integer specifying the number of PLS components to extract.
- `lambda`: Numeric vector of smoothing parameters (one for each functional predictor).

**Output:**

- A list containing:
- `rho`: List of score vectors for each component.
- `xi`: List of weight directions (hybrid objects).
- `W`: List of residualized predictor objects at each step.
- `beta`: List of cumulative regression coefficients (hybrid objects) at each step.

```{r}
#' Fit Hybrid Penalized PLS with Optional Validation
#'
#' Runs the iterative PLS algorithm. If 'validation_data' is provided,
#' it computes and stores the RMSE on the validation set for each component.
#'
#' @param W Initial `predictor_hybrid` object (Training).
#' @param y Numeric vector of response values (Training).
#' @param n_iter Integer, number of components to extract.
#' @param lambda Numeric vector of smoothing parameters.
#' @param validation_data (Optional) A list containing `W_test` (predictor_hybrid) and `y_test`.
#'
#' @return A list containing the model (rho, xi, beta) and optional `validation_rmse`.
#' @export
fit.hybridPLS <- function(W, y, n_iter, lambda, validation_data = NULL) {
  # 1. Initialize storage
  W_now <- rho <- xi <- delta <- nu <- iota <- beta <- list()
  validation_rmse <- numeric(n_iter)
  
  # 2. Initialize current state
  W_now[[1]] <- W
  y_now <- y
  
  # 3. Main PLS Loop
  for (l in 1:n_iter) {
    # --- Step A: Weight Direction (xi) ---
    xi[[l]] <- get_xi_hat_linear_pen(W_now[[l]], y_now, lambda)
    
    # --- Step B: Scores (rho) ---
    rho[[l]] <- inprod.predictor_hybrid(W_now[[l]], xi[[l]])
    
    # --- Step C: Loadings (delta, nu) ---
    delta[[l]] <- get_delta(W_now[[l]], rho[[l]])
    nu[[l]] <- get_nu(y_now, rho[[l]])
    
    # --- Step D: Deflation ---
    W_now[[l + 1]] <- residualize_predictor(W_now[[l]], rho[[l]], delta[[l]])
    y_now <- residualize_y(y_now, rho[[l]], nu[[l]])
    
    # --- Step E: Cumulative Coefficient (Beta) ---
    iota[[l]] <- xi[[l]]
    
    if (l == 1) {
      beta[[l]] <- scalar_mul.predictor_hybrid(iota[[l]], nu[[l]])
    } else {
      for (u in 1:(l - 1)) {
        adjustment <- inprod.predictor_hybrid(delta[[u]], xi[[l]])
        iota[[l]] <- subtr.predictor_hybrid(iota[[l]], iota[[u]], adjustment)
      }
      beta[[l]] <- add.predictor_hybrid(beta[[l - 1]], iota[[l]], nu[[l]])
    }
    
    # --- Step F: Validation (Optional) ---
    if (!is.null(validation_data)) {
      # Predict on test set using the current cumulative beta
      y_pred_test <- inprod.predictor_hybrid(validation_data$W_test, beta[[l]])
      
      # Compute RMSE (standardized scale usually, but here just raw RMSE)
      validation_rmse[l] <- sqrt(mean((validation_data$y_test - y_pred_test)^2))
    }
  }
  
  return(list(
    rho = rho,
    xi = xi,
    beta = beta,
    W = W_now,
    delta = delta,
    nu = nu,
    validation_rmse = if (!is.null(validation_data)) validation_rmse else NULL
  ))
}
```

  

# Simulation tools

## sample splitting

### create_idx_train_test

**Description:**
Randomly splits the indices of a dataset into training and testing sets based on a specified ratio. This function ensures that the indices are sorted and returned as a list containing both sets.

**Usage:**

```r
create_idx_train_test(n_sample, train_ratio)

```

**Arguments:**

- `n_sample`: Integer. The total number of samples in the dataset.
- `train_ratio`: Numeric. The proportion of samples to include in the training set (between 0 and 1).

**Value:**

- A list containing:
  - `idx_train`: A sorted integer vector of training indices.
  - `idx_test`: A sorted integer vector of testing indices.

```{r}
#' Split Sample Indices into Train and Test Sets
#'
#' Randomly partitions the indices of a dataset into training and testing sets.
#'
#' @param n_sample Integer. The total number of samples.
#' @param train_ratio Numeric. The proportion of samples for the training set (0 to 1).
#'
#' @return A list with named elements `idx_train` and `idx_test`.
#' @export
create_idx_train_test <- function(n_sample, train_ratio) {
  # Calculate number of training samples
  n_train <- floor(n_sample * train_ratio)
  
  # Sample indices without replacement
  idx_train <- sort(sample(seq_len(n_sample), n_train, replace = FALSE))
  
  # The remaining indices form the test set
  idx_test <- sort(setdiff(seq_len(n_sample), idx_train))
  
  return(list(
    idx_train = idx_train,
    idx_test = idx_test
  ))
}
```




### get_idx_train

**Description:**
A simplified version of the splitting function that returns only the training indices. Useful when the testing set is defined implicitly as the complement or not immediately needed.

**Usage:**

```r
get_idx_train(n_sample, train_ratio)

```

**Arguments:**

- `n_sample`: Integer. The total number of samples.
- `train_ratio`: Numeric. The proportion of samples for the training set.

**Value:**

- A sorted integer vector of training indices.

```{r}
#' Generate Train Indices
#'
#' Randomly generates a sorted vector of indices for a training set.
#'
#' @param n_sample Integer. Number of samples.
#' @param train_ratio Numeric. Ratio of train samples.
#' @return Vector of sorted train indices.
#' @export
get_idx_train <- function(n_sample, train_ratio) {
  n_train <- floor(n_sample * train_ratio)
  idx_train <- sort(sample(seq_len(n_sample), n_train, replace = FALSE))
  return(idx_train)
}
```



### create_idx_kfold

**Description:**
Generates indices for K-fold cross-validation. It relies on the `caret` package to create balanced folds and organizes them into pairs of training and validation indices for each fold.

**Usage:**

```r
create_idx_kfold(n_sample, n_fold)

```

**Arguments:**

- `n_sample`: Integer. The total number of samples.
- `n_fold`: Integer. The number of folds to create.

**Value:**

- A list of length `n_fold`. Each element is a list containing:
  - `idx_train`: Indices for training in this fold.
  - `idx_valid`: Indices for validation in this fold.


```{r}
#' Generate K-Fold Cross-Validation Indices
#'
#' Creates a list of training and validation indices for K-fold cross-validation.
#' Uses `caret::createFolds` to ensure stratified or random splitting.
#'
#' @param n_sample Integer. The total number of samples.
#' @param n_fold Integer. The number of folds.
#'
#' @return A list of lists, where each sub-list contains `idx_train` and `idx_valid`.
#' @export
create_idx_kfold <- function(n_sample, n_fold) {
  # Generate folds using caret (returns validation indices by default)
  idx_list <- caret::createFolds(seq_len(n_sample), k = n_fold, list = TRUE, returnTrain = FALSE)
  
  idx_list_list <- vector("list", length(idx_list))
  
  for (i in seq_along(idx_list)) {
    valid_hyper_index <- idx_list[[i]]
    # Training set is the complement of the validation set
    train_hyper_index <- setdiff(seq_len(n_sample), valid_hyper_index)
    
    idx_list_list[[i]] <- list(
      "idx_train" = train_hyper_index, 
      "idx_valid" = valid_hyper_index
    )
  }
  
  return(idx_list_list)
}
```



### n_sample.fd

**Description:**
Extracts the number of samples (replications) from a functional data object (`fd` class from the `fda` package). This implementation robustly checks the dimensions of the coefficient matrix.

**Usage:**

```r
n_sample.fd(fd_obj)

```

**Arguments:**

- `fd_obj`: An object of class `fd`.

**Value:**

- Integer. The number of samples (curves) in the object.

```{r}
#' Get Number of Samples from an fd Object
#'
#' Extracts the number of observations (replications) stored in a functional data object.
#'
#' @param fd_obj An object of class `fd`.
#' @return Integer representing the number of samples.
#' @export
n_sample.fd <- function(fd_obj) {
  if (!inherits(fd_obj, "fd")) {
    stop("Input must be of class 'fd'.")
  }
  # The coefficient matrix has dimensions (nbasis x n_sample)
  return(ncol(fd_obj$coefs))
}
```

 
### split.all

**Description:**
Splits a `predictor_hybrid` object and a corresponding response vector into training and testing sets based on a specified ratio. This function ensures that both the scalar matrix and the list of functional predictors are subsetted consistently.

**Inputs:**

- `W_hybrid`: A `predictor_hybrid` object containing the covariates.
- `response`: A numeric vector of response values.
- `train_ratio`: A numeric scalar (0 < ratio < 1) determining the size of the training set.

**Output:**

- A list containing:
  - `predictor_train`: The `predictor_hybrid` object for training.
  - `predictor_test`: The `predictor_hybrid` object for testing.
  - `response_train`: The response vector for training.
  - `response_test`: The response vector for testing.


```{r}
#' Split Hybrid Predictor and Response Data
#'
#' Randomly partitions the hybrid predictor object and response vector into 
#' training and testing sets based on a given ratio. Handles any number of 
#' functional predictors.
#'
#' @param W_hybrid A `predictor_hybrid` object containing all functional and scalar data.
#' @param response A numeric vector. The response variable corresponding to the samples in W_hybrid.
#' @param train_ratio A numeric scalar between 0 and 1 indicating the proportion of data to use for training.
#'
#' @return A list containing split train and test sets for predictors and response.
#' @export
split.all <- function(W_hybrid, response, train_ratio) {
  # --- Input Validation ---
  if (!inherits(W_hybrid, "predictor_hybrid")) {
    stop("'W_hybrid' must be a predictor_hybrid object.")
  }
  if (!is.vector(response) && !is.factor(response)) {
    stop("'response' must be a vector.")
  }
  if (length(response) != W_hybrid$n_sample) {
    stop("Response length must match the number of samples in W_hybrid.")
  }
  if (!is.numeric(train_ratio) || train_ratio <= 0 || train_ratio >= 1) {
    stop("'train_ratio' must be a numeric value strictly between 0 and 1.")
  }

  N <- W_hybrid$n_sample
  N_train <- floor(N * train_ratio)

  # Generate random indices
  # set.seed() should be called by the user before this function if reproducibility is needed
  train_idx <- sort(sample(seq_len(N), N_train))
  test_idx  <- sort(setdiff(seq_len(N), train_idx))

  # --- Subset Scalar Predictors ---
  Z_train <- W_hybrid$Z[train_idx, , drop = FALSE]
  Z_test  <- W_hybrid$Z[test_idx,  , drop = FALSE]

  # --- Subset Functional Predictors ---
  # Use lapply to handle any number of functional predictors (K)
  # The '[' operator on an fd object subsets the samples (replicates)
  fun_list_train <- lapply(W_hybrid$functional_list, function(fd_obj) fd_obj[train_idx])
  fun_list_test  <- lapply(W_hybrid$functional_list, function(fd_obj) fd_obj[test_idx])

  # --- Reconstruct Hybrid Objects ---
  # We reuse the original evaluation points
  W_train <- predictor_hybrid(Z = Z_train, functional_list = fun_list_train, eval_point = W_hybrid$eval_point)
  W_test  <- predictor_hybrid(Z = Z_test,  functional_list = fun_list_test,  eval_point = W_hybrid$eval_point)

  return(list(
    predictor_train = W_train,
    predictor_test  = W_test,
    response_train  = response[train_idx],
    response_test   = response[test_idx],
    train_idx       = train_idx, # Useful to return indices for reference
    test_idx        = test_idx
  ))
}
```

## normalization

 The goal is to perform a two-step standardization: first normalizing *within* each data type (functional vs. scalar) to account for unit differences, and second normalizing *between* the two types to balance their variances for the PLS framework.

### curve_normalize

**Description:**
Performs pointwise centering and scalar scaling on a functional data object. It subtracts a mean function and divides by a scaling constant (denominator). This implementation manually broadcasts the mean subtraction to ensure compatibility with `fda` objects where standard `minus.fd` can sometimes struggle with broadcasting single mean functions across multiple samples.

**Usage:**

```r
curve_normalize(functional, mean_functional, deno)

```

**Arguments:**

- `functional`: The `fd` object to be normalized.
- `mean_functional`: An `fd` object representing the mean (centroid) to subtract.
- `deno`: A numeric scalar scaling factor (e.g., total standard deviation).

**Value:**

- A normalized `fd` object.

```{r}
#' Normalize a functional data object
#'
#' Subtracts a mean function and divides by a scalar constant.
#' Manual broadcasting is used to ensure robust subtraction across samples.
#'
#' @param functional An `fd` object to normalize.
#' @param mean_functional An `fd` object representing the mean.
#' @param deno A numeric scalar for scaling (division).
#'
#' @return A normalized `fd` object.
#' @export
curve_normalize <- function(functional, mean_functional, deno) {
  # Replicate the mean coefficients to match the number of samples in 'functional'
  # This creates a matrix of identical mean columns for broadcasting
  mean_coefs_matrix <- coef(mean_functional) %*% matrix(1, ncol = ncol(coef(functional)))
  
  # Subtract mean and create new fd object
  functional_normalized <- fd(
    coef = coef(functional) - mean_coefs_matrix,
    basisobj = functional$basis
  )
  
  # Apply scaling factor
  # times.fd usually handles scalar multiplication well
  functional_normalized <- times.fd(1 / deno, functional_normalized)
  
  return(functional_normalized)
}
```



### curve_normalize_train_test

**Description:**
Standardizes the *functional* components of hybrid predictors. It centers them to have mean zero and scales them to have unit integrated variance. Crucially, the mean and standard deviation are derived **only from the training data** to prevent data leakage. These training statistics are then applied to normalize the test set.

**Usage:**

```r
curve_normalize_train_test(train, test)

```

**Arguments:**

- `train`: A `predictor_hybrid` object (training set).
- `test`: A `predictor_hybrid` object (test set).

**Value:**

- A list containing the normalized training and testing objects, along with the scaling factors used.

```{r}
#' Normalize Functional Predictors (Train/Test Split)
#'
#' Standardizes functional predictors to have mean zero and unit integrated variance.
#' Statistics (mean and SD) are computed from the training set and applied to the test set.
#'
#' @param train A `predictor_hybrid` object representing the training set.
#' @param test A `predictor_hybrid` object representing the testing set.
#'
#' @return A list containing:
#'   \item{predictor_train}{The normalized training object.}
#'   \item{predictor_test}{The normalized testing object.}
#'   \item{mean_train}{List of mean functions used for centering.}
#'   \item{deno_train}{Vector of scaling factors used.}
#' @export
curve_normalize_train_test <- function(train, test) {
  stopifnot(
    inherits(train, "predictor_hybrid"),
    inherits(test, "predictor_hybrid"),
    train$n_functional == test$n_functional
  )

  train_normalized <- train
  test_normalized <- test
  deno_train <- numeric(train$n_functional)
  mean_train <- list()

  # Iterate through each functional predictor
  for (k in seq_len(train$n_functional)) {
    # 1. Compute Statistics from TRAINING data
    train_fd <- train$functional_list[[k]]
    
    mean_train[[k]] <- fda::mean.fd(train_fd)
    sd_train <- fda::sd.fd(train_fd)
    
    # Scaling factor is the L2 norm of the standard deviation function
    deno_train[k] <- sqrt(fda::inprod(sd_train, sd_train))

    # Safety check for zero variance
    if (deno_train[k] <= 1e-10) {
      warning(paste("Functional predictor", k, "has near-zero variance. Skipping scaling."))
      deno_train[k] <- 1 
    }

    # 2. Normalize TRAINING set
    train_normalized$functional_list[[k]] <- curve_normalize(
      train_fd, 
      mean_train[[k]], 
      deno_train[k]
    )

    # 3. Normalize TEST set using TRAIN stats
    test_normalized$functional_list[[k]] <- curve_normalize(
      test$functional_list[[k]], 
      mean_train[[k]], 
      deno_train[k]
    )
  }

  return(list(
    predictor_train = train_normalized,
    predictor_test = test_normalized,
    mean_train = mean_train,
    deno_train = deno_train
  ))
}
```



### scalar_normalize

**Description:**
Helper function to normalize a scalar matrix. It subtracts a mean vector and divides by a standard deviation vector.

**Usage:**

```r
scalar_normalize(scalar_predictor, mean, deno)

```

**Arguments:**

- `scalar_predictor`: A numeric matrix ().
- `mean`: A numeric vector of length  (means).
- `deno`: A numeric vector of length  (standard deviations).

**Value:**

- A normalized numeric matrix.

```{r}
#' Normalize a scalar predictor matrix
#'
#' Centers columns by 'mean' and scales them by 'deno'.
#'
#' @param scalar_predictor Numeric matrix.
#' @param mean Numeric vector of column means.
#' @param deno Numeric vector of column standard deviations.
#' @return Normalized matrix.
#' @export
scalar_normalize <- function(scalar_predictor, mean, deno) {
  # Subtract mean from each row (broadcasted)
  # Uses the helper subtr_broadcast function defined previously
  scalar_predictor_normalized <- subtr_broadcast(scalar_predictor, mean)
  
  # Create a matrix of denominators matching the dimensions of the predictor
  deno_mat <- matrix(rep(deno, each = nrow(scalar_predictor)), 
                     nrow = nrow(scalar_predictor), 
                     ncol = length(deno))
  
  # Element-wise division
  scalar_predictor_normalized <- scalar_predictor_normalized / deno_mat
  return(scalar_predictor_normalized)
}
```



### scalar_normalize_train_test

**Description:**
Standardizes the *scalar* components () of the hybrid predictors. It ensures each scalar covariate has mean zero and unit variance. As with the functional part, statistics are derived solely from the training set.

**Usage:**

```r
scalar_normalize_train_test(predictor_train, predictor_test)

```

**Arguments:**

- `predictor_train`: A `predictor_hybrid` object (train set).
- `predictor_test`: A `predictor_hybrid` object (test set).

**Value:**

- A list containing the normalized hybrid objects and the statistics used.

```{r}
#' Normalize Scalar Predictors (Train/Test Split)
#'
#' Standardizes scalar predictors (Z) to have mean zero and unit variance.
#' Statistics are computed from the training set.
#'
#' @param predictor_train A `predictor_hybrid` object (train).
#' @param predictor_test A `predictor_hybrid` object (test).
#'
#' @return A list containing normalized objects and statistics.
#' @export
scalar_normalize_train_test <- function(predictor_train, predictor_test) {
  stopifnot(
    inherits(predictor_train, "predictor_hybrid"),
    inherits(predictor_test, "predictor_hybrid"),
    predictor_train$n_scalar == predictor_test$n_scalar
  )

  predictor_train_normalized <- predictor_train
  predictor_test_normalized <- predictor_test

  # 1. Compute Statistics from TRAINING data
  mean_train <- colMeans(predictor_train$Z)
  sd_train <- apply(predictor_train$Z, 2, sd)
  
  # Handle zero variance columns
  sd_train[sd_train == 0] <- 1

  # 2. Normalize TRAINING set
  predictor_train_normalized$Z <- scalar_normalize(
    predictor_train$Z,
    mean_train,
    sd_train
  )

  # 3. Normalize TEST set using TRAIN stats
  predictor_test_normalized$Z <- scalar_normalize(
    predictor_test$Z,
    mean_train,
    sd_train
  )

  return(list(
    predictor_train = predictor_train_normalized,
    predictor_test = predictor_test_normalized,
    mean_train = mean_train,
    sd_train = sd_train
  ))
}
```



### btwn_normalize_train_test

**Description:**
Performs the second step of standardization: balancing the variance *between* functional and scalar predictors. It scales the scalar component  by a factor  so that the total variance of the scalar part matches the total variance of the functional parts.

The weight  is calculated as:



where the numerator is the sum of squared  norms of all functional predictors, and the denominator is the sum of squared Euclidean norms of the scalar predictors (calculated on the training set).

**Usage:**

```r
btwn_normalize_train_test(train, test)

```

**Arguments:**

- `train`: A `predictor_hybrid` object (train set).
- `test`: A `predictor_hybrid` object (test set).

**Value:**

- A list containing the scaled hybrid objects and the scaling factor .

```{r}
#' Inter-Modality Normalization (Between Functional and Scalar)
#'
#' Scales the scalar predictors (Z) so that their total variability is comparable
#' to the total variability of the functional predictors. This addresses the 
#' scale invariance issue in PLS by weighting the scalar part.
#'
#' @param train A `predictor_hybrid` object (train).
#' @param test A `predictor_hybrid` object (test).
#'
#' @return A list containing normalized objects and the scaling factor.
#' @export
btwn_normalize_train_test <- function(train, test) {
  stopifnot(inherits(train, "predictor_hybrid"), inherits(test, "predictor_hybrid"))

  train_normalized <- train
  test_normalized <- test
  Z_s <- train$Z

  # --- 1. Calculate Numerator (Total Variance of Functional Parts) ---
  omega_numerator <- 0
  for (k in seq_len(train$n_functional)) {
    # Compute inner product matrix <X_i, X_j>
    # The diagonal elements <X_i, X_i> represent the squared L2 norm ||X_i||^2
    functional_inprod_matrix <- fda::inprod(
      train$functional_list[[k]],
      train$functional_list[[k]]
    )
    omega_numerator <- omega_numerator + sum(diag(functional_inprod_matrix))
  }

  # --- 2. Calculate Denominator (Total Variance of Scalar Part) ---
  omega_denominator <- sum(Z_s^2)

  # --- 3. Compute Weight omega ---
  if (omega_denominator == 0) {
    warning("Scalar component has zero variance. Skipping inter-modality scaling.")
    omega <- 1
  } else {
    omega <- omega_numerator / omega_denominator
  }

  # --- 4. Apply Scaling (sqrt(omega)) ---
  # This effectively weights the scalar inner product by omega
  scaling_factor <- sqrt(omega)
  
  train_normalized$Z <- scaling_factor * train$Z
  test_normalized$Z  <- scaling_factor * test$Z

  return(list(
    predictor_train = train_normalized,
    predictor_test = test_normalized,
    scaling_factor = scaling_factor
  ))
}
```



### split_and_normalize.all

**Description:**
A wrapper function that orchestrates the entire data preprocessing pipeline. It performs the following steps in order:

1. **Splitting:** divides predictors and response into training and testing sets.
2. **Within-Normalization (Functional):** Standardizes functional predictors (mean 0, unit integrated var).
3. **Within-Normalization (Scalar):** Standardizes scalar predictors (mean 0, unit var).
4. **Between-Normalization:** Balances variance between functional and scalar components.
5. **Response Normalization:** Standardizes the response variable  (mean 0, unit var).

**Usage:**

```r
split_and_normalize.all(W_hybrid, response, train_ratio)

```

**Arguments:**

- `W_hybrid`: The full `predictor_hybrid` dataset.
- `response`: The full response vector.
- `train_ratio`: Ratio for training data split.

**Value:**

- A comprehensive list containing processed training/testing sets for predictors and response, along with all normalization statistics.

```{r}
#' Split and Preprocess Hybrid Data
#'
#' Executes the full preprocessing pipeline: splitting data, standardizing within
#' modalities (functional/scalar), balancing variance between modalities, and 
#' standardizing the response.
#'
#' @param W_hybrid The full `predictor_hybrid` object.
#' @param response The numeric response vector.
#' @param train_ratio Numeric scalar (0-1) for train/test split.
#'
#' @return A list containing processed datasets and normalization parameters.
#' @export
split_and_normalize.all <- function(W_hybrid, response, train_ratio) {
  
  # 1. Split Data
  # Note: Requires the previously defined split.all function
  split_result <- split.all(W_hybrid, response, train_ratio)

  # 2. Normalize Functional Predictors (Within)
  curve_norm <- curve_normalize_train_test(
    split_result$predictor_train, 
    split_result$predictor_test
  )
  
  # 3. Normalize Scalar Predictors (Within)
  scalar_norm <- scalar_normalize_train_test(
    curve_norm$predictor_train, 
    curve_norm$predictor_test
  )
  
  # 4. Normalize Between Modalities (Balance Variances)
  btwn_norm <- btwn_normalize_train_test(
    scalar_norm$predictor_train,
    scalar_norm$predictor_test
  )
  
  # 5. Normalize Response Variable
  response_mean_train <- mean(split_result$response_train)
  response_sd_train   <- sd(split_result$response_train)
  
  # Prevent division by zero if response is constant
  if (response_sd_train == 0) response_sd_train <- 1
  
  response_train_std <- (split_result$response_train - response_mean_train) / response_sd_train
  response_test_std  <- (split_result$response_test  - response_mean_train) / response_sd_train
  
  response_norm <- list(mean_train = response_mean_train, sd_train = response_sd_train)

  # Return comprehensive results
  return(list(
    predictor_train = btwn_norm$predictor_train,
    predictor_test  = btwn_norm$predictor_test,
    response_train  = response_train_std,
    response_test   = response_test_std,
    
    # Store intermediate results and statistics for reference/reconstruction
    details = list(
      curve_normalize_result  = curve_norm,
      scalar_normalize_result = scalar_norm,
      btwn_normalize_result   = btwn_norm,
      response_normalize_result = response_norm,
      split_indices = list(train = split_result$train_idx, test = split_result$test_idx)
    )
  ))
}
```



## Baseline methods

### fit_hybrid_pcr_iterative

**Description:**
This function implements a **Hybrid Principal Component Regression (PCR)** algorithm designed to handle high-dimensional data containing both scalar vectors and functional curves. The core strategy is **dimensionality reduction via PCA** applied separately to each data modality, followed by a linear regression on the resulting scores.

#### 1. Dimensionality Reduction
The function decouples the dimensionality reduction step for scalar and functional predictors:

* **Scalar Predictors ($\mathbf{Z}$):** Standard PCA is applied to the training matrix $\mathbf{Z}_{train}$. The data is centered and scaled. Test data $\mathbf{Z}_{test}$ is projected onto the rotation matrix derived from the training set.
* **Functional Predictors ($\mathbf{X}(t)$):** Functional PCA (FPCA) is applied to each functional variable.
    * **Training:** We decompose the training functions into a mean function $\mu(t)$ and a set of orthogonal eigenfunctions (harmonics) $\phi_k(t)$:
        $$X_{i}(t) \approx \mu(t) + \sum_{k=1}^{K} \xi_{ik} \phi_k(t)$$
    * **Testing (Robust Centering):** A critical step in this function is the robust projection of test data. We explicitly subtract the **training mean** $\mu_{train}(t)$ from the raw test curves before computing inner products with the training eigenfunctions. This ensures the test scores are strictly comparable to the training scores:
        $$\xi_{test, k} = \int \left( X_{test}(t) - \mu_{train}(t) \right) \phi_{k, train}(t) \, dt$$

#### 2. Iterative Model Fitting
Instead of selecting a single fixed number of components, the function iterates through a range of model complexities ($l = 1, \dots, \text{n\_comp\_max}$).

At iteration $l$, the regression model is formulated as:
$$Y = \beta_0 + \sum_{j=1}^{\min(l, \text{rank}(Z))} \alpha_j \text{Score}_{Z,j} + \sum_{p=1}^{P} \sum_{k=1}^{l} \gamma_{p,k} \text{Score}_{X^{(p)}, k} + \epsilon$$

This allows us to observe the full trajectory of the Root Mean Squared Error (RMSE) as the model complexity increases, facilitating the selection of the optimal number of components.

```{r fit_hybrid_pcr_iterative}
#' Iterative Hybrid Principal Component Regression
#'
#' @description
#' Fits a Principal Component Regression (PCR) model that integrates both scalar and 
#' functional predictors. The function performs dimensionality reduction separately 
#' for each modality and iteratively fits linear models with an increasing number 
#' of principal components.
#'
#' @details
#' The workflow consists of three main stages:
#' \enumerate{
#'   \item \strong{Scalar PCA:} Performs standard PCA on the scalar matrix \code{Z}. 
#'         Test data is projected onto the training rotation matrix.
#'   \item \strong{Functional PCA:} Performs FPCA on each functional predictor using 
#'         the \code{fda} package. Crucially, test curves are centered using the 
#'         \emph{training mean function} before projection onto training harmonics 
#'         to prevent data leakage.
#'   \item \strong{Iterative Regression:} Fits a series of linear models (\code{lm}). 
#'         Model \code{l} includes the first \code{l} principal components from 
#'         both the scalar and functional sets.
#' }
#'
#' @param W_train A \code{predictor_hybrid} object containing training data.
#' @param y_train A numeric vector of training response values.
#' @param W_test A \code{predictor_hybrid} object containing test data.
#' @param y_test A numeric vector of test response values.
#' @param n_comp_max Integer. The maximum number of principal components to include 
#'        in the regression models. Defaults to 10.
#'
#' @return A list containing:
#' \item{validation_rmse}{A numeric vector of length \code{n_comp_max} containing 
#' the RMSE on the test set for each model complexity level.}
#'
#' @importFrom stats prcomp predict lm
#' @importFrom fda pca.fd fd inprod
#' @export
fit_hybrid_pcr_iterative <- function(W_train, y_train, W_test, y_test, n_comp_max = 10) {
  
  validation_rmse <- numeric(n_comp_max)
  
  # 1. Scalar PCA (Train)
  # Computes rotation matrix on training data only
  k_z_max <- min(n_comp_max, ncol(W_train$Z))
  pca_z <- prcomp(W_train$Z, center = TRUE, scale. = TRUE)
  
  # Extract training scores and project test data onto training rotation
  all_z_scores_train <- pca_z$x[, 1:k_z_max, drop = FALSE]
  all_z_scores_test  <- predict(pca_z, newdata = W_test$Z)[, 1:k_z_max, drop = FALSE]
  
  # 2. Functional PCA (Train)
  n_funcs <- length(W_train$functional_list)
  all_f_scores_train_list <- list()
  all_f_scores_test_list  <- list()
  
  for(i in 1:n_funcs) {
    # Fit FPCA on Training Data to get harmonics and mean
    pca_fd <- fda::pca.fd(W_train$functional_list[[i]], nharm = n_comp_max)
    all_f_scores_train_list[[i]] <- pca_fd$scores
    
    # Project Test Data (Robust Manual Centering)
    mean_fd <- pca_fd$meanfd
    harmonics <- pca_fd$harmonics
    
    # Extract test coefficients and training mean coefficients
    coefs_test <- W_test$functional_list[[i]]$coefs
    coefs_mean <- as.vector(mean_fd$coefs)
    
    # Sweep subtract: Test_Centered = Test_Raw - Mean_Train
    coefs_centered <- sweep(coefs_test, 1, coefs_mean, "-")
    centered_test  <- fd(coefs_centered, W_test$functional_list[[i]]$basis)
    
    # Project centered test data onto training harmonics
    all_f_scores_test_list[[i]] <- fda::inprod(centered_test, harmonics)
  }
  
  # 3. Iterative Regression Loop
  for (l in 1:n_comp_max) {
    # Scalar Scores Subset
    k_curr <- min(l, k_z_max)
    z_train_curr <- all_z_scores_train[, 1:k_curr, drop=FALSE]
    z_test_curr  <- all_z_scores_test[, 1:k_curr, drop=FALSE]
    
    # Functional Scores Subset
    f_train_curr_list <- list()
    f_test_curr_list  <- list()
    for(i in 1:n_funcs) {
      f_train_curr_list[[i]] <- all_f_scores_train_list[[i]][, 1:l, drop=FALSE]
      f_test_curr_list[[i]]  <- all_f_scores_test_list[[i]][, 1:l, drop=FALSE]
    }
    
    # Construct Design Matrices
    df_train <- data.frame(z_train_curr, do.call(cbind, f_train_curr_list))
    df_test  <- data.frame(z_test_curr,  do.call(cbind, f_test_curr_list))
    
    # Fit Linear Model
    df_train$Y <- y_train
    model <- lm(Y ~ ., data = df_train)
    
    # Predict and Compute RMSE
    y_pred <- predict(model, newdata = df_test)
    validation_rmse[l] <- sqrt(mean((y_test - y_pred)^2))
  }
  
  return(list(validation_rmse = validation_rmse))
}
```

### fit_pfr

**Description:**
The `fit_pfr` function serves as a wrapper for fitting a Penalized Functional Regression (PFR) model (using the `refund` package in R) within a simulation or cross-validation pipeline. It is designed to handle a specific data structure where predictors are split into scalar matrices and functional data objects.

**Key Implementation Details:**

* **Scalar Predictor Unrolling:** A common issue when using `pfr()` or `gam()` is that passing a matrix column (e.g., `df$Z`) can sometimes trigger "length mismatch" errors during prediction. This function addresses this by converting the scalar matrix `Z` into individual columns (`Z1`, `Z2`, etc.) within the data frame.

* **Functional Data Evaluation:** The function assumes inputs are `fd` objects (from the `fda` package). It evaluates these functions at specified time points (`eval_pts`) to create a dense matrix representation required by the `lf()` (linear functional) term in `pfr`.

* **Dynamic Formula Construction:** Since the number of scalar predictors may vary, the regression formula is constructed dynamically as a string before being passed to `pfr`.

* **FPCA Smoothing:** The term `lf(..., presmooth = 'fpca.sc')` indicates that the functional predictors are pre-smoothed using Functional Principal Component Analysis (FPCA). This allows the model to handle noisy or irregular functional data effectively by regressing on the principal component scores.
 

```{r}
#' Fit Penalized Functional Regression (PFR)
#'
#' This function formats training and testing data, fits a PFR model using the `refund` package,
#' and evaluates predictive performance via RMSE. It explicitly handles the "unrolling" of
#' scalar matrix predictors to avoid common dimension errors in `gam`/`pfr`.
#'
#' @param W_train A list containing training predictors:
#'   \itemize{
#'     \item \code{Z}: Matrix of scalar predictors.
#'     \item \code{functional_list}: List of `fd` objects (functional predictors).
#'     \item \code{eval_point}: Vector of evaluation time points.
#'   }
#' @param y_train Vector of scalar response values for training.
#' @param W_test A list containing testing predictors (same structure as \code{W_train}).
#' @param y_test Vector of scalar response values for testing (used for RMSE calculation).
#'
#' @return A numeric value representing the Root Mean Squared Error (RMSE) on the test set.
#'         Returns \code{NA} if the model fit fails.
#' @export
fit_pfr <- function(W_train, y_train, W_test, y_test) {
  
  # Extract common evaluation points for the functional curves
  eval_pts <- W_train$eval_point
  
  # ------------------------------------------------------------------
  # 1. Prepare Scalar Predictors (Unrolling)
  # ------------------------------------------------------------------
  # Convert the scalar matrix Z into a data frame with explicit column names 
  # (Z1, Z2, ...). This "unrolling" is critical because `pfr`/`gam` can 
  # throw "variable length differs" errors if predictors are stored as a 
  # single matrix column inside the data frame during prediction.
  Z_train_df <- as.data.frame(W_train$Z)
  colnames(Z_train_df) <- paste0("Z", 1:ncol(Z_train_df))
  
  Z_test_df  <- as.data.frame(W_test$Z)
  colnames(Z_test_df) <- paste0("Z", 1:ncol(Z_test_df))
  
  # ------------------------------------------------------------------
  # 2. Construct Data Frames for Model Fitting
  # ------------------------------------------------------------------
  # Combine response, unrolled scalars, and evaluated functional matrices.
  
  # Training Data
  df_train <- cbind(response = y_train, Z_train_df)
  
  # Evaluate functional objects (fd) at discrete points to create predictor matrices.
  # t() is used because eval.fd returns (time x subjects), but pfr expects (subjects x time).
  df_train$F1 <- t(eval.fd(eval_pts, W_train$functional_list[[1]])) 
  df_train$F2 <- t(eval.fd(eval_pts, W_train$functional_list[[2]]))
  
  # Testing Data
  df_test <- cbind(response = y_test, Z_test_df)
  df_test$F1 <- t(eval.fd(eval_pts, W_test$functional_list[[1]]))
  df_test$F2 <- t(eval.fd(eval_pts, W_test$functional_list[[2]]))
  
  # ------------------------------------------------------------------
  # 3. Dynamically Build the Formula
  # ------------------------------------------------------------------
  # Create the scalar part of the formula: "Z1 + Z2 + ... + Zp"
  scalar_formula_part <- paste(colnames(Z_train_df), collapse = " + ")
  
  # Construct the full formula string.
  # lf(): Defines a linear functional term.
  # presmooth = 'fpca.sc': Applies FPCA to smooth functions and reduce dimensionality 
  # prior to regression, which is robust for noisy data.
  f_str <- paste0(
    "response ~ ", scalar_formula_part, " + ",
    "lf(F1, argvals = eval_pts, presmooth = 'fpca.sc') + ",
    "lf(F2, argvals = eval_pts, presmooth = 'fpca.sc')"
  )
  
  # ------------------------------------------------------------------
  # 4. Fit Model and Predict
  # ------------------------------------------------------------------
  tryCatch({
    # Fit the PFR model.
    # method = "GCV.Cp": Uses Generalized Cross-Validation for smoothing parameter selection.
    # gamma = 1.2: Inflation factor for GCV to prevent overfitting (smoother results).
    fit <- pfr(as.formula(f_str), data = df_train, method = "GCV.Cp", gamma = 1.2)
    
    # Predict on test data
    pred <- predict(fit, newdata = df_test)
    
    # Calculate RMSE
    rmse <- sqrt(mean((y_test - pred)^2))
    return(rmse)
    
  }, error = function(e) {
    # Graceful error handling prevents the entire simulation loop from crashing
    message("PFR Error: ", e$message)
    return(NA)
  })
}
```

# Kidney Data Preprocessing Pipeline

This section details the transformation of raw renogram data into a structured **Hybrid Predictor** object suitable for the `FSHybridPLS` package. The process involves extracting patient metadata, averaging and transforming response variables, and applying a domain-specific normalization to the functional curves.

* **Mathematical Formulation:** Let $N$ be the number of unique subjects. For the $i$-th subject ($i = 1, \ldots, N$), the data consists of:

    * **Scalar Predictors ($\mathbf{z}$):** We extract 15 scalar covariates (Age + 14 physiological metrics). Let $\mathbf{z}_i \in \mathbb{R}^{15}$ denote the scalar predictor vector for subject $i$.

    * **Response Variable ($y$):** The raw data contains three diagnostic metrics for the response. We first calculate the arithmetic mean of these three indicators:
        $$y_i^{\text{raw}} = \frac{1}{3} \sum_{k=1}^{3} y_{i,k}$$
        and then apply min-max transformation to the range $[0,1]$:
        $$y_i = \frac{y_i^{\text{raw}} - \min(y_i^{\text{raw}})}{\max(y_i^{\text{raw}}) - \min(y_i^{\text{raw}})}$$
      

    * **Functional Predictors ($X$):** Each subject has two distinct time-series curves (Renograms):
        * **Baseline Renogram:** $X_{i}^{(1)}(t)$ observed at $T_1 = 59$ time points.
        * **Post-Furosemide Renogram:** $X_{i}^{(2)}(t)$ observed at $T_2 = 40$ time points.

* **Medical Normalization:** To ensure comparability across patients with varying absolute kidney uptake levels, we normalize both curves relative to the peak of the **baseline** curve. Let $m_i$ be the maximum value of the baseline curve for subject $i$:
    $$m_i = \max_{t} X_{i}^{(1)}(t)$$
    The normalized functions, $\tilde{X}$, are computed as:
    $$\tilde{X}_{i}^{(1)}(t) = \frac{X_{i}^{(1)}(t)}{m_i} \quad \text{and} \quad \tilde{X}_{i}^{(2)}(t) = \frac{X_{i}^{(2)}(t)}{m_i}$$

    > **Note:** The divisor $m_i$ is derived strictly from the *baseline* curve but is applied to *both* curves. This preserves the relative magnitude of the post-furosemide response compared to the baseline peak.

* **Implementation Logic:** The function `load_and_preprocess_kidney_data` performs these mathematical operations using vectorized algebra for efficiency:
    * **Extraction & Alignment:** Filters the dataframe to separate "Baseline" and "Post-Furosemide" entries and reshapes time-series data into wide matrices ($N \times T$).
    * **Response Transformation:** Computes the mean response, scales it to $[0,1]$, applies a safety squeeze (to map $[0,1] \to [\epsilon, 1-\epsilon]$), and finally applies the `qlogis` (logit) function.
    * **Vectorized Normalization:** Computes the scaling factor vector $\mathbf{m} = (m_1, \ldots, m_N)^\top$ and applies it row-wise to the functional data matrices.
    * **Basis Smoothing:** Smooths the discrete points into continuous B-spline functions over the standardized domain $t \in [0,1]$.
    * **Hybrid Object Construction:** Encapsulates components into the `predictor_hybrid` S3 class: $\mathbf{W} = \left\{ \mathbf{Z}, \left( \tilde{X}^{(1)}, \tilde{X}^{(2)} \right) \right\}$.
    
```{r}
#' Load and Preprocess Kidney Data for FSHybridPLS
#'
#' This function processes the raw 'kidney' dataframe into a `predictor_hybrid` object.
#' It performs:
#' 1. Extraction of scalar and functional covariates.
#' 2. Specific medical normalization (scaling by baseline max).
#' 3. Smoothing of functional curves into B-spline basis objects.
#' 4. Transformation of Response: Min-Max scaling followed by Logit transformation.
#' 5. Construction of the hybrid predictor object.
#'
#' @param kidney_df The raw dataframe containing kidney data (columns: ID, Study, renogram_value, etc.)
#' @param n_basis Integer. Number of B-spline basis functions to use for smoothing (default 20).
#'
#' @return A list containing:
#'   \item{W}{A `predictor_hybrid` object containing the predictors.}
#'   \item{y}{A numeric vector representing the transformed response (logit of min-max scaled mean diagnosis metrics).}
#' @export
load_and_preprocess_kidney_data <- function(kidney_df, n_basis = 20) {
  
  # --- 1. Data Extraction ---
  # Split data by ID to ensure order consistency
  ids <- unique(kidney_df$ID)
  n_sample <- length(ids)
  
  # Helper to extract scalar/response from the first row of each patient's baseline
  base_data_idx <- which(kidney_df$Study == "Baseline")
  patient_meta <- kidney_df[base_data_idx, ]
  patient_meta <- patient_meta[!duplicated(patient_meta$ID), ]
  
  # --- Response Extraction & Transformation ---
  # 1. Raw Mean (Columns 13, 14, 15)
  y_mat <- as.matrix(patient_meta[, c(13, 14, 15)])
  y_raw <- rowMeans(y_mat, na.rm = TRUE)
  
  # 2. Min-Max Scaling to [0, 1]
  y_min <- min(y_raw, na.rm = TRUE)
  y_max <- max(y_raw, na.rm = TRUE)
  # Prevent division by zero if all y are identical
  if (y_max == y_min) {
    warning("Response variable has zero variance. Skipping scaling/logit.")
    y <- y_raw
  } else {
    y_scaled <- (y_raw - y_min) / (y_max - y_min)
    
    # 3. Safety Squeeze (avoid Inf/-Inf at boundaries)
    # Maps [0, 1] -> [epsilon, 1-epsilon]
    epsilon <- 1e-5
    y_safe <- y_scaled * (1 - 2 * epsilon) + epsilon
    
    # 4. Logit Transformation: log(p / (1-p))
    #y <- qlogis(y_safe)
    y <- y_scaled
    # <- y_raw
  }
  
  # --- Scalar Predictors (Z) ---
  # Columns: 12 (Age) + 16:29
  Z <- as.matrix(patient_meta[, c(12, 16:29)])
  colnames(Z) <- c("Age", colnames(patient_meta)[16:29])
  
  # --- Functional Data Extraction ---
  # Filter and sort
  df_base <- kidney_df[kidney_df$Study == "Baseline", ]
  df_post <- kidney_df[kidney_df$Study != "Baseline", ]
  
  # Reshape to (ID x Time) matrices
  reno_base_mat <- matrix(df_base$renogram_value, nrow = n_sample, byrow = TRUE)
  reno_post_mat <- matrix(df_post$renogram_value, nrow = n_sample, byrow = TRUE)
  
  # --- 2. Medical Preprocessing (Normalization) ---
  # Calculate max of baseline for each patient
  max_base <- apply(reno_base_mat, 1, max)
  max_base[max_base == 0] <- 1 
  
  # Scale matrices
  reno_base_norm <- reno_base_mat / max_base
  reno_post_norm <- reno_post_mat / max_base
  
  # --- 3. Smoothing (Convert to fd objects) ---
  # Define time grids normalized to [0,1]
  t_base <- seq(0, 1, length.out = ncol(reno_base_norm))
  t_post <- seq(0, 1, length.out = ncol(reno_post_norm))
  
  # Create Basis (B-spline)
  basis_base <- create.bspline.basis(rangeval = c(0, 1), nbasis = n_basis)
  basis_post <- create.bspline.basis(rangeval = c(0, 1), nbasis = n_basis)
  
  # Smooth (Transpose: Time x Samples)
  fd_base <- Data2fd(t_base, t(reno_base_norm), basis_base)
  fd_post <- Data2fd(t_post, t(reno_post_norm), basis_post)
  
  # Assign Names
  fd_base$fdnames <- list("Time", "Patient", "Baseline Renogram")
  fd_post$fdnames <- list("Time", "Patient", "Post-Furosemide Renogram")
  
  # --- 4. Construct Hybrid Predictor ---
  common_eval <- seq(0, 1, length.out = 100)
  
  W <- predictor_hybrid(
    Z = Z,
    functional_list = list(fd_base, fd_post),
    eval_point = common_eval
  )
  
  return(list(W = W, y = y))
}
```

# Numerical Studies

This repository contains R scripts to replicate the numerical studies presented in the paper. All scripts are located in the `numerical_studies` directory.

### 1. `6_1_geometric_validation.R`
Validates the geometric properties of the hybrid space (orthonormality, weighted norms).
```bash
Rscript numerical_studies/6_1_geometric_validation.R [RepID]
```

### 2. `6_2_beta_estimation.R`
Estimates the $\beta$ coefficient function for a single hyperparameter pair.
```bash
Rscript numerical_studies/6_2_beta_estimation.R [RepID] [N] [Lam1] [Lam2]
```

### 3. `6_3_1_scenario_1.R`
Runs the simulation for **Scenario 1:** Orthogonal Nuisance Variance.
```bash
Rscript numerical_studies/6_3_1_scenario_1.R [RepID]
```

### 4. `6_3_2_scenario_2.R`
Runs the simulation for **Scenario 2:** Function-Driven Intermodal Correlation.
```bash
Rscript numerical_studies/6_3_2_scenario_2.R [RepID]
```

### 5. `6_4_kidney_single_rep.R`
Runs the comparative analysis on the kidney dataset (HybridPLS vs. OLS, PCR, PFR).
*Note: Requires `renogram_data.csv` in the `../data/` directory.*
```bash
Rscript numerical_studies/6_4_kidney_single_rep.R [Lam1] [Lam2] [RepID]
```

 
 



