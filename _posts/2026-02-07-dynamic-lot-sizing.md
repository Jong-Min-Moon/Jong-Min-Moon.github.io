---
layout: post
title: "Dynamic Lot Sizing Problem"
date: 2026-02-07
description: "An introduction to the Dynamic Lot Sizing Problem and its key assumptions."
project: operations-management
categories: operations-research optimization
math: true
---

The **Dynamic Lot Sizing Problem** is a fundamental model in inventory management where a decision-maker must determine the optimal order quantities for a single item over a finite planning horizon.

## Problem Definition

A manager decides how much inventory to order in each period $t$ to satisfy demand while minimizing total costs, which typically include ordering costs and holding costs.

### Key Assumptions

1.  **Single-Item, Single-Level**: We consider only the end product, ignoring raw materials or multi-echelon interactions.
2.  **Finite Planning Horizon**: The decision-making process spans a discrete, finite timeline $t = 1, 2, \dots, T$.
3.  **Known Dynamic Demand**: The demand $d_t$ for each period varies over time (hence "dynamic") but is known in advance for the entire sequence $d_1, \dots, d_T$ (deterministic).
4.  **Periodic Review**: Inventory levels are reviewed, and ordering decisions are made at the beginning of each period.
5.  **Unconstrained Capacity**: There are no limits on the order quantity or inventory storage (infinite warehouse assumption).
6.  **No Backorders**: Demand must be fully met in the period it occurs; shortages are not permitted.

Input variables:
* $d_t$: demand in period $t$
* $c_o$: ordering cost
* $c_h$: holding cost



## Calcium Imaging
given y_1, ..., y_T, want to decide s_1, ..., s_T
and c_1,.. c_T 
c_t: current inventory level.
s_t: order quantity in period t. 
perishable good: c_t = s_t + \gamma c_(t-1)
the holding cost is 1/2(y_t-c_t)^2.
