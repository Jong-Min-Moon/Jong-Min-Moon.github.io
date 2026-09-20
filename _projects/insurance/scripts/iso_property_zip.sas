libname iso "/sas/data/project/EG/ActShared/ISO_DataCube/Scrubbed_DataCube_Tables";


proc sql;
    create table work.zip_totals as
    select YEAR,
           ZIPCD,
           min(ST) as ST,  
           sum(EARNED_PREMIUM) as TOTAL_PREMIUM,
           sum(LOSS_LAE_INCURRED) as TOTAL_LOSS
    from iso.iso_prop_20_24
    group by YEAR, ZIPCD;
quit;

proc sql;
    create table work.zip_tol_long as
    select YEAR,
           ZIPCD,
           min(ST) as ST,  
           TOL,
           sum(LOSS_LAE_INCURRED) as TOL_LOSS
    from iso.iso_prop_20_24
    where EARNED_PREMIUM = 0 and TOL is not missing
    group by YEAR, ZIPCD, TOL;
quit;

proc sql;
    create table work.zip_tol_share as
    select a.YEAR,
           a.ZIPCD,
           a.ST,
           a.TOL,
           a.TOL_LOSS,
           b.TOTAL_LOSS,
           a.TOL_LOSS / b.TOTAL_LOSS as LR_TOL
    from work.zip_tol_long as a
    left join work.zip_totals as b
    on a.YEAR = b.YEAR and a.ZIPCD = b.ZIPCD;
quit;

proc sort data=work.zip_tol_share;
    by YEAR ZIPCD ST;
run;

proc transpose data=work.zip_tol_share
    out=work.zip_tol_wide(drop=_NAME_)
    prefix=TOL_;
    by YEAR ZIPCD ST;
    id TOL;
    var LR_TOL;
run;
