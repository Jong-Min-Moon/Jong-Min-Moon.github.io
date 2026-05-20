---
layout: distill
title: "ISO Property Data: Loss Ratio Analysis by State and ZIP Code"
description: "Aggregating earned premium and loss+LAE from ISO property data to compute loss ratios and peril compositions across states and ZIP codes."
tags: insurance loss-ratio SAS property
categories: insurance
date: 2026-05-19
featured: false
mermaid:
  enabled: true
  zoomable: true
project: insurance
authors:
  - name: Jongmin Moon


_styles: >
  .fake-img {
    margin-bottom: 12px;
  }
  .fake-img p {
    text-align: center;
    margin: 12px 0;
  }
---

# Data

- zip_mappings_20260116_sm: lookup table to map zip codes to territory variables (bg2_terr and scs_terr)

## ISO DataCube™

* The dataset is **stacked**:
  * Rows with **nonzero `EARNED_PREMIUM`** do **not** contain `TOL` and have zero LOSS_LAE_INCURRED.
  * Rows with **zero `EARNED_PREMIUM`** contain `TOL` (categorical loss type) and have nonzero LOSS_LAE_INCURRED.


### Variables
This information is provided by ISO DataCube™:
Detail and Statistics of verisk  % cite: https://www.verisk.com/4a79d9/siteassets/media/downloads/underwriting/iso-datacube-detail-and-statistics.pdf
- Time: Latest available five calendar/accident
years/quarters
  - YEAR
  - QTR: quarter
- Space
  - State (ST)
  - ZIP code (ZIPCD)
  - ISO rating territories(TERR)
  - BIG_Territory, BGII_Territory, SCL_Territory: Territories for sublines
- Causes of Loss
- Subline ( and ) 
  - SUB, Sub_Desc
  - Basic Group I (SUB = 1)
  - Basic Group II (SUB = 2)
  - Special (SUB = 3)
- ISO classification detail
  - CLASS, Class_Description
     - For example, CLASS=932 and Class_Description='Gasoline Service Stations -- 0932'
  - Major_Class_Group
    - For example, Major_Class_Group='Non-Manufacturing/Service'
  - Rating_Class_Group
    - For example, Rating_Class_Group='Other Habitational'
  - Sub_Class_Group
    - For example, Sub_Class_Group='Dwellings Written in Conjunction with Commercial Risks & Rated from the CLM'
- Coverages (COV and Coverage)
  - Building Coverage (COV=1)
  - Contents Coverage (COV=2)
  - Indivisible buildings and personal property (COV=3)
  - Time Element (Business Interruption) Coverage (COV=4)
- Construction type (Construction_Type)
  - `Construction Not Available` 
  - `Fire Resistive`
  - `Frame` 
  - `Joisted Masonry` 
  - `Masonry Non-Combustible` 
  - `Modified Fire Resistive`
  - `Non-Combustible` 
  - `Not Applicable`
- Type of loss (TOL): Property losses segmented by category
  - `All Other`
  - `Fire & Lightning`
  - `Not Available`
  - `Water Damage`
  - `Wind`
  - `Burglary & Theft`
  - `Mold`
  - `Vandalism`
  - `Freezing`
  - `Sprinkler Leakage`
  - `Collapse`
  - `Explosion`
  - `Riot & Civil Commotion`
  - `Hail`

• Type of policy: Monoline versus commercial fire and
allied lines business written on a package policy (other
than businessowners)

• Rating: Class rated versus schedule (specific) rated,
where applicable
• Sprinklered: Sprinklered versus non-sprinklered, where
applicable

• Size of loss range
- Major catastrophes: Major catastrophes (e.g., hurricanes,
wildfires, hail events) identified separately
  - CAT_code: 308127 categories.

## Codes

### Code for category check
#### TOL Category Check

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

The TOL categories are:
- TOL_All Other
- TOL_Fire & Lightning
- TOL_Not Available
- TOL_Water Damage
- TOL_Wind
- TOL_Burglary & Theft
- TOL_Mold
- TOL_Vandalism
- TOL_Freezing
- TOL_Sprinkler Leakage
- TOL_Collapse
- TOL_Explosion
- TOL_Riot & Civil Commotion
- TOL_Hail


#### Coverage categories check

```sas
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

/* Count distinct categories */
proc sql;
    select count(distinct COV) as num_cov_categories
    from iso.iso_prop_20_24;
quit;

/* List all categories */
proc sql;
    select distinct Coverage
    from iso.iso_prop_20_24
    where Coverage is not missing
    order by Coverage;
quit;
```


#### Construction_Type categories check

```sas
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

/* Count distinct categories */
proc sql;
    select count(distinct Construction_Type) as num_categories
    from iso.iso_prop_20_24;
quit;

/* List all categories */
proc sql;
    select distinct Construction_Type
    from iso.iso_prop_20_24
    where Construction_Type is not missing
    order by Construction_Type;
quit;
```

#### CAT_code categories check

```sas
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

/* Count distinct categories */
proc sql;
    select count(CAT_code) as num_categories
    from iso.iso_prop_20_24;
quit;

/* List all categories */
proc sql;
    select distinct CAT_code
    from iso.iso_prop_20_24
    where CAT_code is not missing
    order by CAT_code;
quit;
```

#### CAT_event categories check

```sas
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

/* Count distinct categories */
proc sql;
    select count(CAT_event) as num_categories
    from iso.iso_prop_20_24;
quit;

/* List all categories */
proc sql;
    select distinct CAT_event
    from iso.iso_prop_20_24
    where CAT_event is not missing
    order by CAT_event;
quit;
```

### Code for summary

#### claim row vs premium row

## Geometric granularity

- ISO data: zip code level (ZIPCD)
- Doug's data: bg2_terr


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

- loss ratio: the most common loss ratio metric is reported loss retio, or reported losses divided by earned premium. A  loss ratio can be larger than 1 (or 100%).When the loss ratio exceeds 1, it indicates that the insurance company is paying out more in claims than it is collecting in earned premiums.

## Plan for loss ratio computation


**Loss Ratio Analysis Plan**

* The dataset is **stacked**:
  * Rows with **nonzero `EARNED_PREMIUM`** do **not** contain `TOL` and have zero LOSS_LAE_INCURRED.
  * Rows with **zero `EARNED_PREMIUM`** contain `TOL` (categorical loss type) and have nonzero LOSS_LAE_INCURRED.

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




# 05-20 joining and preparing the tables

## Task

From the discussion earlier, please join Doug’s territory information onto the ISO data by zip code.

Based on the feedback from Doug yesterday, we can aggregate the ISO TOL (peril) data into two groups: CAT related & non-CAT. The types of CAT events we will be getting from the simulated data are
•	SCS = Severe convective storm – Wind + Hail
•	HU = Hurricane
•	EQ = Earthquake
•	WS = winter storm (includes freezing)
In ISO, I think hurricane is included in the wind+hail peril. Figure out a grouping method that works to group TOL into CAT & Non-CAT using this information as context.

Lets produce a table that has the following fields:
Categorical
•	Year
•	State
•	EQ Zone
•	BGII Territory
•	Coverage [Building | Contents| time element]
•	Subline (maybe its labeled as SUB) [BGI | BGII | SCL]
•	Grouped TOL [CAT vs Non-CAT]
Numeric
•	Earned Exposure
•	Earned Premium
•	Loss+LAE

Don’t forget to add the filter for when exposures are included in the data. I will probably have more feedback after we review this data together.

Using this data, we can get the damage ratios for various segments. We will use these for the non-cat portion of the capital allocation factors.



## report
the TOL variable has categories:
  - `All Other`
  - `Fire & Lightning`
  - `Not Available`
  - `Water Damage`
  - `Wind`
  - `Burglary & Theft`
  - `Mold`
  - `Vandalism`
  - `Freezing`
  - `Sprinkler Leakage`
  - `Collapse`
  - `Explosion`
  - `Riot & Civil Commotion`
  - `Hail`
  which do not provide precise information whether it is CAT or not. However, the ISO dataset also has CAT_code variable and CAT_event variable which contains CAT related information.
 
  1.5287E8 rows where cat_code / CAT_event is blank, 308127 rows not  blank.
  among them,   there is a category named Non-catastrophe corresponding to CAT_code=0000 having 226891 rows.
   so 81,236 rows are catastrophes. 

  to classify them I use keywords:
- Starts with Hurricane
- Ends with Fire or Fires
- Starts with Riot / Civil
- Tropical Storm
- Starts with Wind & Thunderstorm / Tornadoes
- Starts with Winter Storm


the result:

CAT_group /num_categories / N_obs
Wind/Thunderstorm/Tornado 51 46315 
Winter Storm 5 16783 
Hurricane 14 12220 
Tropical Storm 6 3197 
Riot/Civil 1 1769 
Fire 10 952 
total 83126
the 6 catogires exaclty sum up to 83126 rows, so all catastrpohes are classified into these 6.

   ## Codes




### Cat blank or not
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

```
proc sql;
    select distinct CAT_event
    from iso.iso_prop_20_24
    where CAT_code ne '0000'
          and CAT_event is not missing
    order by CAT_event;
quit;
```
num_blank

num_not_blank

total_rows


1.5287E8 308127 1.5318E8 



result:

   ### finding the CAT_code for CAT_event = Non-catastrophe
  
  ```sas
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

/* Step 1: filter first */
proc sql;
    create table work.noncat_subset as
    select CAT_event, CAT_code
    from iso.iso_prop_20_24
    where CAT_event = 'Non-catastrophe'
          and CAT_code is not missing;
quit;

/* Step 2: aggregate */
proc sql;
    select CAT_event,
           CAT_code,
           count(*) as N_obs
    from work.noncat_subset
    group by CAT_event, CAT_code
    order by N_obs desc;
quit;

  ```

### count non-cat

```
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";
proc sql;
    select 
        sum(case when CAT_code = '0000' then 1 else 0 end) as num_non_cat,
        sum(case when CAT_code ne '0000' then 1 else 0 end) as num_cat,
        count(*) as total_rows
    from iso.iso_prop_20_24;
quit;
```
result:
num_non_cat num_cat total_rows
226891 1.5296E8 1.5318E8 
### overview of non-0000
```
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

proc sql;
    select distinct CAT_event
    from iso.iso_prop_20_24
    where CAT_code ne '0000'
          and CAT_event is not missing
    order by CAT_event;
quit;

```

### Catastrpohe classification step 1

```sas
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

proc sql;
    create table work.cat_event_tagged as
    select 
        CAT_event,
        case
            when upcase(CAT_event) like '%HURRICANE%' then 'Hurricane'
            when upcase(CAT_event) like '%FIRE' 
              or upcase(CAT_event) like '%FIRES' then 'Fire'
            when upcase(CAT_event) like 'RIOT%' 
              or upcase(CAT_event) like 'CIVIL%' then 'Riot/Civil'
            when upcase(CAT_event) like 'TROPICAL STORM%' then 'Tropical Storm'
            when upcase(CAT_event) like 'WIND%' 
              or upcase(CAT_event) like 'THUNDERSTORM%' 
              or upcase(CAT_event) like 'TORNADO%' then 'Wind/Thunderstorm/Tornado'
            when upcase(CAT_event) like 'WINTER STORM%' then 'Winter Storm'
            else 'Other'
        end as CAT_group
    from iso.iso_prop_20_24
    where CAT_code ne '0000'
          and CAT_event is not missing;
quit;

proc sql;
    select CAT_group,
           count(distinct CAT_event) as num_categories,
           count(*) as N_obs
    from work.cat_event_tagged
    group by CAT_group
    order by N_obs desc;
quit;

proc sql outobs=100;
    select distinct CAT_event
    from work.cat_event_tagged
    where CAT_group = 'Other'
    order by CAT_event;
quit;
```