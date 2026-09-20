/* Step 1: Assign ISO library */
libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

/* Step 2: Aggregate by ZIPCD */
proc sql;
    create table work.summary_by_zipcd as
    select ZIPCD,
           count(*) as N_obs,
           sum(EARNED_PREMIUM) as SUM_EARNED_PREMIUM,
           mean(EARNED_PREMIUM) as MEAN_EARNED_PREMIUM,
           std(EARNED_PREMIUM) as SD_EARNED_PREMIUM,
           sum(LOSS_LAE_INCURRED) as SUM_LOSS_LAE_INCURRED,
           mean(LOSS_LAE_INCURRED) as MEAN_LOSS_LAE_INCURRED,
           std(LOSS_LAE_INCURRED) as SD_LOSS_LAE_INCURRED
    from iso.iso_prop_20_24
    group by ZIPCD;
quit;
