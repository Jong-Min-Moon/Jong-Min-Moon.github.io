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

Using this data, we can get the damage ratios for various segments. 
- We will use these for the non-cat portion of the capital allocation factors.



## Report

The `TOL` variable contains the following categories:

- All Other  
- Fire & Lightning  
- Not Available  
- Water Damage  
- Wind  
- Burglary & Theft  
- Mold  
- Vandalism  
- Freezing  
- Sprinkler Leakage  
- Collapse  
- Explosion  
- Riot & Civil Commotion  
- Hail  

These categories do not clearly indicate the nature of the loss, specifically whether a loss was a result of hurricane, storm or earthquake. However, the ISO datacube dataset provides two additional variables:

- `CAT_code`
- `CAT_event`

These variables contain explicit catastrophe-related information.


### CAT Event Classification Logic

To classify catastrophe events, the following keyword-based rules were applied:

- Starts with `"Hurricane"` → Hurricane  
- Ends with `"Fire"` or `"Fires"` → Fire  
- Starts with `"Riot"` or `"Civil"` → Riot/Civil  
- Starts with `"Tropical Storm"` → Tropical Storm  
- Starts with `"Wind"`, `"Thunderstorm"`, or `"Tornado"` → Wind/Thunderstorm/Tornado  
- Starts with `"Winter Storm"` → Winter Storm  
- Ends with `"Mudslide"` → Mudslide  
- `CAT_code = '0000'` → Non-catastrophe  
- Missing `CAT_event` → Blank  


### Classification Results (2020–2024)

| CAT Group                         | Count       |
|----------------------------------|------------|
| Blank                            | 152,874,889 |
| Non-catastrophe                  | 226,891     |
| Wind/Thunderstorm/Tornado        | 46,315      |
| Winter Storm                     | 16,783      |
| Hurricane                        | 12,220      |
| Tropical Storm                   | 3,197       |
| Riot/Civil                       | 1,769       |
| Fire                             | 952         |

**Total: 153,183,016**


### Classification Results (2018–2022)

| CAT Group                         | Count       |
|----------------------------------|------------|
| Blank                            | 157,990,518 |
| Non-catastrophe                  | 264,381     |
| Wind/Thunderstorm/Tornado        | 23,725      |
| Winter Storm                     | 15,469      |
| Hurricane                        | 9,937       |
| Tropical Storm                   | 2,678       |
| Riot/Civil                       | 1,801       |
| Fire                             | 1,044       |
| Mudslide                         | 14          |

**Total: 158,309,567**

### Tropical storms

what are tropical storms?  in 20_24 data, CAT_event that contain Tropical Storm are:
Tropical Storm Alberto 
Tropical Storm Elsa 
Tropical Storm Fred 
Tropical Storm Hilary 
Tropical Storm Isaias 
Tropical Storm Ophelia 

Hurricane refers to a strong tropical cyclone occurs in Atlantic ocean or NE Pacific Ocean (https://en.wikipedia.org/wiki/Tropical_cyclone) (e.g. in the north america.)
Therefore hurricane and tropical storms fall into same category. but let us disstinguish them in sub-categories.

### Observations

- Over 99% of rows have blank `CAT_event` values. Catastrophe events represent a **very small fraction** of total data.
- The classification successfully partitions all rows into **mutually exclusive categories**.
- No **Earthquake events** were identified in either dataset (2018–2022 or 2020–2024).

## Feedback 05-21 morning
tornado and hurricane are very differnt in nature.
tornados are mostly followed by hail. so tornado can be identified as wind+hail




wind hail
hurricane
winterstorm
everything else


completely remove anything related to catastrophic fire


### CAT Classification 

#### Objective
Classify each row into:
- `is_CAT` indicator (1 = catastrophe, 0 = non-catastrophe)
- `CAT_type` (SCS, Hurricane, WinterStorm, or missing for non-cat)
We do not analyze all catastrophes; we only do what simulation model exists. thery are scs, hurrican, winterstorm and earthquake, but the cat_event do not contain earthquakes

#### Strategy
- Classification relies on both:
  - `CAT_event` (text-based patterns)
  - `TOL` (for SCS identification)
- Missing `CAT_event` values are still eligible for SCS classification
- Categories are **mutually exclusive**
- Priority-based logic ensures no overlap

#### Rules
#####  Exclusion Rules

The following rows **must NOT be classified as CAT (is_CAT = 1)**:

Rows where `CAT_event`:
- Ends with `"Fire"` or `"Fires"`
- Ends with `"Mudslide"`
- Starts with `"Riot"` or `"Civil"`

These rows are automatically treated as **non-catastrophe (is_CAT = 0)**. Because they are not the types of catastrpohe that we want to analyze.


##### CAT Classification Rules (is_CAT = 1)
A row is classified as a catastrophe (`is_CAT = 1`) only if it passes the exlusion rule and satisfies one of the following conditions:

##### Severe Convective Storm (SCS)

Criteria:
- `CAT_event` **does NOT contain**:
  - `"Tropical Storm"`
  - `"Hurricane"`
- AND `TOL` is:
  - `"Wind"` OR `"Hail"`
- `CAT_event` **can be blank or non-blank**

Assignment:
- `is_CAT = 1`
- `CAT_type = 'SCS'`

##### Hurricane

Criteria:
- `CAT_event` contains:
  - `"Tropical Storm"` OR
  - `"Hurricane"`

Assignment:
- `is_CAT = 1`
- `CAT_type = 'HU'`

##### Winter Storm

Criteria:
- `CAT_event` contains:
  - `"Winter Storm"`

Assignment:
- `is_CAT = 1`
- `CAT_type = 'WS'`


#####  Non-CAT Classification

All rows that do not get CAT_type by the criteria above gets:

- `is_CAT = 0`
- `CAT_type = NULL`


##### Processing Order (Important)
1. Apply **Exclusion Rules** (Fire, Mudslide, Riot/Civil)  
2. Assign **Hurricane**  
3. Assign **Winter Storm**  
4. Assign **SCS**  
5. Everything else → **Non-CAT**


### Joining
After creating new categorical variable, we retain variables:
-	YEAR
-	ST
- ZIPCD
- BGII_Territory
- COV
- SUB
- is_CAT
- CAT_type
- earned_premium
- earned_exposure
- TOL


SCL_Territory
•	EQ Zone

 •	Grouped TOL [CAT vs Non-CAT]
Numeric
•	Earned Exposure
•	Earned Premium
•	Loss+LAE







   ## Codes

### TOL Category Check 20_24

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

### TOL Category Check 20_24

```sas
/* Assign library to the exact folder */
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

/* Verify dataset exists and is readable */
proc contents data=iso.iso_prop_18_22;
run;

/* Your query using that dataset */
proc sql;
    select TOL,
           count(*) as N_obs
    from iso.iso_prop_18_22
    where TOL is not missing
    group by TOL
    order by N_obs desc;
quit;+

```
 

### Catastrpohe classification for 20-24

```sas
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";


/* Step 1: Tag CAT_event into groups */
proc sql;
    create table work.cat_event_tagged as
    select 
        CAT_event,
        CAT_code,
        case
            when CAT_event is missing then 'Blank'
            when upcase(CAT_event) like '%NON-CATASTROPHE%' then 'Non-catastrophe'
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
            when upcase(CAT_event) like '%MUDSLIDE' then 'Mudslide'
            else 'Other'
        end as CAT_group
    from iso.iso_prop_20_24;
quit;


proc sql;
    select CAT_group,
           put(count(*), comma20.) as N_obs_format
    from work.cat_event_tagged
    group by CAT_group;
quit;

```

### Catastrpohe classification for 18-22

```sas
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";


/* Step 1: Tag CAT_event into groups */
proc sql;
    create table work.cat_event_tagged as
    select 
        CAT_event,
        CAT_code,
        case
            when CAT_event is missing then 'Blank'
            when upcase(CAT_event) like '%NON-CATASTROPHE%' then 'Non-catastrophe'
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
            when upcase(CAT_event) like '%MUDSLIDE' then 'Mudslide'
            else 'Other'
        end as CAT_group
    from iso.iso_prop_18_22;
quit;


proc sql;
    select CAT_group,
           put(count(*), comma20.) as N_obs_format
    from work.cat_event_tagged
    group by CAT_group;
quit;

```

#### is there an earthquake?
```
proc sql;
    select distinct CAT_event
    from iso.iso_prop_18_22
    where CAT_code ne '0000'
          and CAT_event is not missing
          and upcase(CAT_event) like '%EARTHQUAKE%';
quit;

proc sql;
    select distinct CAT_event
    from iso.iso_prop_20_24
    where CAT_code ne '0000'
          and CAT_event is not missing
          and upcase(CAT_event) like '%EARTHQUAKE%';
quit;
```

#### tropical storm overview
```sas
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

/* view top 100. we can see that CAT_event is in the format of Tropical Storm XXX, for example, Tropical Strom Isaias */
proc sql outobs=100;
    select *
    from iso.iso_prop_20_24
    where CAT_event is not missing
          and upcase(CAT_event) like '%TROPICAL STORM%';
quit;


proc sql;
    select distinct CAT_event
    from iso.iso_prop_20_24
    where CAT_event is not missing
          and upcase(CAT_event) like '%TROPICAL STORM%'
    order by CAT_event;
quit;

```