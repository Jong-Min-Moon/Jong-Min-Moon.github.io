---
layout: post
title: "Fundamentals of Neural Recording"
date: 2021-09-06
description: "Non-invasive, invasive, intracellular, extracellular, and single-unit recording methods"
project: neural-probe-integration
categories: research, computational-neuroscience
math: true
---
## 1. Non-invasive vs. Invasive Recording Methods

| Feature | Non-invasive Methods | Invasive Methods |
| :--- | :--- | :--- |
| **Examples** | fMRI, EEG, MEG | Intracellular / Extracellular Recording |
| **Sensor Location** | **Outside the skull** (Scalp) | **Inside the skull** (Intracranial) |
| **Primary Subjects** | Can be humans | Usually animals (Rodents, Primates) |
| **Analogy** | **The Concert Hall**<br>The singer hears the *general atmosphere* (roar of the crowd) but cannot distinguish individuals. | **The Interview**<br>The interviewer holds a microphone to a *specific person* to hear exactly what they say. |
| **Resolution** | **Aggregated Signal**<br>Reads a large pool of neurons; cannot isolate single units. | **Single Unit**<br>Can isolate and record from individual neurons. |
 

---

## 2. Types of Invasive Recording: Intracellular vs. Extracellular

Invasive recordings are further categorized by where the electrode is placed relative to the cell membrane.

| Feature | Intracellular | **Extracellular** |
| :--- | :--- | :--- |
| **Placement** | Electrode inserted **inside** the cell | Electrode placed **outside/near** the cell |
| **Signal** | Very clear, high fidelity | Detects signals from **multiple (a few)** nearby cells |
| **Disadvantages** | High risk of cell damage<br>Signal varies by technique/location<br>Difficult in moving animals | Signal requires processing (**Spike Sorting**) due to aggregation |
| **Advantages** | Precise potential measurement | **Robust** to movement/technique<br>Applicable to **awake behaving animals** |

> **Note:** When we say "Single Unit Recording," we generally refer to **Invasive, Extracellular** recording.

---

## 3. Signal Characteristics & Processing

The raw signal obtained from extracellular recording contains different frequency bands:

* **LFP (Local Field Potential):** 0.1 ~ 300 Hz (Low frequency, synaptic potentials).
* **Spiking Activity (MUA/SUA):** 300 ~ 3,000 Hz (High frequency, action potentials).

### Characteristics of Extracellular Single Unit (SU) Signals
Because the signal is measured from outside the cell, it has four distinct characteristics: **"Flipped, Noisy, Weak, Aggregated."**

1.  **Flipped:** Since the electrode is outside, the action potential appears as a **negative deflection** (convex down). You must look for "dips" rather than peaks.
2.  **Noisy:** Contains significant background electrical noise.
3.  **Weak:** The signal amplitude is very low.
    * $\rightarrow$ Requires **Filtering**.
4.  **Aggregated:** A single electrode picks up spikes from multiple neighboring neurons.
    * $\rightarrow$ Requires **Spike Sorting**.

---

## 4. Spike Sorting

The process of separating the activity of individual neurons from the aggregated signal.

### Step 1: Spike Detection
* Identify waveforms that are significantly larger than the background noise.
* **Threshold:** Usually set to **3x or 4x the Standard Deviation (SD)** of the noise.

### Step 2: Sorting / Clustering
* Group the detected waveforms based on their shape to assign them to specific neurons.
* **Technique:** Dimensionality reduction (e.g., **PCA**) followed by clustering.
* **Features:** Amplitude, width, and waveform shape are key discriminators.

---

## 5. Visualization: Raster Plot

The standard method for visualizing spike timing data.

* **Structure:**
    * **X-axis:** Time.
    * **Y-axis:** Trial number.
    * **Dots:** Occurrence of a spike.
* **Interpretation:**
    * **Annotations:** Stimulus onset or behavioral events are usually marked at the top.
    * **Vertical Patterns:** Reveal **consistency** across trials (Do spikes align at the same time relative to the stimulus?).
    * **Horizontal Patterns:** Reveal **temporal patterns** (Is the neuron bursting? Is it tonic?).

---

### Reference
* **LFP and Recording Video:** [YouTube Link](https://www.youtube.com/watch?v=LyBPd53cSPI)