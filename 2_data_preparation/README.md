# Data Preparation — HCICS MVP

This folder contains the ETL (Extract, Transform, Load) scripts used to clean
and standardize raw datasets for the Humanitarian Crisis Intelligence and
Communication System (HCICS) MVP. These scripts transform fragmented
humanitarian data into analysis-ready formats while preserving data lineage and
reproducibility.

## Overview

The data preparation pipeline processes three core datasets:

- IDP Displacement Data (IOM DTM) — Locality and state-level IDP statistics
- Administrative Boundaries (OCHA COD-AB) — Sudan's administrative geography
- Health Facilities (HOT OSM) — Geospatial point data of health infrastructure

All scripts follow reproducible research practices:

- Original raw files are never modified
- Scripts read from `../1_datasets/raw/` and write to `../1_datasets/clean/`
- Transformations are documented through code comments and this README

---

## Script Inventory

### 1. `1_clean_idps_data.py`

**Purpose:**
Cleans and standardizes IDP displacement data at state (ADM1) and locality
(ADM2) levels.

**Input Files:**

- `raw_idps_locality_data.csv`
- `raw_idps_state_data.csv`

**Output Files:**

- `clean_idps_locality.csv`
- `clean_idps_state.csv`

**Key Transformations:**

- Removes metadata header rows and invalid entries
- Standardizes column names to snake_case
- Converts numeric fields and fills missing values
- Computes fields such as:

  - `has_origin_breakdown`
  - `nationality_data_complete`
  - `avg_household_size`
  - `non_sudanese_percentage`
  - `displacement_concentration_pct` (state-level)

**Data Quality Validation:**

- Verifies locality totals align with state totals
- Identifies states with highest IDP concentrations
- Flags incomplete nationality breakdowns

**Usage:**
python 1_clean_idps_data.py

---

### 2. `2_clean_boundaries_data.py`

**Purpose:**
Cleans and standardizes Sudan's administrative boundary gazetteer.

**Input File:**

- `raw_boundaries_data.csv`

**Output Files:**

- `clean_boundaries_data.csv`
- `boundaries_state_summary.csv`
- `lookup_states.csv`
- `lookup_localities.csv`

**Key Transformations:**

- Removes redundant alternative name fields
- Renames columns for consistency
- Converts dates and area measurements to numeric formats
- Trims whitespace and normalizes text
- Generates derived fields such as:

  - `size_category`
  - `state_name_standardized`
  - `is_special_admin`

**Usage:**
python 2_clean_boundaries_data.py

---

### 3. `3_clean_health_facilities.py`

**Purpose:**
Extracts, cleans, and standardizes geospatial health facility data from a HOT
OSM shapefile archive.

**Input File:**

- `raw_health_facilities.zip` (shapefile bundle)

**Output Files:**

- `clean_health_facilities.csv`
- `facilities_summary.csv`

**Key Processing Steps:**

- Extracts shapefile and loads using GeoPandas
- Extracts coordinates and standardizes attributes
- Categorizes facility types (e.g., hospital, clinic, pharmacy)
- Flags missing names
- Generates fallback display names
- Filters points to Sudan geographic extent

**Usage:**
python 3_clean_health_facilities.py

---

## Data Quality Summary

**IDP Data:**

- ~6.5 million IDPs represented
- 100% completeness at locality and state aggregation

**Boundaries:**

- 19 states and 187 localities
- National-level coverage

**Health Facilities:**

- 1,126 facilities processed
- ~97% have original names
- ~86% have Arabic names
- Majority are pharmacies, followed by clinics and hospitals

---

## Dependencies

- pandas
- numpy
- geopandas (required for Script 3)
- zipfile, shutil, pathlib

**Installation:**
pip install pandas numpy geopandas

---

## Reproducibility Notes

- Update file paths in scripts to match your system layout
- Run scripts in sequence for consistent downstream results
- Raw data is preserved and never overwritten
- All outputs use UTF-8 with BOM for interoperability

---

## Future Enhancements

- Add time-series analysis for displacement trends
- Integrate shapefiles for full spatial joins
- Add facility capacity and operational status indicators

---

## Data Lineage and Sources

All datasets originate from the Humanitarian Data Exchange (HDX):

- Sudan Displacement Data (IOM DTM)
- Sudan Administrative Boundaries (OCHA COD-AB)
- Sudan Health Facilities (OSM / HOT Export)

Reference download links are documented in:
../1_datasets/README.md

---

**Author:** Abdulrahman Sirelkhatim
**Program:** MIT Emerging Talent — Capstone Project (ELO2 Track 2)
**Last Updated:** November 7, 2025
