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




for BCE loss:

I stoped at epoch878.
@epoch873  Train loss: 2934.513720703125 Train AUC: 0.8198394859507676 Train ACC: 0.7467167971953751 Valid loss: 2956.881005859375 Valid AUC: 0.8256095592081545 Valid ACC: 0.7515513026118269 TIME:19.053945302963257
@epoch874  Train loss: 2934.469384765625 Train AUC: 0.8198208490014082 Train ACC: 0.7467167971953754 Valid loss: 2956.99072265625 Valid AUC: 0.8248790864944449 Valid ACC: 0.7515513026118269 TIME:19.07580041885376
@epoch875  Train loss: 2934.55673828125 Train AUC: 0.82030038639158 Train ACC: 0.7467167971953748 Valid loss: 2956.8703125 Valid AUC: 0.824193373084068 Valid ACC: 0.7515513026118269 TIME:19.099503755569458
@epoch876  Train loss: 2934.5728515625 Train AUC: 0.8204617665261027 Train ACC: 0.7467167971953744 Valid loss: 2957.084033203125 Valid AUC: 0.8263562296628955 Valid ACC: 0.7515513026118269 TIME:19.085535049438477
@epoch877  Train loss: 2934.52197265625 Train AUC: 0.8202487465143203 Train ACC: 0.7467167971953744 Valid loss: 2956.86533203125 Valid AUC: 0.825389525651931 Valid ACC: 0.7515513026118269 TIME:19.071943998336792
@epoch878  Train loss: 2934.45283203125 Train AUC: 0.8199612427651873 Train ACC: 0.7467167971953746 Valid loss: 2956.862109375 Valid AUC: 0.825797423988581 Valid ACC: 0.7515513026118269 TIME:19.058160305023193



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