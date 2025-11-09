# Data Exploration — HCICS MVP

This folder contains exploratory data analysis (EDA) for the
**Humanitarian Crisis Intelligence and Communication System (HCICS)** project.
The exploration focuses on understanding the distribution of
**internally displaced persons (IDPs)** and **health facility availability**
across Sudan before conducting formal geospatial analysis.

---

## Contents

**Notebook:**

- `data_exploration.ipynb`

**Datasets Explored:**

- `clean_idps_state.csv` — State-level IDP displacement data (18 states)
- `clean_idps_locality.csv` — Locality-level IDP displacement data
(187 localities)
- `clean_health_facilities.csv` — Health facility locations and types
(1,126 facilities)
- `lookup_localities.csv` — Administrative boundary reference (localities)
- `lookup_states.csv` — Administrative boundary reference (states)

---

## Exploration Approach

This notebook uses **descriptive statistics and visualizations** to understand
patterns in the humanitarian crisis data. No inferential statistics or
predictive modeling are performed at this stage.

---

## Key Questions Explored

### 1. Where are IDPs concentrated?

- State-level and locality-level distribution analysis
- Top 10 states and localities by IDP population
- Percentage of national IDP population by region

### 2. Where are people fleeing from?

- Origin state analysis showing displacement patterns
- Identification of primary conflict zones
- Understanding migration flows

### 3. What health facilities are available?

- Distribution of facility types (hospitals, clinics, pharmacies, etc.)
- Critical facility count (hospitals + clinics)
- Data quality assessment (name completeness, coordinate precision)

### 4. How is the data structured for the dashboard?

- State–locality hierarchical relationships
- Validation that locality data aggregates correctly to state totals
- Preview of drill-down interface structure

### 5. What are IDP household characteristics?

- Average household size distribution
- Non-Sudanese IDP population analysis
- Nationality breakdown by state

---

## Visualizations Generated

- **Horizontal bar charts:** Top states/localities by IDP population
- **Pie and bar charts:** Health facility type distribution
- **Histograms:** Household size distribution, localities per state
- **Comparative bar charts:** Origin state analysis
- **Hierarchical drill-down demonstration:** State → locality view
- **Data quality metrics visualization**

---

## Key Findings

- ~6.55 million total IDPs across Sudan
- Top 3 states (**River Nile**, **South Darfur**, **East Darfur**) host ~30% of
all IDPs
- **Khartoum** is the primary origin of displacement (conflict epicenter)
- Only **238 critical facilities** (hospitals + clinics) — 21% of total
facilities
- **Data quality is high:** 97% of facilities have names, nearly 100% have valid
coordinates
- **Hierarchical structure validated:** Locality data correctly aggregates to
state level
- **Average household size:** ~5 people per household

---

## Observations for Analysis Phase

The exploration identifies potential geographic mismatches between IDP
concentrations and health facility locations, particularly in:

- States with high IDP populations but dispersed facilities
- **Darfur region** showing both high displacement and origin patterns
- **River Nile** hosting significant IDPs despite not being a conflict origin

These findings guide the **next phase** — formal geospatial analysis to
calculate accessibility metrics and generate vulnerability maps.

---

## Notes

- **Reproducibility:** Notebook can be run independently with relative file
paths
- **No inference:** Analysis is purely descriptive; no statistical testing or
modeling performed
- **Dashboard preparation:** Section 5 validates the hierarchical data structure
for the interactive drill-down map

---

## Next Steps

The findings from this exploration will guide the
**Analysis Phase (Milestone 3):**

1. Conduct **geospatial proximity analysis** (IDP locations → nearest health
facility)
2. Calculate **accessibility metrics** (distance, travel time)
3. Create **composite vulnerability scores** by locality
4. Generate **“Map of Vulnerability”** for resource allocation decisions
5. Identify **critical service gaps** requiring immediate intervention

---

**Author:** Abdulrahman Sirelkhatim

**Program:** MIT Emerging Talent — Capstone Project (ELO2 Track 2)

**Date:** November 8, 2025
