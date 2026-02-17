---
layout: post
title: "Fundamentals of Phase Locking"
date: 2021-11-22
description: "Distinguishing Spike-Field Locking from Inter-Trial Phase Locking"
project: neural-probe-integration
categories: research, statistics
math: true
---

### I. The Core Concept: Consistency of Angles
In neuroscience, *phase locking* mathematically means **consistency of angles**. You collect a sequence of phase angles (0° to 360°) and ask: 
>Are these angles random (uniform), or do they cluster around a specific direction?

However, the term is used in two very different experimental contexts depending on **what** is locking to **what**.



---

### II. Type 1: Spike-Field Phase Locking (Internal Sync)
> "Phase locking refers to the tendency of a neuron to fire action potentials at particular phases of an ongoing periodic sound waveform, such as the sinusoidal waveforms that are typically used in physiological studies of the auditory system"
>
> — *Encyclopedia of Neuroscience, 2009*

- **Synonyms:** Spike-field coherence , spike-phase coupling.
- **What is locking?** A single neuron's firing (spike train).
- **What is it locking to?** An internal brain rhythm (LFP/Theta Wave).
- **The Reference Frame:** The brain's clock (the cycle of the wave itself).
- **The Question:** *"Does this neuron fire in sync with the background beat of the hippocampus?"*

**Mechanism:**
The LFP oscillation acts as a "conductor." When the voltage is at a specific phase (e.g., the trough), the membrane potential of the neuron is pushed closer to threshold, making it more likely to fire.
* **Result:** Spikes cluster at the "preferred phase" of the oscillation.
* **Meaning:** This proves **Network Connectivity**. It confirms the single neuron is physically "plugged in" to the local population dynamics.



---

### III. Type 2: Inter-Trial Phase Locking (External Sync)
> "Activity is phase-locked when its phase is the same or very similar on each trial"
>
> — *Cohen, M. X. Analyzing Neural Time Series Data: Theory and Practice, Chapter 3*

**Context:** EEG/ERP Analysis (Cohen, Chapter 2).
**Synonyms:** Inter-Trial Phase Clustering (ITPC), Phase-Locking Value (PLV).

* **What is locking?** A macroscopic voltage wave (**EEG/LFP**).
* **What is it locking to?** An **External Event** (Stimulus Onset / $t=0$).
* **The Reference Frame:** The Experimenter's Clock.
* **The Question:** *"Does the brain start oscillating with the exact same phase every time I show the picture?"*

**Mechanism:**
This distinction is used to separate **Evoked** from **Induced** activity.
1.  **Phase-Locked (Evoked):** The stimulus "resets" the phase of the oscillation. On Trial 1, 2, and 3, the wave starts with a *peak* at 100ms.
    * *Result:* Creates an **ERP** (Event-Related Potential).
2.  **Non-Phase-Locked (Induced):** The stimulus increases the *power* of the oscillation, but the phase is random. On Trial 1 it's a peak; on Trial 2 it's a trough.
    * *Result:* Invisible in ERPs (cancels out). Visible in Time-Frequency Power.



---

### IV. Comparison: The Musician vs. The Sprinter

The best way to remember the difference is through analogy:

| Feature              | **Type 1: Spike-Field (Internal)**                                                | **Type 2: Inter-Trial (External)**                                           |
| :------------------- | :-------------------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| **The Analogy**      | **The Jazz Musician**                                                             | **The Sprinter**                                                             |
| **Description**      | A drummer who always hits the snare drum exactly on the **3rd beat** of the song. | A runner who always launches exactly **100ms** after the starting gun fires. |
| **Synchronization**  | Syncs to the **Rhythm** (Continuous).                                             | Syncs to the **Trigger** (Discrete).                                         |
| **Data Source**      | Correlation between **Spikes** and **LFP**.                                       | Correlation between **Trial 1**, **Trial 2**, **Trial 3**...                 |
| **Scientific Value** | Validates **Probe Location** and **Network Membership**.                          | Validates **Stimulus Determinism** and **Evoked Potentials**.                |

---

### V. The Mathematical Unity
Despite the conceptual difference, the statistical test used is often identical (The Rayleigh Test).

1.  **Extract Angles:**
    * *Type 1:* Collect the LFP phase angle at every spike timestamp ($\phi_{spike}$).
    * *Type 2:* Collect the EEG phase angle at time $t$ across all trials ($\phi_{trial}$).
2.  **Vector Sum:** Treat each angle as a vector on a unit circle.
3.  **Calculate Length:**
    * If the vector length $\approx 0$, the activity is **Random** (Unlocked).
    * If the vector length $\approx 1$, the activity is **Clustered** (Locked).

> **Summary:**
> * **Spike-Field Locking** tells you about the **Brain's Internal Wiring** (Spike $\leftrightarrow$ Wave).
> * **Inter-Trial Locking** tells you about the **Brain's Reaction to the World** (Stimulus $\leftrightarrow$ Wave).