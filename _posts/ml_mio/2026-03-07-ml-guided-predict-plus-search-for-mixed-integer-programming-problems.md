---
layout: distill
title: "ML-guided Predict + Search for Mixed-Integer Programming Problems"
description: "A hybrid framework combining machine learning with traditional optimization solvers for MIP problems."
date: 2026-03-07
categories: ml_mio optimization
tags: machine-learning mixed-integer-programming
project: ml_mio
authors:
  - name: Jongmin Mun
    url: "https://github.com/Jong-Min-Moon"
    affiliations:
      name: USC Marshall
toc:
  - name: "Introduction: Predict + Search"
  - name: Homework Objectives
---

If you encounter technical hurdles when doing this part of the hw, you can email me or come to the office hour:

- **Contact**: <caijunya@usc.edu>
- **Office Hour**: 2/18 Wednesday 3-4pm, 2/23 Monday 1:30-2:30pm, 3/6 Friday 2-3pm
- **Zoom link**: [Link](https://usc.zoom.us/j/64785555872?pwd=eFpEdjVmZVBZQXNqclZtQzT2EyM3RSUT09)

## Introduction: Predict + Search

Predict + Search is a hybrid framework that combines machine learning with traditional optimization solvers to tackle challenging mixed-integer programming (MIP) problems. Instead of relying solely on the solver's internal heuristics, a learned model is first used to predict promising values for a subset of decision variables based on structural features of the problem instance. These predictions are then partially enforced or used to guide the search, after which a classical MIP solver completes the optimization over the remaining variables. The key idea is that machine learning can capture recurring patterns across similar problem instances, while exact solvers ensure feasibility and optimality guarantees. In this homework, we apply the Predict + Search paradigm to Maximum Independent Set instances by training a graph neural network on the bipartite constraint–variable graph, and we study how prediction quality—under different loss functions—interacts with downstream MIP solving performance.

## Homework Objectives

This homework uses a **fixed dataset of MIP instances (features) + solution (label) data**. Students will:

1.  **Train a prediction model** on the MIP bipartite graph (constraints–variables) using a Graph Neural Network model to predict the variable values in the solutions of the MIPs.
2.  Compare results when training with **BCE vs Contrastive (InfoNCE) loss**.
3.  **Evaluate ML metrics** in terms of solution prediction.
4.  Run a **solver-based “predict + search”** experiment using the trained model, where a fraction of the MIP variables are assigned to values based on the predictions of the GNN model, and then a MIP solver is used to search for an assignment of the remaining variables.
5.  **Analyze results** in terms of MIP-solving metrics vs ML-accuracy metrics with plots and discussion.


# Local Environment Setup

This section provides instructions for setting up your local environment on **Apple Silicon (M1/M2/M3)**. We recommend using Python 3.10, as it is currently the most stable version for the PyTorch and PyTorch Geometric (PyG) ecosystem.

### 1. Create a Virtual Environment

First, create and activate a new conda environment:

```bash
conda create -n graph_env python=3.10
conda activate graph_env
```

Upgrade the base packaging tools:

```bash
pip install --upgrade pip setuptools wheel
```

### 2. Install PyTorch with MPS Support

To leverage the Apple Silicon GPU, install the specific version of PyTorch:

```bash
pip install torch==2.2.2 torchvision torchaudio
```

You can verify that the GPU (MPS) is available with the following command:

```bash
python - <<EOF
import torch
print("Torch:", torch.__version__)
print("MPS available:", torch.backends.mps.is_available())
EOF
```

**Expected Output:**
```text
Torch: 2.2.2
MPS available: True
```

This confirms the M1 Pro GPU via MPS is usable.

### 3. Install Data Science and Metric Learning Stack

Install the core data science libraries and metric-learning tools:

```bash
pip install numpy pandas scikit-learn matplotlib tqdm networkx
pip install torchmetrics torcheval pytorch-metric-learning
```

### 4. Install PyTorch Geometric (PyG)

Install PyTorch Geometric. Note that while the wheels may indicate CPU, they will still utilize MPS for device placement:

```bash
pip install torch_geometric
```

### 5. Install Additional Utilities and Gurobi

Finally, install utilities for data downloading and the Gurobi optimizer:

```bash
pip install gdown
conda install -c gurobi gurobi
pip install gurobipy
```



## Things to note:
- MPS do not support float64. 
- The operator 'aten::scatter_reduce.two_out' is not currently supported on the MPS backend

- RuntimeError: MPS backend out of memory (MPS allocated: 13.55 GB, other allocations: 3.30 GB, max allowed: 18.13 GB). Tried to allocate 1.37 GB on private pool. Use PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0 to disable upper limit for memory allocations (may cause system failure).


## Second try: USC CARC

salloc --partition=gpu --gres=gpu:1 --cpus-per-task=8 --mem=32GB --time=1:00:00


2. Load a Conda module
Once you have been granted the resources and logged in to a compute node, load the Conda module:

module purge
module load conda

3. Initialize shell to use Conda and Mamba
Modifies your ~/.bashrc file so that Conda and Mamba are ready to use every time you log in (without needing to load the module):

mamba init bash
source ~/.bashrc


Create new Conda environments in one of your available directories. By default, the packages will be installed in your home directory under /home1/<user_name>/.conda/envs/. Conda environments are isolated project environments designed to manage distinct package requirements and dependencies for different projects. We recommend using the mamba command for faster package solving, downloading, and installing. However, you can use the conda command, with various options, to install and inspect Conda environments.

The process for creating and using environments has three basic steps:


Create the environment in your home directory (recommended)

-p specifies the full path instead of default read-only /apps.
```bash
mamba create -p $HOME/conda_envs/graph_env python=3.10
conda activate $HOME/conda_envs/graph_env
```

Check which CUDA version is available on your cluster:
```bash
nvidia-smi
```

(/home1/jongminm/conda_envs/graph_env) [jongminm@d23-16 ~]$ nvidia-smi
Sat Mar  7 15:49:35 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 575.57.08              Driver Version: 575.57.08      CUDA Version: 12.9     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  Tesla P100-PCIE-16GB           On  |   00000000:07:00.0 Off |                    0 |
| N/A   27C    P0             26W /  250W |       0MiB /  16384MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
                                                                                         
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |

mamba install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia


here’s a compact one-liner you can paste directly into your shell to check PyTorch, CUDA, GPU name, and memory usage in one command:

python -c "import torch; print('Torch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('Device name:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'); print('Memory allocated (MB):', torch.cuda.memory_allocated(0)//1024**2 if torch.cuda.is_available() else 'N/A')"

Torch: 2.5.1
CUDA available: True
Device name: Tesla P100-PCIE-16GB
Memory allocated (MB): 0


```bash
mamba install numpy==1.23 pandas scikit-learn matplotlib tqdm networkx
```bash
pip install torch_geometric
```

pip install torchmetrics torcheval pytorch-metric-learning


when using gurobipy: guroby version and gurobypy version should match. if you just run pip install gurobipy blidnly, you might run into the error:

gurobipy._exception.GurobiError: Request denied: license not valid for Gurobi version 13

so first check gurobi version on bash by
```bash
module load gurobi
gurobi_cl --version
```


```bash
pip install gurobipy==12.0.3
```

# GNN Model Training & Results

To evaluate the learning progress of the Graph Neural Network (GNN), we monitor several key performance indicators. Because our model is designed as a **Bernoulli generative model**, it learns the success probabilities for binary outcomes, which we then compare against the true labels (the optimal solutions).

* **Loss Curves:** We track both training and validation loss to detect convergence and identify any potential overfitting or underfitting.
* **Binary Accuracy:** This measures how frequently the learned probabilities correctly predict the true labels. It serves as a direct indicator of how well the generative model matches the optimal solution.
* **AUC (Area Under the Curve):** As a classification metric, AUC evaluates the model’s ability to distinguish between classes across various thresholds. This is particularly useful for validating the success probabilities generated by our Bernoulli model.


## 1. Binary Cross-Entropy (BCE) Loss
BCE loss is the standard approach for binary classification. The following results were recorded at the final epoch (1500):

| Metric       | Training | Validation |
| :----------- | :------- | :--------- |
| **Loss**     | 2934.45  | 2956.86    |
| **AUC**      | 0.820    | 0.826      |
| **Accuracy** | 0.747    | 0.752      |


## 2. Contrastive Loss
At the final epoch (1500), we observe that while the **AUC** remains comparable to the BCE model, the **Loss scale** and **Accuracy** metrics differ significantly. This shift is expected due to the nature of the Contrastive objective function, which prioritizes the relative distance between representations rather than direct label matching.

| Metric       | Training | Validation |
| :----------- | :------- | :--------- |
| **Loss**     | 0.152    | 0.244      |
| **AUC**      | 0.820    | 0.825      |
| **Accuracy** | 0.655    | 0.659      |



# Evaluate MIP solving performance

# Result Summary and Comparison

## Objective Value Statistics (Lower Is Better)

| Statistic | Gurobi   | BCE Model | CL Model |
| --------- | -------- | --------- | -------- |
| Count     | 10       | 10        | 10       |
| Mean      | -2523.60 | -2519.70  | -2520.80 |
| Std Dev   | 15.58    | 15.64     | 13.63    |
| Min       | -2551.00 | -2545.00  | -2541.00 |
| 25th Pctl | -2528.25 | -2528.50  | -2531.00 |
| Median    | -2522.50 | -2517.50  | -2520.50 |
| 75th Pctl | -2514.25 | -2509.50  | -2514.00 |
| Max       | -2499.00 | -2498.00  | -2500.00 |

**Interpretation:**

- Gurobi achieves the best average objective but with slightly higher variability.
- The CL Model performs comparably, with a tighter spread.
- The BCE Model’s solutions are close but slightly worse on average.

---

## Best Primal Bound Counts (Quality; Larger Is Better)
The primal bound represents the best solution found so far. It is the lowest-cost feasible solution the solver has identified up to the current point and reflects the quality of the current answer. If you were to stop the solver right now, this would be the solution you’d use. The results indicate that Gurobi achieved the best primal bound more than the CL model, although the difference is relatively small.

| Method   | Count of Best Primal Bound |
| -------- | -------------------------- |
| Gurobi   | 6                          |
| CL Model | 4                          |

---

## Primal Integral Statistics (Efficiency; Lower Is Better)
The primal integral measures the speed of improvement over time by calculating the area under the objective value curve. A solver that quickly finds high-quality solutions will have a lower (better) primal integral than one that finds similar solutions later in the process. The results show that Gurobi improves relatively slowly, while the CL model achieves the fastest and most consistent improvements.

| Statistic | BCE Model | CL Model | Gurobi |
| --------- | --------- | -------- | ------ |
| Count     | 10        | 10       | 10     |
| Mean      | 5.52      | 4.61     | 19.91  |
| Std Dev   | 1.08      | 1.28     | 2.93   |
| Min       | 4.03      | 2.43     | 13.74  |
| 25th Pctl | 4.86      | 4.14     | 18.46  |
| Median    | 5.31      | 4.59     | 20.44  |
| 75th Pctl | 6.43      | 4.86     | 21.44  |
| Max       | 7.22      | 7.28     | 23.67  |

#### Best Performer by Primal Integral

| Method    | Count of Best Primal Integral |
| --------- | ----------------------------- |
| CL Model  | 8                             |
| BCE Model | 2                             |

**Interpretation:**

- Both ML models (BCE and CL) significantly outperform vanilla Gurobi in terms of primal integral, indicating faster convergence to good feasible solutions.
- The CL model consistently yields the lowest primal integral values in most instances.



## Relation of Training Metrics to Optimization Quality

Here are example training and validation metrics from the two loss functions used to train our models:

### Binary Cross Entropy (BCE) Loss Results:

@epoch1499 Train loss: 2934.45 Train AUC: 0.820 Train ACC: 0.747
Valid loss: 2956.86 Valid AUC: 0.826 Valid ACC: 0.752 TIME: 19.06s


### Contrastive Loss (CL) Results:

@epoch1499 Train loss: 0.152 Train AUC: 0.820 Train ACC: 0.655
Valid loss: 0.244 Valid AUC: 0.825 Valid ACC: 0.659 TIME: 27.28s


### How do these relate to optimization quality?

- **Train/Validation Loss** measures how well the model fits the training data or generalizes to unseen data — lower values indicate better predictive accuracy.
- **AUC (Area Under Curve)** and **Accuracy (ACC)** reflect the quality of binary variable prediction — higher is better.
- The BCE model achieves higher accuracy but has higher loss values (due to the loss scale), while the CL model achieves lower loss but slightly lower accuracy.
- These prediction qualities directly influence the **Predict + Search** framework’s ability to guide the MIP solver: better predictions help the solver focus on promising variable assignments, improving both the primal bound and primal integral.
- But somehow,  the CL model’s lower primal integral suggests that despite slightly lower accuracy, its predictions better guide the solver toward faster solution improvements.
  
# Side notes

## Copying/moving conda environment

Conda does not automatically detect a copied environment, and copying environments can easily break things.

Here’s why.

1️⃣ How Conda tracks environments

Conda keeps metadata about environments in:

conda-meta/ inside the environment

a registry in the base conda installation

Example typical structure:

miniconda3/
 ├── envs/
 │   └── graph_env/
 │       ├── bin/
 │       ├── lib/
 │       └── conda-meta/

When you run:

conda info --envs

Conda lists environments it knows about, usually from:

~/miniconda3/envs/

If you copy an environment somewhere else, Conda may not register it.

2️⃣ What happens if you copy it manually

Example:

cp -r ~/miniconda3/envs/graph_env /project2/.../conda_envs/

Possible issues:

Conda doesn’t list it

Hardcoded paths break

Activation fails

Binary libraries reference old paths

For example, many packages contain absolute paths like:

/home/user/miniconda3/envs/graph_env/...

So moving the environment can break them.

3️⃣ When copying does work

Sometimes it works if:

the path is identical

packages don’t depend on absolute paths

you call python directly

Example:

/project2/.../conda_envs/graph_env/bin/python train.py

This bypasses Conda activation.

4️⃣ Correct way to move an environment
Option A (recommended): export + recreate
conda activate graph_env
conda env export > env.yml

Then recreate:

conda env create -p /project2/.../conda_envs/graph_env -f env.yml
Option B: use conda-pack (best for clusters)

Install:

pip install conda-pack

Pack:

conda pack -n graph_env -o graph_env.tar.gz

Unpack elsewhere:

tar -xzf graph_env.tar.gz

Then fix paths:

./bin/conda-unpack
5️⃣ Best practice for HPC clusters

Most clusters recommend:

$PROJECT/conda_envs/

Create environment directly there:

conda create -p /project2/.../conda_envs/graph_env python=3.10

Then activate:

conda activate /project2/.../conda_envs/graph_env

💡 In your case, since the environment already exists at:

/project2/dilkina_1832/jongmin_hw1/conda_envs/graph_env

try activating with the prefix:

conda activate /project2/dilkina_1832/jongmin_hw1/conda_envs/graph_env

If Conda still says it’s not an environment, it was likely copied and broken, and recreating it is the safest fix.