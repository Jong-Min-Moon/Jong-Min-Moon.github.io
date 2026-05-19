libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";

/* Step 1: State-level totals */
proc sql;
    create table work.st_totals as
    select YEAR,
           ST,
           sum(EARNED_PREMIUM) as TOTAL_PREMIUM,
           sum(LOSS_LAE_INCURRED) as TOTAL_LOSS
    from iso.iso_prop_20_24
    group by YEAR, ST;
quit;

/* Step 2: State-level TOL losses (long format) */
proc sql;
    create table work.st_tol_long as
    select YEAR,
           ST,
           TOL,
           sum(LOSS_LAE_INCURRED) as TOL_LOSS
    from iso.iso_prop_20_24
    where EARNED_PREMIUM = 0 and TOL is not missing
    group by YEAR, ST, TOL;
quit;

/* Step 3: Compute TOL share (composition of loss) */
proc sql;
    create table work.st_tol_share as
    select a.YEAR,
           a.ST,
           a.TOL,
           a.TOL_LOSS,
           b.TOTAL_LOSS,
           a.TOL_LOSS / b.TOTAL_PREMIUM as LR_TOL
    from work.st_tol_long as a
    left join work.st_totals as b
    on a.YEAR = b.YEAR and a.ST = b.ST;
quit;

proc sort data=work.st_tol_share;
    by YEAR ST;
run;

/* Step 4: Pivot to wide format (14 TOL columns automatically) */
proc transpose data=work.st_tol_share
    out=work.st_tol_wide(drop=_NAME_)
    prefix=TOL_;
    by YEAR ST;
    id TOL;
    var LR_TOL;
run;