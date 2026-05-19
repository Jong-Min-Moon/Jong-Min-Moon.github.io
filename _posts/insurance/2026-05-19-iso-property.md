---
layout: distill
title: "ISO property data"
description: " "
tags: distill formatting
categories:  
date: 2026-05-19
featured: false
mermaid:
  enabled: true
  zoomable: true
project: ise-547
authors:
  - name: Jongmin Mun


_styles: >
  .fake-img {
    margin-bottom: 12px;
  }
  .fake-img p {
    text-align: center;
    margin: 12px 0;
  }
---

## Task

Start working to aggregate EARNED_PREMIUM & LOSS_LAE_INCURRED by TOL (type of loss / peril), ZIPCD (zip code) and ST (state).
Look through the rest of the fields. 


## terms

- premium is the amount the insured pays for insurance coverage. 
- Written premium is the total premimum associated with policies that were issued during a specified period.
- Earend premium represents the portion of the written premium for which coverage has laready been provied as of a certian point in time.


- Losses: amount paid or owed to claimants under the provisions of an insurance contract
- loss is amount of compensation, claim is demand for compensation
- LAE: loss adjustment claims. amounts paid by the insurance company to investigate and settle claims
- Losses + LAE takes up most of insurance cost and thus the premium.

- loss ratio: the most common loss ratio metric is reported loss retio, or reported losses divided by earned premium.

### TOL Category Check

How many `TOL` categories are there?  
There are fourteen distinct categories, which means it is feasible to assign one column per TOL if needed (e.g., for pivoting or wide-format analysis).

```sas
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

proc sql;
    select count(distinct TOL) as num_tol_categories
    from iso.iso_prop_20_24
    where EARNED_PREMIUM = 0 and TOL is not missing;
quit;
```
## Plan for loss ratio computation


**Loss Ratio Analysis Plan**

* The dataset is **stacked**:
  * Rows with **nonzero `EARNED_PREMIUM`** do **not** contain `TOL`.
  * Rows with **zero `EARNED_PREMIUM`** contain `TOL` (categorical loss type).

* The data spans **multiple years**, so the first step is to **analyze each year separately**.

* Analysis will be conducted at two **geographic levels**:
  * **State (`ST`)**
  * **ZIP code (`ZIPCD`)**

* The **loss ratio** is defined as:
  $$
  \text{Loss Ratio} = \frac{\sum(\text{LOSS\_LAE\_INCURRED})}{\sum(\text{EARNED\_PREMIUM})}
  $$

* Because `TOL` is **not recorded for premium rows**, it is **not possible to compute loss ratios by TOL directly** (missing denominator).
  * However, we can compute the **distribution of losses by TOL** to understand how each peril contributes to total losses.


### Reporting Structure
- For each year:
  - Perform analysis at two levels of granularity:
    - ZIP code
    - State

- At each level:
  - Compute the overall loss ratio
  - Provide a breakdown of losses by TOL (composition analysis):
    - Create 14 columns, one for each TOL category
    - Each column represents the proportion of total loss attributable to that TOL
    - The proportions across all TOL columns sum to 1 for each group (year × geography)




