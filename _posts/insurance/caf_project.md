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
  - Basic Group I (SUB = 1): fire
  - Basic Group II (SUB = 2):  (Wind)
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
- exposures
  - 
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



# Capital Allocation Factor Workflow


## Inputs
Peril mix for each region and statewise peril permissible loss ratios
### Input 1: Peril Mix (Average Annual Loss)

| Region     | SCS AAL | HU AAL | EQ AAL | NC AAL | Total AAL |
|------------|--------:|-------:|-------:|-------:|----------:|
| Region 1   | 450,000 | 30,000 | 15,000 | 600,000 | 1,095,000 |
| Region 2   | 50,000  | 25,000 | 12,500 | 500,000 | 587,500   |
| Region 3   | 300,000 | 20,000 | 160,000| 400,000 | 880,000   |
| Region 4   | 30,000  | 15,000 | 120,000| 300,000 | 465,000   |
| Region 5   | 20,000  | 240,000| 5,000  | 200,000 | 465,000   |
| **Total**  | **850,000** | **330,000** | **312,500** | **2,000,000** | **3,492,500** |

### Input 2: statewise PLRS by perils
The following values are assumed given:

| SCS PLR | HU PLR | EQ PLR | NC PLR |
|--------:|-------:|-------:|-------:|
| 54.3%   | 37.6%  | 40.6%  | 62.9%  |


### Research question
- What is the best way to determine the peril mix for a given region (or perhaps for a given risk)?			
- Currently, we use the two-step method:
  1. S  tate-level AALs is provided by the commercial pricing team from their indications analysis.		
- We then allocate these AALs to the (within-state) region level based on assumed damage ratio relativities.

>Damage Ratio = Average Annual Loss per $1000 Total Insured Value			

> AAL = Average Annual Loss			

> TIV = Total Insured Value			

- These relativities depend on the policies in a recent in-force book of business. Particularly in small states,		
  our in-force book may not be credible. 		
- Can a model-based approach help us generate more theoretically-reasonable peril mixes / capital charges?		

in-force : currently in our contract
historical data vs in-force modeled data vs industry modeled data
we are currently doing the second we want to do the third



# ISO Data pre-processing

## Task

From the discussion earlier, please join Doug’s territory information onto the ISO data by zip code.

Based on the feedback from Doug yesterday, we can aggregate the ISO TOL (peril) data into two groups: CAT related & non-CAT. The types of CAT events we will be getting from the simulated data are
-	SCS = Severe convective storm – Wind + Hail
-	HU = Hurricane
-	EQ = Earthquake
-	WS = winter storm (includes freezing)
In ISO, I think hurricane is included in the wind+hail peril. Figure out a grouping method that works to group TOL into CAT & Non-CAT using this information as context.

Lets produce a table that has the following fields:
- Categorical
  -	Year
  -	State
  -	EQ Zone
  -	BGII Territory
  -	Coverage [Building | Contents| time element]
  -	Subline (maybe its labeled as SUB) [BGI | BGII | SCL]
  -	Grouped TOL [CAT vs Non-CAT]
- Numeric
  -	Earned Exposure
  -	Earned Premium
  -	Loss+LAE

Don’t forget to add the filter for when exposures are included in the data. I will probably have more feedback after we review this data together.

Using this data, we can get the damage ratios for various segments. 
We will use these for the non-cat portion of the capital allocation factors.


# Data preprocessing

## Exposure
- The “coverage” referenced in the`CAF simplified example` file actually represents exposure by subline (1:bg1, 2:bg2, 3:scl).
- The `cov` variable in iso means building/content/indivisible/time element. Since the RMS data do not have this classification, we do not use `cov` for aggregation.

| peril | subline | terr      |
|-------|---------|-----------|
| WT    | 2       | bg2_terr  |
| SCS   | 2       | scs_terr  |
| HU    | 2       | bg2_terr  |
| eq    | 3       | eq_terr   |
| ff    | 3       | eq_terr   |
|non-cat | 1 | bg1_terr|

Based on this, the exposure table to be created is:

| geographical aggregation level | exposure |
|------------------|----------|
| bg2_terr         | sub=2    |
| scs_terr         | sub=2    |
| eq_terr          | sub=3    |
| bg1_terr          | sub=1    |

The first three rows are included solely to validate that catastrophic events are being separated correctly; they will not be used in the primary analysis.

## Loss
- the RMS model has EQ, FF, HU, SCS, WT (winterstorm)
- In iso, we want to capture these peril, not to use them, but to exclude them and get non-cat portion.

| Peril   | Geographic Aggregation Level |
|---------|-----------------------------|
| EQ/FF   | No records on ISO           |
| HU      | bg2_terr                    |
| SCS     | bg2_terr                    |
| WT      | bg2_terr                    |
| non-cat | bg1_terr                    |

# Capturing non-CAT portion from ISO

- The purpose of separating ISO data into CAT and Non-CAT components is to enable more reliable modeling of **baseline risk** using the **non-CAT portion** of the data.

- ISO data is historical and observational. Catastrophe events occur irregularly over time. As a result, the observed losses in any given year can be highly volatile and may not reflect the true risk of given year. For example:
  - A hurricane may occur once every five years.
  - If a hurricane occurs in a given year, that year's losses will be **artificially inflated**, while other years may show **no CAT losses at all**.

- To address this issue, catastrophe risk is instead modeled using **AAL (Average Annual Loss)**, computed from a stochastic catastrophe model.
- Instead of relying on observed discrete events, the model simulates many years of possible outcomes and derives a smoothed expectation.
 
## Excluding the CAT portion

### TOL vs CAT_event
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
These are identified based on the loss date, state, ZIP code or territory, and type of loss
associated with the catastrophe.  

### CAT_event Interpretation  

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


#### Classification Results (2020–2024)

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


#### Classification Results (2018–2022)

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


#### Observations

- Over 99% of rows have blank `CAT_event` values. Catastrophe events represent a **very small fraction** of total data.
- The classification successfully partitions all rows into **mutually exclusive categories**.
- No **Earthquake events** were identified in either dataset (2018–2022 or 2020–2024).

  

### CAT Classification Plan
- We divide the rows into **CAT-related** and **non-CAT** categories based on a combination of `CAT_event` and `TOL` information.
  - `CAT_event` captures **recognized catastrophe events** (event-based classification)  
  - `TOL` captures **loss mechanisms** (damage-based classification)  

TOL is used to capture SCS more accurately. Aligning with the RMS data, we aim to capture catastrphes of
- Earthquake
- Hurricane
- Winterstorm
- SCS.

The logic of capturing these catastrpohes is as follows:
- Rows are classified as **CAT-related** if they fall into one of the following groups:
  - `CAT_event` starts with `"Wind"`, `"Thunderstorm"`, or `"Tornado"`  
  - `CAT_event` starts with `"Winter Storm"`  
  - `CAT_event` starts with `"Hurricane"`  
  - `CAT_event` starts with `"Tropical Storm"` 
  - `CAT_event` ends with `"Fire"` or `"Fires"`  
  - `TOL = Wind` or `TOL = Hail`  
- rows are classified as **non-CAT** if they do not fall into the previous categories AND belong to:
  - `CAT_event` missing  
  - `CAT_code = '0000'`
  - `CAT_code` starts with `"Mudslide"`
  - `CAT_code` starts with `"Riot"` or `"Civil"`  
 
  
The rationale:

#### Tropical Storms and Hurricanes

- A hurricane is a strong tropical cyclone occurring in the Atlantic or Northeast Pacific.  
- A tropical storm represents a lower intensity stage of the same system.  
- Both belong to the same physical phenomenon and share similar risk drivers.  

Therefore, it is appropriate to group tropical storms with hurricanes.


#### Severe Convective Storms (SCS) and Tornadoes

- The computer model for **Severe Convective Storms (SCS)** is not limited to tornado events.  
- Instead, it captures a broader severity of losses driven by:
  - **Wind**
  - **Hail**

- As a result:
  - Even if `CAT_event` is missing,
  - Rows with `TOL = Wind` or `TOL = Hail` should still be treated as **CAT-related**

 



 

### CAT Classification Workflow
 
 

#### 1. CAT Identification (`is_CAT = 1`)

##### Hurricane (HU)
Criteria:
- `CAT_event` contains:
  - `"Hurricane"`  
  - `"Tropical Storm"`

Assignment:
- `is_CAT = 1`
- `CAT_type = 'HU'`


##### Winter Storm (WS)
Criteria:
- `CAT_event` contains:
  - `"Winter Storm"`

Assignment:
- `is_CAT = 1`
- `CAT_type = 'WS'`


#### Severe Convective Storm (SCS)

Criteria:
- `CAT_event` contains:
  - `"Wind"`, `"Thunderstorm"`, or `"Tornado"`  
**OR**
- `TOL = Wind` or `TOL = Hail`

Assignment:
- `is_CAT = 1`
- `CAT_type = 'SCS'`

####  Fire
- `CAT_event` ends with `"Fire"` or `"Fires"` → `CAT_type = 'Fire'`, `is_CAT = 1`




### 2. Non-CAT Classification (`is_CAT = 0`)

Rows are classified as non-CAT if they **do not satisfy any CAT criteria above** and follows into the following:
- Missing `CAT_event` with no supporting `TOL` signal: `is_CAT = 0`, `CAT_type = ''`
- `CAT_code = '0000'` (Non-catastrophe): `is_CAT = 0`, `CAT_type = ''`  
- `CAT_event` ends with `"Mudslide"` → `CAT_type = 'Mudslide'`, `is_CAT = 0`
- `CAT_event` starts with `"Riot"` or `"Civil"` → `CAT_type = 'Civil'`, `is_CAT = 0`
- All remaining unmatched rows: `is_CAT = 0`, `CAT_type = ''`  

  

### With/Without Exposure / Exposure Indicator
Exposure is not provided for the Time Element (Business Interruption) coverage. Additionally, certain records
have had exposure removed due to data quality issues.


## Validation of cat classification
- the ground up loss (GU) financial perspective represents total loss to the exposure and excludes any insurance or reinsurance terms in the loss calculations.
- The gross loss (GR) financial perspective represents the loss to the insurer, accounting for the application of all insurance terms but without consideration for any reinsurance recoveries.

Loss after reinsurance recoveries
What the company actually retains
Equivalent to

### Joining

####  Data Source

The analysis is based on the dataset:
/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables/iso_prop_20_24.sas7bdat

#### Variable Selection
After creating the new categorical variables (`is_CAT`, `CAT_type`), retain the following fields for downstream analysis:

- `YEAR`
- `ST`
- `ZIPCD`
- `BGII_Territory`
- `COV`
- `SUB`
- `is_CAT`
- `CAT_type`
- `EARNED_PREMIUM`
- `EARNED_EXPOSURE`
- `TOL`
- `EXPOSURE_VIEW`
- `LOSS_LAE_INCURRED`



#### ZIP Mapping
Join the main dataset with the ZIP mapping file:
/sas/data/project/EG/jmun/zip_mapping.sas7bdat
with join key:
- `ZIPCD` (main dataset) = `zip` (mapping dataset)
to add the variable:
  - `eq_risk_color`


## Creating tables
The data is noisy on the ZIPCD level. Therefore we will aggregate on a territory level. For the time being, let's prepare two tables:
1. noncat, state level
2. wind hail hurricane


pseudocode for non-cat:
create agg_iso_prop_18_22_noncat
select year, ST, SUB, 
sum(earned_premium), sum(earned_exposure), sum(earned_premium)/ sum(earned_exposure) as damage ratio
group by st, sub
from /sas/data/project/EG/jmun/agg_iso_prop_18_22.sas7bdat
where exposure_view = 'with exposure'


aggregate over territory

for the scs hurrivan bg2 territory
eq : eq terriorty
non-cat: state 



exposure separated by coverage:



swap covereage with subline


three tables


# Scale comparisons between ISO and RMS

comparison in Ohio SCS

| Variable           | N    | Mean        | Std Dev     | Minimum        | 1st Pctl    | 5th Pctl    | 25th Pctl  | Median      | 75th Pctl   | 95th Pctl    | 99th Pctl    | Maximum      |
|--------------------|------|-------------|-------------|----------------|-------------|-------------|------------|-------------|-------------|--------------|--------------|--------------|
| iso earned_exposure    | 1338 | 464834.93   | 795836.04   | 0              | 45.8330000  | 903.0070000 | 11402.88   | 90412.69    | 642997.16   | 2019014.47   | 3170730.60   | 7744521.31   |
| iso loss_incurred      | 507  | 90107.59    | 482882.05   | 3.0000000      | 321.0000000 | 1762.00     | 7500.00    | 21770.00    | 55288.00    | 265017.00    | 946214.00    | 9453910.00   |
| iso damage_ratio   | 507  | 0.3786888   | 1.7265477   | 2.5143807E-6   | 0.000578392 | 0.0018185   | 0.0141434  | 0.0418223   | 0.1660173   | 1.4827292    | 5.6232747    | 31.0825358   |
| rms tiv                | 1138 | 5242524800  | 7221842245  | 1386549.96     | 14425624.14 | 60350954.66 | 625804948  | 1956799737  | 7470847820  | 20396616531  | 30575829261  | 59773184221  |
| rms Location_GU_AAL    | 1138 | 1258294.71  | 1734993.82  | 213.8191455    | 3835.15     | 16599.87    | 198519.40  | 523674.18   | 1641872.94  | 4804241.39   | 8157281.50   | 14463048.53  |
| rms damage_ratio   | 1138 | 0.000285271 | 0.000101462 | 0.000049453    | 0.000093600 | 0.000130112 | 0.000207177| 0.000277313 | 0.000356425 | 0.000463171  | 0.000530662  | 0.000649731  |


### Ohio 2025 RMS data
 

# obsevaion OH<AK
KA more variance

ground up and gross


iso ground up


## 
- [ ] in IL, there are observations where bgII_territory is blank. they have inignorable amount of exposures. maybe they correspond to zip code xxxxx- check it.





## aa
- class_minor is 95% similar to iso class variable (ISO data has a very fine-grained class variable: 145 categories, excel file). However, new codes are added by cincy when it's necessary, so they are not identical.

- since RMS data do not have a fine grained class variable, it is better to use a coarse variable.


- iso: variable `rating_class_group` 21 categories
- RMS: variable `OCCTPE` and `O_DESC`36 categories
- CIC: variable `OCCUPANCY_TYPE_CD` and	`OCCUPANCY_TYPE_DESC`: 32 categories





### RMS data class


### CIC data category
32 categories

OCCUPANCY_TYPE_CD	OCCUPANCY_TYPE_DESC
	
  00	Unknown
  01	Permanent Dwelling (single family housing)
  02	Permanent Dwelling (multi family housing)
  03	Temporary Lodging
  04	Group Institutional Housing
  05	Retail Trade
  06	Wholesale Trade
  07	Personal and Repair Services
  08	Professional, Technical and Business Services
  09	Health Care Service
  10	Entertainment and Recreation
  11	Parking
  12	Heavy Fabrication and Assembly
  13	Light Fabrication and Assembly
  14	Food and Drugs Processing
  18	Construction
  19	Petroleum
  20	Agriculture
  21	Mining
  22	Religion and Nonprofit
  23	General Services
  25	Education
  27	Railroad
  28	Air
  29	Sea/Water
  30	Electrical
  33	Natural Gas
  37	General Commercial
  38	General Industrial
  39	Miscellaneous
  44	Gasoline Service Stations
  47	Restaurants


 


##  ISO -> CIC


| ISO Rating Class Group                | CIC Code | CIC Description                               |
| ------------------------------------- | -------- | --------------------------------------------- |
| Other Habitational                    | 02       | Permanent Dwelling (multi family housing)     |
| Apartments or Condominiums            | 02       | Permanent Dwelling (multi family housing)     |
| Motels & Hotels                       | 03       | Temporary Lodging                             |
| Restaurants & Bars                    | 47       | Restaurants                                   |
| Other Mercantile                      | 05       | Retail Trade                                  |
| Non-Governmental Offices & Banks      | 08       | Professional, Technical and Business Services |
| **Public Buildings**                      | 23   or 08    | General Services **or**     Professional, Technical and Business Services?           |
| Hospitals & Nursing Homes             | 09       | Health Care Service                           |
| Recreational Facilities               | 10       | Entertainment and Recreation                  |
| Churches and Synagogues               | 22       | Religion and Nonprofit                        |
| Schools, Academic                     | 25       | Education                                     |
| Buildings Under Construction          | 18       | Construction                                  |
| **Storage**                               | 06       | Wholesale Trade           |
| Food, Beverage, Tobacco Manufacturing | 14       | Food and Drugs Processing                     |
| Chemical Manufacturing                | 12       | Heavy Fabrication and Assembly                |
| Metal Manufacturing                   | 12       | Heavy Fabrication and Assembly                |
| Wearing Apparel                       | 13       | Light Fabrication and Assembly                |
| Wood Manufacturing                    | 13       | Light Fabrication and Assembly                |
| Other Manufacturing                   | 38       | General Industrial                            |
| Other Non-Manufacturing               | 37       | General Commercial                            |




 ### examples of public buildings in iso:
- Penal Institutions
- Museums
- Libraries
- Art Galleries (non-profit)
- Fire Dept
- Police
- Water/Sewer

### examples of storage in iso:
Piers, Wharves, Bridges
Freight Terminals
General Storage Warehouses - Bailee
Miscellaneous Products Storage - (other than Retail or Wholesale or Cold Storage)
Household Goods Storage
Cold Storage Warehouses
Farm Products (other than Grain, Cotton, Tobacco)
Grain, Seed, Bean Warehouses
Cotton Compresses and Storage
Waste and Reclaimed Material, including Yards
Whiskey and Liquor Warehouses in Connection with Distilleries
Tobacco Warehouses, Storage
Tobacco Sales Warehouses
Grain Elevators - Terminal
Grain Elevators - Country
Building Supply Yards, including Retail Lumberyards, Coal and Coke Yards
Mill Yards
Oil Distributing, Oil Terminals and LPG Tank Farms, Including Stock
Oil Distributing, Oil Terminals and LPG Tank Farms, Excluding Stock

 




#  CIC Categories with No ISO Match

| ISO Rating Class Group | CIC Code | CIC Description                            |
| ---------------------- | -------- | ------------------------------------------ |
| NULL                   | 00       | Unknown                                    |
| NULL                   | 01       | Permanent Dwelling (single family housing) **check**|
| NULL                   | 04       | Group Institutional Housing    **check** other habitaitonal            |
| NULL                   | 19       | Petroleum                                  |
| NULL                   | 20       | Agriculture                                |
| NULL                   | 21       | Mining                                     |
| NULL                   | 27       | Railroad                                   |
| NULL                   | 28       | Air                                        |
| NULL                   | 29       | Sea/Water                                  |
| NULL                   | 30       | Electrical                                 |
| NULL                   | 33       | Natural Gas                                |
| NULL                   | 39       | Miscellaneous                              |






## RMS → CIC Mapping (36 → 32)


| RMS Category                                     | CIC Code | CIC Description                               |
| ------------------------------------------------ | -------- | --------------------------------------------- |
| Unknown                                          | 00       | Unknown                                       |
| Permanent Dwelling (single family housing)       | 01       | Permanent Dwelling (single family housing)    |
| Permanent Dwelling (multi family housing)        | 02       | Permanent Dwelling (multi family housing)     |
| Multi-Family Dwelling - Homeowners Association   | 02       | Permanent Dwelling (multi family housing)     |
| Multi-Family Dwelling - Condominium Unit Owner   | 02       | Permanent Dwelling (multi family housing)     |
| Hotels- Large                                    | 03       | Temporary Lodging                             |
| Professional, Technical and Business Services    | 08       | Professional, Technical and Business Services |
| Health Care Service                              | 09       | Health Care Service                           |
| Universities and Colleges                        | 25       | Education                                     |
| General Commercial                               | 37       | General Commercial                            |
| General Industrial                               | 38       | General Industrial                            |
| Agriculture                                      | 20       | Agriculture                                   |
| Heavy Industrial - Mining                        | 21       | Mining                                        |
| Heavy Industrial - Cement                        | 12       | Heavy Fabrication and Assembly                |
| Heavy Industrial - Steel                         | 12       | Heavy Fabrication and Assembly                |
| Heavy Industrial - Pulp & Paper                  | 12       | Heavy Fabrication and Assembly                |
| Heavy Industrial - General                       | 38       | General Industrial                            |
| Chemical Processing - Primarily Indoor           | 12       | Heavy Fabrication and Assembly                |
| Light Industrial - General Manufacturing         | 13       | Light Fabrication and Assembly                |
| Light Industrial - Semiconductor                 | 13       | Light Fabrication and Assembly                |
| High Technology                                  | 13       | Light Fabrication and Assembly                |
| Light Industrial - Pharmaceutical                | 14       | Food and Drugs Processing                     |
| Light Industrial - Biomedical                    | 14       | Food and Drugs Processing                     |
| Food & Beverage                                  | 14       | Food and Drugs Processing                     |
| Petrochemical - Refineries                       | 19       | Petroleum                                     |
| Petrochemical - Pipelines                        | 19       | Petroleum                                     |
| Electric Power Generation - Fossil Fuel (Small)  | 30       | Electrical                                    |
| Electric Power Generation - Fossil Fuel (Medium) | 30       | Electrical                                    |
| Electric Power Generation - Fossil Fuel (Large)  | 30       | Electrical                                    |
| Electric Power Generation - Hydroelectric        | 30       | Electrical                                    |
| Electric Power Generation - Gas Power (Large)    | 30       | Electrical                                    |
| Electric Power - Nuclear Power Plant             | 30       | Electrical                                    |
| Electric Power - Nuclear power plant             | 30       | Electrical                                    |
| Natural Gas                                      | 33       | Natural Gas                                   |
| **Water/Sewage treatment plants**                    | 23       | General Services**                              |
| **Airport (Large)**                                 | 28       | Air                                           |



##  CIC categories with **no RMS match**

| RMS Category | CIC Code | CIC Description                                     |
| ------------ | -------- | --------------------------------------------------- |
| NULL         | 04       | Group Institutional Housing                         |
| NULL         | 05       | Retail Trade                                        |
| NULL         | 06       | Wholesale Trade                                     |
| NULL         | 07       | Personal and Repair Services                        |
| NULL         | 10       | Entertainment and Recreation                        |
| NULL         | 11       | Parking                                             |
| NULL         | 18       | Construction                                        |
| NULL         | 22       | Religion and Nonprofit                              |
| NULL         | 27       | Railroad                                            |
| NULL         | 29       | Sea/Water                                           |
| NULL         | 39       | Miscellaneous                                       |
| NULL         | 44       | Gasoline Service Stations                           |
| NULL         | 47       | Restaurants                                         |




# meeting 06-01
done so far:
- recieved the model data from reinsurance group: perils are EQ+FF, HU, SCS, WT
- recieved PLR by perils by state from Dan: categories are EQ,	HU,	SCS,	WF, NC.
- to ensure the non-cat part do not over- or under- represent when we compute the final peril mix, compared, for winterstorm in minnesota:
  - loss and damage ratio, iso vs model

will do:
 - compare class/occupancy between ISO and the modeled dat
 


# Codes

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

#### corrleation between (wind or hail) and (thunderstorm and tornado)
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

proc sql;
    select
        case
            when upcase(coalescec(TOL,'')) like '%WIND%'
              or upcase(coalescec(TOL,'')) like '%HAIL%'
            then 1 else 0
        end as tol_flag,

        case
            when substr(upcase(coalescec(CAT_event,'')),1,4) = 'WIND'
              or substr(upcase(coalescec(CAT_event,'')),1,13) = 'THUNDERSTORM'
              or substr(upcase(coalescec(CAT_event,'')),1,7) = 'TORNADO'
            then 1 else 0
        end as cat_flag,

        count(*) as N_obs

    from iso.iso_prop_18_22
    where TOL is not missing
    group by calculated tol_flag, calculated cat_flag
    order by tol_flag, cat_flag
;
quit;

proc sql;
    select
        case
            when upcase(coalescec(TOL,'')) like '%WIND%'
              or upcase(coalescec(TOL,'')) like '%HAIL%'
            then 1 else 0
        end as tol_flag,

        case
            when substr(upcase(coalescec(CAT_event,'')),1,4) = 'WIND'
              or substr(upcase(coalescec(CAT_event,'')),1,13) = 'THUNDERSTORM'
              or substr(upcase(coalescec(CAT_event,'')),1,7) = 'TORNADO'
            then 1 else 0
        end as cat_flag,

        count(*) as N_obs

    from iso.iso_prop_10_24
    where TOL is not missing
    group by calculated tol_flag, calculated cat_flag
    order by tol_flag, cat_flag
;
quit;


#### earned exposure 0 and positive
```sas
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

proc sql outobs=10;
    select *
    from iso.iso_prop_18_22
    where EARNED_EXPOSURE > 0;
quit;

proc sql outobs=10;
    select *
    from iso.iso_prop_18_22
    where EARNED_EXPOSURE > 0
          and TOL is not missing;
quit;
```




#### Join
```sas
proc sql;
    create table work.grouping as
    select
        a.YEAR,
        a.ST,
        a.ZIPCD,
        a.BGII_Territory,
        a.COV,
        a.SUB,
        a.EARNED_PREMIUM,
        a.EARNED_EXPOSURE,
        a.TOL,
        a.EXPOSURE_VIEW,
        a.LOSS_LAE_INCURRED,

        b.eq_risk_color,

        case
            when upcase(coalescec(a.CAT_event,'')) like '%MUDSLIDE%' then 'Mudslide'
            when upcase(coalescec(a.CAT_event,'')) like 'RIOT%' 
              or upcase(coalescec(a.CAT_event,'')) like 'CIVIL%' then 'Civil'

            when upcase(coalescec(a.CAT_event,'')) like '%HURRICANE%' 
              or upcase(coalescec(a.CAT_event,'')) like '%TROPICAL STORM%' then 'HU'

            when upcase(coalescec(a.CAT_event,'')) like '%WINTER STORM%' then 'WS'

            when (upcase(coalescec(a.CAT_event,'')) like '%WIND%' 
                  or upcase(coalescec(a.CAT_event,'')) like '%THUNDERSTORM%' 
                  or upcase(coalescec(a.CAT_event,'')) like '%TORNADO%')
              or (upcase(coalescec(a.TOL,'')) like '%WIND%' 
                  or upcase(coalescec(a.TOL,'')) like '%HAIL%')
            then 'SCS'

            when upcase(coalescec(a.CAT_event,'')) like '%FIRE%' then 'Fire'

            else ''
        end as CAT_type length=10,

        case
            when upcase(coalescec(a.CAT_event,'')) like '%MUDSLIDE%' then 0
            when upcase(coalescec(a.CAT_event,'')) like 'RIOT%' 
              or upcase(coalescec(a.CAT_event,'')) like 'CIVIL%' then 0
            when a.CAT_code = '0000' then 0

            when upcase(coalescec(a.CAT_event,'')) like '%HURRICANE%' 
              or upcase(coalescec(a.CAT_event,'')) like '%TROPICAL STORM%' then 1

            when upcase(coalescec(a.CAT_event,'')) like '%WINTER STORM%' then 1

            when (upcase(coalescec(a.CAT_event,'')) like '%WIND%' 
                  or upcase(coalescec(a.CAT_event,'')) like '%THUNDERSTORM%' 
                  or upcase(coalescec(a.CAT_event,'')) like '%TORNADO%')
              or (upcase(coalescec(a.TOL,'')) like '%WIND%' 
                  or upcase(coalescec(a.TOL,'')) like '%HAIL%')
            then 1

            when upcase(coalescec(a.CAT_event,'')) like '%FIRE%' then 1

            else 0
        end as is_CAT

    from iso.iso_prop_20_24 as a
    left join mylib.zip_mapping as b
        on a.ZIPCD = put(b.zip, z5.)
;
quit;


proc sql;
create table mylib.agg_iso_prop_20_24 as
    select
        YEAR,
        ST,
        ZIPCD,
        BGII_Territory,
        COV,
        SUB,
        EXPOSURE_VIEW,
        TOL,
        CAT_type,
        is_CAT,
        eq_risk_color,

        sum(EARNED_PREMIUM) as EARNED_PREMIUM,
        sum(EARNED_EXPOSURE) as EARNED_EXPOSURE,
        sum(LOSS_LAE_INCURRED) as LOSS_LAE_INCURRED

    from work.grouping 

    group by
        YEAR,
        ST,
        ZIPCD,
        BGII_Territory,
        COV,
        SUB,
        EXPOSURE_VIEW,
        TOL,
        CAT_type,
        is_CAT,
        eq_risk_color
;
quit;
```


#### 18-22
```sas
proc sql;
    create table work.grouping as
    select
        a.YEAR,
        a.ST,
        a.ZIPCD,
        a.BGII_Territory,
        a.COV,
        a.SUB,
        a.EARNED_PREMIUM,
        a.EARNED_EXPOSURE,
        a.TOL,
        a.EXPOSURE_VIEW,
        a.LOSS_LAE_INCURRED,

        b.eq_risk_color,

        case
            when upcase(coalescec(a.CAT_event,'')) like '%MUDSLIDE%' then 'Mudslide'
            when upcase(coalescec(a.CAT_event,'')) like 'RIOT%' 
              or upcase(coalescec(a.CAT_event,'')) like 'CIVIL%' then 'Civil'

            when upcase(coalescec(a.CAT_event,'')) like '%HURRICANE%' 
              or upcase(coalescec(a.CAT_event,'')) like '%TROPICAL STORM%' then 'HU'

            when upcase(coalescec(a.CAT_event,'')) like '%WINTER STORM%' then 'WS'

            when (upcase(coalescec(a.CAT_event,'')) like '%WIND%' 
                  or upcase(coalescec(a.CAT_event,'')) like '%THUNDERSTORM%' 
                  or upcase(coalescec(a.CAT_event,'')) like '%TORNADO%')
              or (upcase(coalescec(a.TOL,'')) like '%WIND%' 
                  or upcase(coalescec(a.TOL,'')) like '%HAIL%')
            then 'SCS'

            when upcase(coalescec(a.CAT_event,'')) like '%FIRE%' then 'Fire'

            else ''
        end as CAT_type length=10,

        case
            when upcase(coalescec(a.CAT_event,'')) like '%MUDSLIDE%' then 0
            when upcase(coalescec(a.CAT_event,'')) like 'RIOT%' 
              or upcase(coalescec(a.CAT_event,'')) like 'CIVIL%' then 0
            when a.CAT_code = '0000' then 0

            when upcase(coalescec(a.CAT_event,'')) like '%HURRICANE%' 
              or upcase(coalescec(a.CAT_event,'')) like '%TROPICAL STORM%' then 1

            when upcase(coalescec(a.CAT_event,'')) like '%WINTER STORM%' then 1

            when (upcase(coalescec(a.CAT_event,'')) like '%WIND%' 
                  or upcase(coalescec(a.CAT_event,'')) like '%THUNDERSTORM%' 
                  or upcase(coalescec(a.CAT_event,'')) like '%TORNADO%')
              or (upcase(coalescec(a.TOL,'')) like '%WIND%' 
                  or upcase(coalescec(a.TOL,'')) like '%HAIL%')
            then 1

            when upcase(coalescec(a.CAT_event,'')) like '%FIRE%' then 1

            else 0
        end as is_CAT

    from iso.iso_prop_18_22 as a
    left join mylib.zip_mapping as b
        on a.ZIPCD = b.zip

;
quit;


proc sql;
create table mylib.agg_iso_prop_18_22 as
    select
        YEAR,
        ST,
        ZIPCD,
        BGII_Territory,
        COV,
        SUB,
        EXPOSURE_VIEW,
        TOL,
        CAT_type,
        is_CAT,
        eq_risk_color,

        sum(EARNED_PREMIUM) as EARNED_PREMIUM,
        sum(EARNED_EXPOSURE) as EARNED_EXPOSURE,
        sum(LOSS_LAE_INCURRED) as LOSS_LAE_INCURRED

    from work.grouping 

    group by
        YEAR,
        ST,
        ZIPCD,
        BGII_Territory,
        COV,
        SUB,
        EXPOSURE_VIEW,
        TOL,
        CAT_type,
        is_CAT,
        eq_risk_color
;
quit;
```

#### industry data statewide damage ratio

```python
import pandas as pd
import os
import re

# ✅ Folder containing your files
folder_path = "RMS 2025 CAT"

results = []

# ✅ Loop through all CSV files
for file in os.listdir(folder_path):
    if file.endswith(".csv"):

        file_path = os.path.join(folder_path, file)

        # ✅ Extract catastrophe tag from filename
        # looks for EQ / FF / HU / SCS / WT
        match = re.search(r'\b(EQ|FF|HU|SCS|WT)\b', file)
        cat_event = match.group(1) if match else "UNKNOWN"

        print(f"Processing: {file} → {cat_event}")

        # ✅ Load data
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()

        # ✅ Convert numeric columns
        cols = ["TIV", "Location_GU_AAL", "Location_GR_AAL"]
        df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")

        # ✅ Aggregate by state
        agg = (
            df.groupby("STATECODE", dropna=False)
              .agg(
                  TIV_sum=("TIV", "sum"),
                  GU_AAL_sum=("Location_GU_AAL", "sum"),
                  GR_AAL_sum=("Location_GR_AAL", "sum"),
              )
              .reset_index()
        )

        # ✅ Compute ratios
        agg["GU_damage_ratio"] = agg["GU_AAL_sum"] / agg["TIV_sum"]
        agg["GR_damage_ratio"] = agg["GR_AAL_sum"] / agg["TIV_sum"]

        # ✅ Add catastrophe event label
        agg["cat_event"] = cat_event

        # ✅ Store result
        results.append(agg)

# ✅ Combine all files
final_df = pd.concat(results, ignore_index=True)

# ✅ Optional: sort
final_df = final_df.sort_values(["cat_event", "GU_damage_ratio"], ascending=[True, False])

# ✅ Save output
output_path = os.path.join(folder_path, "state_damage_ratios_by_cat.csv")
final_df.to_csv(output_path, index=False)

print("Saved to:", output_path)
```
