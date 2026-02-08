---
layout: post
title: "Data Analysis Detail: Subsequent analysis for biological interpretation"
date: 2023-12-15
description: "Identifying key brain regions with sex-specific alterations."
project: autism-sex-differences
categories: research computational-neuroscience paper-details real-data-analysis
---

# subsequent analysis

They’re studying **how sex (male/female)** and **disease state (e.g., ASD vs. control)** interact to affect brain function.  
They already have a *t-statistic map* — think of it as a brain-wide image showing where this interaction is statistically strong (similar to a regression coefficient map).

- Now, we want to **interpret** these interaction effects biologically.
    
- That is, *what brain functions and genes are associated with the regions showing strong interaction effects.*
    

1. **Cognitive decoding** → linking the statistical map to mental functions.
    
2. **Gene enrichment analysis** → linking it to patterns of gene expression in the brain.
    

## Step 1: Cognitive decoding

**Goal:** Identify what kinds of cognitive functions correspond to the pattern of sex-related differences in ASD.

- **Input:** their *t-statistic map* of sex×disease interaction.
    

1-1: correlation to first principal component

1-2: correlation to each cognitive terms

They use public databases that map **brain regions to mental functions** (from many fMRI studies).

- **Tools:**
    
    - **neuromaps toolbox** → compares their map to reference maps.
        
    - **NeuroSynth** → a large meta-analysis database linking words like “memory,” “attention,” “language” to brain activation maps.
        
- **Procedure:**  
    They calculate correlations between their map and “cognition maps” from NeuroSynth.  
    If their map correlates strongly with, say, the “social cognition” map, that suggests the sex×disease effect is most pronounced in brain areas involved in social cognition.
    

So, in statistical terms:

r=corr(t-stat map,cognitive function map)r = \text{corr}(\text{t-stat map}, \text{cognitive function map})r=corr(t-stat map,cognitive function map)

for many different cognitive terms.  
The terms with the highest |r| show which cognitive functions are most related to the observed interaction.

**What they did:**

- They used **NeuroSynth** and **neuromaps** — databases built from thousands of fMRI studies — which provide brain maps for different cognitive functions (like memory, moral reasoning, attention, etc.).
    
- They correlated their **interaction t-map** with the **cognition map** derived from NeuroSynth.
    
    - The correlation was high (*r = 0.771, p = 0.042*), meaning that regions showing sex differences in ASD follow a **sensory-to-association cortex gradient**, sometimes called the *cortical hierarchy*.
        
- Then, they further decoded the map by checking correlations with many **specific cognitive term maps** (e.g., “self-referential,” “theory of mind,” “moral reasoning”).
    
    - The highest correlations were with **higher-order cognitive control functions** — processes related to self-reflection, social understanding, and moral judgment.
        

**Interpretation:**  
The sex differences in ASD appear strongest in brain regions responsible for *internally oriented cognition* (default mode network), not in simple sensory regions.

### **Step 2: Gene enrichment (transcriptomic) analysis**

**Goal:** Identify whether particular **genes** show similar spatial patterns to the interaction map — i.e., whether brain regions with stronger sex-related differences also show higher expression of certain genes.

**What they did:**

- Used **abagen**, which processes microarray gene-expression data from the **Allen Human Brain Atlas** (a set of postmortem human brains).
    
- For each gene, they correlated its expression map (across cortical regions) with their **t-statistic interaction map**.
    
    - Genes whose expression strongly matched the t-map pattern were selected (|r| > threshold, FDR < 0.05).
        
- Then, they used a **developmental enrichment tool (CSEAtool)** to see *where and when* those genes are typically active — for example, which brain cell types or developmental stages show enrichment.
    

**What they found:**

- The correlated genes were most enriched in **cortical, striatal, and thalamic** cells — regions known to play roles in ASD.
    
- Prior studies have shown that ASD involves atypical growth and function in these regions (e.g., striatal overgrowth, reduced thalamic volume).
    
- This suggests that **sex-related differences in ASD connectivity** may arise partly from **sex-dependent genetic expression** in these brain systems.