# data/raw/ — Source Data Provenance

## Original source
Care Quality Commission. 2026. Care directory with ratings (04 August 2026)
[Data set]. CQC. https://www.cqc.org.uk/system/files/2026-08/04_August_2026_Latest_ratings.ods
(.ods, 25.70MB, English)

Listed publicly at: https://www.cqc.org.uk/about-us/transparency/using-cqc-data

## Files in this folder

**`19_August_2026_CQC_directory.csv`**
Full, unmodified download of CQC's locations listing. Used in Stage 5
(integrate) of the pipeline to join facility name, region, and provider
details onto the ratings data.

**`Locations_ratings_correct_extract.csv`**
A filtered subset of `04_August_2026_Latest_ratings.ods` (linked above;
25.70MB, exceeding GitHub's 25MB upload limit), containing only rows
where Domain = "Responsive" and Care Home? = "Y" — the exact filter
applied in Stage 2 of the pipeline (see src/etl/cqc_pipeline_dag.py).
17,030 rows, independently verified against the original .ods file
using COUNTIFS formulas in Google Sheets
(=COUNTIFS(S:S,"Responsive",D:D,"Y")).

The original, unfiltered file (319,798 rows) can be re-downloaded
directly from the CQC URL above to independently reproduce this extract.
