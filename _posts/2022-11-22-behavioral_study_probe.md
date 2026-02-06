---
layout: post
title: "Fundamentals of Neural Signal Decomposition"

description: "Spikes, LFPs, and frequency bands"

categories: research computational-neuroscience paper-details real-data-analysis
math: true
---





---

### III. Task 1: Active Locomotion Analysis


#### 1. Single-Unit Activity & Behavioral Correlation
The firing rates of individual neurons in both regions showed distinct modulation depending on the specific motor behavior of the mouse.

* **State A: Running (Forward Motion)**
    * **Behavior:** The mouse moves forward along the long arm of the maze.
    * **Neural Response:**
        * **CA1:** Firing rate **increases** significantly (consistent with spatial navigation/place cell activity).
        * **L6:** (Activity profile not specified for this state).

* **State B: Stopping & Orienting**
    * **Behavior:** The mouse stops at the intersection and performs head rotations to scan for a distinct exit path.
    * **Neural Response:**
        * **CA1:** Firing rate **decreases**.
        * **L6:** Firing rate **increases** (consistent with visual scanning/head rotation).



#### 2. Local Field Potential (LFP) Dynamics
* **Observation:** The LFP trace in the CA1 region exhibited significantly **greater fluctuation amplitude** during the **running state** compared to the standstill state.
* **Implication:** This reflects the recruitment of synchronized population activity (theta rhythm) required for locomotion and navigation.

---

### IV. Validation Methodology: Phase-Locking Analysis
To verify that the recorded signals represented genuine neural physiology rather than artifacts or noise, the study performed a **Phase-Locking Analysis (PLA)**.

#### 1. The Rationale
The implanted probes capture a single raw voltage trace that is separated into two components via filtering:
* **LFP (1–300 Hz):** Reflects collective network activity.
* **Spikes (500–3000 Hz):** Reflects individual neuronal output.

Since both signals originate from the same biological source, they should be temporally correlated. If the signals were noise, the spikes would occur randomly relative to the background oscillation.



#### 2. The Mechanism in Context
* **Context:** During active running, the hippocampus generates robust **Theta oscillations (6–10 Hz)**.
* **Analysis:** The phase of the Theta oscillation is extracted (via Hilbert transform) at the exact moment each spike occurs.
* **Criterion:**
    * *Uniform Distribution (0°–360°):* Indicates random firing (No relationship / Potential noise).
    * *Clustered Distribution:* Indicates **Phase Locking**.

#### 3. Finding
The analysis revealed that spikes from CA1 neurons clustered around a **preferred phase** of the LFP theta rhythm. This confirms **significant phase locking**, demonstrating precise temporal coordination between individual neurons and the broader hippocampal network, thereby validating the signal quality of the interface