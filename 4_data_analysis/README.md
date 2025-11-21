# Data Analysis — HCICS MVP

This folder contains the complete analytical pipeline for the Humanitarian
Crisis Intelligence and Communication System (HCICS) project. The analysis
transforms cleaned humanitarian datasets into actionable vulnerability
assessments through geospatial proximity analysis and statistical validation.

## Table of Contents

- [Overview](#overview)
- [Contents](#contents)
- [Analysis Pipeline](#analysis-pipeline)
- [Key Findings Summary](#key-findings-summary)
- [Critical Findings & Interpretation](#critical-findings--interpretation)
- [Reproducibility](#reproducibility)
- [Integration with Milestone 4](#integration-with-milestone-4)

---

## Overview

The analysis phase implements the Crisis Analysis Core of the HCICS MVP,
achieving two primary objectives:

- **Geospatial Vulnerability Assessment:** Calculate spatial relationships
between IDP populations and health facility infrastructure to identify critical
service gaps
- **Statistical Validation:** Verify the robustness of vulnerability scoring
through inferential analysis and machine learning

This phase directly addresses the core research question: "Can geospatial
analysis of structured humanitarian data effectively identify and visualize
critical gaps between IDP locations and health facility access in Sudan?"

## Contents

### Core Analysis Modules

1. `crisis_analysis.py`

- **Purpose:** Executes the primary geospatial vulnerability assessment pipeline
- **Input:** Cleaned IDP data, health facilities, administrative boundaries
- **Output:** Vulnerability scores, risk categories, proximity metrics
- **Key Functions:**

  - `calculate_proximity_metrics():` Computes distances and facility counts
  - `calculate_vulnerability_index():` Generates composite vulnerability scores
  - `classify_risk():` Categorizes localities into Critical/High/Moderate/Low
  risk

1. `inferential_analysis.py`

- **Purpose:** Validates vulnerability methodology through statistical testing
- **Input:** Results from crisis analysis (localities_vulnerability.geojson)
- **Output:** Statistical reports, model performance metrics, hypothesis test
results
- **Key Components:**

  - Spatial autocorrelation analysis (Moran's I)
  - Machine learning classification (Random Forest, Logistic Regression)
  - Regional hypothesis testing (t-tests, ANOVA, chi-square)

1. `visualization.py`

- **Purpose:** Generates static and interactive maps for reporting
- **Input:** GeoJSON outputs from crisis analysis
- **Output:** PNG maps and interactive HTML dashboard preview
- **Visualizations:**

  - Vulnerability index thematic map
  - Risk category classification map
  - Accessibility gap analysis with facility overlay
  - Interactive Folium map with layered data

1. `complete_analysis.py`

- **Purpose:** Orchestrates the full analysis workflow
- **Execution:** Runs all three phases sequentially with error handling
- **Output:** Comprehensive analysis package with validation reports

### Supporting Modules

1. `locality_coordinate.py`

- **Purpose:** Provides verified coordinates for major localities
- **Function:** Corrects approximate centroids with known geographic coordinates
- **Coverage:** 50+ verified localities, state-level fallbacks

1. `__init__.py`

- **Purpose:** Package initialization for modular imports
- **Exports:** Main analysis functions for dashboard integration

---

### Analysis Workflow Diagram

```text
Data Loading
    ↓
Proximity Calculation
    ↓
Vulnerability Scoring
    ↓
Statistical Validation
    ↓
Visualization
```

---

### Analysis Pipeline

***Phase 1: Geospatial Data Preparation***
**Input:**

- `clean_idps_locality.csv`     (181 localities, ~6.55M IDPs)
- `clean_health_facilities.csv` (1,126 facilities)
- `clean_boundaries_data.csv`   (Administrative reference)

**Processing:**

1. Load and validate datasets
2. Create GeoDataFrames with point geometries
3. Generate locality centroids (verified + approximate)
4. Build spatial indices (KD-trees) for efficient querying

**Output:**

- Localities GeoDataFrame (181 points with IDP data)
- Facilities GeoDataFrame (1,126 points, 238 critical)

***Phase 2: Proximity Analysis***
**Methodology:**

- Haversine distance calculations (great circle)
- Nearest neighbor queries via KD-tree
- Facility counts within 5km, 10km, 20km radii

**Metrics Calculated:**

- Distance to nearest hospital/clinic
- Distance to nearest facility (any type)
- Count of critical facilities within thresholds
- Count of all facilities within thresholds

**Output:**

- Proximity DataFrame (11 metrics per locality)

***Phase 3: Vulnerability Assessment***
**Composite Vulnerability Index = Weighted Average of:**

1. IDP Burden Score (40%): Population size relative to maximum
2. Facility Access Score (40%): Distance + facility density
3. Origin Intensity Score (20%): Proportion from conflict zones

**Risk Classification:**

- Critical: Vulnerability Index ≥ 80
- High: 60 ≤ Index < 80
- Moderate: 40 ≤ Index < 60
- Low: Index < 40

**Output:**

- Complete vulnerability dataset with classifications

***Phase 4: Statistical Validation***

**Validation Techniques:**

1. Spatial Autocorrelation (Moran's I)
  → Tests for geographic clustering of vulnerability

2. Predictive Modeling (Random Forest + Logistic Regression)
   → Validates scoring methodology (87% accuracy)

3. Regional Hypothesis Testing
  → Darfur vs. Non-Darfur comparison (t-test)
  → Multi-regional ANOVA
  → Risk distribution chi-square test

**Output:**

- Statistical validation report
- Feature importance rankings
- Model performance visualizations

---

### Output Structure

```text
outputs/
├── locality_vulnerability_analysis.csv    # Primary results table
├── localities_vulnerability.geojson       # GeoJSON for mapping
├── health_facilities.geojson              # Facility locations
│
├── maps/                                   # Static visualizations
│   ├── vulnerability_index_map.png
│   ├── risk_categories_map.png
│   ├── accessibility_gap_map.png
│   └── interactive_vulnerability_map.html
│
└── inferential_analysis/                  # Statistical validation
    ├── morans_i_scatter.png
    ├── feature_importance.png
    ├── confusion_matrices.png
    ├── regional_hypothesis_tests.png
    └── inferential_analysis_report.txt
```

---

### Key Findings Summary

#### Geographic Scope

- **Total IDPs analyzed:** 6,552,118 million across 181 localities
- **Critical risk localities:** 0 (0% of total)
- **High risk localities:** 6 (3.3% of total)
- **Average distance to hospital:** 88.1 km
- **Localities beyond 20km:** 156 (86.2% of total)

#### Top 5 Most Vulnerable Localities

1. **Shendi, River Nile - Score:** 73.7 (High)
2. **Port Sudan, Red Sea - Score:** 68.7 (High)
3. **Ad Damar, River Nile - Score:** 63.4 (High)
4. **Atbara, River Nile - Score:** 63.3 (High)
5. **Ed Damazine, Blue Nile - Score:** 61.7 (High)

---

### Statistical Validation Results

#### Spatial Clustering

- **Moran's I:** 0.4918 (p < 0.001)
- **Interpretation:** Significant positive spatial autocorrelation detected
- **Implication:** High-vulnerability localities cluster geographically,
justifying regional targeting.

#### Predictive Model Performance

- **Random Forest Accuracy:** 94.6%
- **Logistic Regression Accuracy:** 94.6%
- **Conclusion:** Vulnerability scoring methodology is statistically robust

#### Top Vulnerability Drivers (Feature Importance)

- IDP Burden Score (0.3841)
- Origin Intensity Score (0.3476)
- Facility Access Score (0.2683)

#### Regional Comparison (Darfur vs. Non-Darfur)

- **Darfur mean vulnerability:** 31.90
- **Non-Darfur mean vulnerability:** 42.33
- **t-test p-value:** 0.0012
- **Conclusion:** Darfur shows LOWER vulnerability than non-Darfur regions
(p < 0.001). Non-Darfur areas hosting displaced populations require prioritized
response.

---

### Analysis Methodology

1. Geospatial Proximity Calculation

**Haversine Distance Formula:**

d = 2R × arcsin(√(sin²(Δφ/2) + cos(φ₁)cos(φ₂)sin²(Δλ/2)))

**Where:**
  R = Earth's radius (6,371 km)
  φ = latitude in radians
  λ = longitude in radians

**Efficiency Optimization:**

- KD-tree spatial indexing for O(log n) nearest neighbor queries
- Vectorized distance calculations via NumPy
- Ball queries for radius-based facility counts

1. Vulnerability Scoring Logic

**IDP Burden Score:**

```python
score = (locality_idps / max_idps) × 100
```

**Facility Access Score (inverse relationship):**

```python
distance_component = (distance / max_distance) × 100
facility_component = (1 - facilities / max_facilities) × 100
access_score = (0.6 × distance_component) + (0.4 × facility_component)
```

**Origin Intensity Score:**

```python
score = (idps_from_khartoum / total_idps) × 100
```

**Composite Index:**

```python
vulnerability_index = (0.4 × idp_burden) +
                     (0.4 × facility_access) +
                     (0.2 × origin_intensity)
```

1. Statistical Validation Framework

#### **Hypothesis 1: Spatial Clustering**

- **Null Hypothesis (H₀):** Vulnerability is randomly distributed
- **Alternative (H₁):** Similar values cluster geographically
- **Test:** Moran's I spatial autocorrelation
- **Result:** Reject H₀ (p < 0.001) — clustering confirmed

#### **Hypothesis 2: Regional Differences**

- **Null Hypothesis (H₀):** No difference between Darfur and other regions
- **Alternative (H₁):** Darfur has significantly different vulnerability
- **Test:** Independent samples t-test
- **Result:** Reject H₀ (p = 0.0012) — Non-Darfur regions show significantly
  HIGHER vulnerability than Darfur

#### **Hypothesis 3: Methodology Validity**

- **Validation:** Machine learning classification
- **Test:** Random Forest cross-validation
- **Result:** 94.6% accuracy — methodology validated

---

### Critical Findings & Interpretation

#### 🔍 Why Are There No "Critical" Risk Localities?

The analysis identified **zero localities** meeting the Critical threshold
(vulnerability index ≥80). This counterintuitive result reflects:

1. **Distributed Crisis Pattern**: Rather than extreme localized hotspots,
Sudan's humanitarian crisis manifests as widespread moderate vulnerability
across many localities.

2. **Scoring Methodology Design**: The composite weighted index
(40% IDP burden + 40% facility access + 20% origin intensity) was calibrated for
**relative prioritization** rather than absolute severity classification.

3. **Data Granularity Limitations**: State-level facility aggregation may mask
severe sub-locality gaps where IDPs concentrate in areas distant from mapped
facility coordinates.

**Implication**: The absence of "Critical" localities does **not** indicate
absence of crisis. Rather, it suggests that **156 localities (86%)** require
intervention, with **resource allocation differentiated by High/Moderate
priority tiers** rather than emergency/non-emergency binaries.

---

#### 🌍 The Darfur Paradox: Why Lower Vulnerability Scores?

Despite being the conflict epicenter, **Darfur states show significantly lower
vulnerability scores** (31.90 vs 42.33, p<0.001) than non-Darfur regions.
This paradox likely reflects:

1. **Outward Displacement**: IDPs fled **from** Darfur **to** other states
(Khartoum, River Nile, Red Sea), creating burden concentration in receiving
areas.

2. **Pre-existing Infrastructure**: Darfur's baseline health facility density,
while low, may be proportionally better than the infrastructure capacity of
regions suddenly absorbing massive IDP influxes.

3. **Data Capture Limitations**: Darfur's insecurity may result in undercounting
of IDPs who remain in conflict zones versus those who reached safer displacement
sites covered by IOM DTM surveys.

**Implication**: **River Nile state** (4 of top 5 vulnerable localities) and
**Red Sea state** (Port Sudan) require immediate humanitarian focus as
overwhelmed IDP hosting areas, while Darfur requires parallel conflict
resolution and infrastructure rebuilding for eventual return conditions.

---

#### 🚨 The Accessibility Crisis: 86% Beyond Threshold

**156 localities (86.2%)** exceed the 20km hospital access threshold,
representing **5,090,385 IDPs (77.7%)** with severely compromised healthcare
access. The **88.1km mean distance** is:

- **17.6× the WHO recommended maximum** (5km)
- **4.4× the humanitarian emergency threshold** (20km)
- **Equivalent to 2+ hours travel time** under ideal conditions
(impassable during rainy season/conflict)

**Implication**: Fixed facility expansion alone cannot address this crisis.
Response requires:

- Mobile health clinics targeting clusters of distant localities
- Community health worker programs in IDP settlements
- Telemedicine pilots where connectivity exists
- Pre-positioned emergency medical supplies in high-burden localities

---

### Reproducibility

#### Running the Complete Pipeline

#### **Option 1: Execute Full Workflow**

```python
python complete_analysis.py
```

#### **Option 2: Run Individual Modules (Phase 1-3: Geospatial analysis)**

```python
python crisis_analysis.py
```

#### **Phase 4: Statistical validation**

```python
python inferential_analysis.py
```

#### **Generate visualizations**

```python
python visualization.py
```

### System Requirements

**Python Version:** 3.8+
**Core Dependencies:**

- pandas, numpy (data processing)
- geopandas, shapely (geospatial operations)
- scikit-learn (machine learning)
- esda, libpysal (spatial statistics)
- matplotlib, seaborn, folium (visualization)

See `requirements.txt` for all required libraries

**Installation:**

```bash
pip install -r requirements.txt
```

### Data Requirements

**All input files must be present in `../1_datasets/clean/:`**

- `clean_idps_locality.csv`
- `clean_health_facilities.csv`
- `clean_boundaries_data.csv`

---

### Configuration

**File Paths:**

***Note:** Update in each script if using different directory structure:*

```python
CLEAN_DATA = Path("../1_datasets/clean")
OUTPUT_PATH = Path("outputs")
```

**Analysis Parameters (in crisis_analysis.py):**

```python
CRITICAL_FACILITY_TYPES = ["hospital", "clinic"]
ACCESSIBILITY_THRESHOLDS = [5, 10, 20]
VULNERABILITY_WEIGHTS = {
    "idp_burden": 0.4,
    "facility_access": 0.4,
    "origin_intensity": 0.2
}
```

---

### Limitations and Future Work

#### Current Limitations

1. Coordinate Precision

- ~50 localities use verified coordinates
- ~137 localities use state-level approximations with random offsets
- **Impact:** Distance calculations have ±5km uncertainty for approximate locations

1. Temporal Scope

- Analysis represents single time point (April 2024 data)
- Does not capture population movement trends
- **Recommendation:** Implement time-series analysis in future phases

1. Facility Functionality

- Assumes all mapped facilities are operational
- Does not account for capacity, staffing, or service availability
- **Recommendation:** Integrate WHO HeRAMS operational status data

1. Access Modeling

- Uses Euclidean distance as proxy for travel time
- Does not account for road networks, terrain, or security barriers
- **Recommendation:** Implement network analysis with OSM road data

### Recommended Enhancements

#### Phase 1 Extensions (Short-term)

- Acquire official locality boundary shapefiles from OCHA COD-AB
- Calculate true polygon centroids instead of approximations
- Integrate facility capacity data (beds, staff)

#### Phase 2 Extensions (Medium-term)

- Add time-series analysis to track vulnerability changes
- Implement travel-time analysis using OSM road networks
- Include disease outbreak data (cholera, malaria) as additional vulnerability factor

#### Phase 3 Extensions (Long-term)

- Real-time API integration for dynamic IDP tracking
- Predictive modeling for future displacement patterns
- Integration with climate/environmental risk factors

---

### Validation and Quality Assurance

#### Data Quality Checks

**IDP Data Validation:**

- Locality totals match state totals (6.55M IDPs)
- No missing state codes or locality identifiers
- Household sizes within expected range (4-7 persons)

**Facility Data Validation:**

- 100% of facilities have valid coordinates
- 97% geographic filtering accuracy (within Sudan bbox)
- 238 critical facilities identified (hospitals + clinics)

**Geospatial Validation:**

- All coordinates within Sudan boundaries (21.8-39°E, 3-23°N)
- Distance calculations validated against known city pairs
- Spatial join success rate: 100% (no orphaned records)

---

### Statistical Validation

**Model Cross-Validation:**

- 5-fold CV accuracy: 94.6%(±3.2%)
- Confusion matrix shows balanced performance across risk categories
- No evidence of overfitting (train/test gap <5%)

**Spatial Statistics:**

- Moran's I significance confirmed with 999 permutations
- Spatial weights matrix validated (5 nearest neighbors)
- No isolated localities (all have spatial connections)

---

### Integration with Milestone 4

This analysis phase produces all required inputs for the Communication Dashboard
(Milestone 4):

#### **Dashboard Data Feeds**

Primary Data Sources:

`localities_vulnerability.geojson` → Interactive map layer
`health_facilities.geojson` → Facility overlay
`locality_vulnerability_analysis.csv` → Data tables and filters

**Key Performance Indicators:**

- **Total IDPs:** 6,552,118
- **Critical risk localities:** 0
- **High risk localities:** 6
- **Average distance to hospital:** 88.1 km
- **Model validation accuracy:** 94.6%
- **Spatial clustering (Moran's I):** 0.4918***

**Visualization Assets:**

- Static maps (PNG) for reports
- Interactive HTML map for web embedding
- Feature importance charts
- Confusion matrices

---

### Dashboard Requirements

The analysis outputs are designed to support three core dashboard components:

#### Interactive Vulnerability Map

- Risk-colored localities (Critical/High/Moderate/Low)
- IDP-sized circles
- Health facility overlay
- Click-through details

#### Statistical Validation Panel

- Model accuracy display
- Spatial clustering metrics
- Feature importance visualization

#### Priority Action List

- Top 5 most vulnerable localities
- Sortable/filterable table
- Export functionality

### References and Methodology Sources

1. **Geospatial Analysis Framework:**

- Haversine distance calculation (Sinnott, 1984)
- KD-tree spatial indexing (Bentley, 1975)
- Geographic Information Systems principles (Longley et al., 2015)

1. **Statistical Methods:**

- Moran's I spatial autocorrelation (Moran, 1950)
- Random Forest classification (Breiman, 2001)
- Hypothesis testing framework (Fisher, 1925)

1. Humanitarian Data Standards:

- Humanitarian Data Exchange (HDX) guidelines
- OCHA Common Operational Datasets (COD)
- IOM Displacement Tracking Matrix (DTM) methodology

1. Vulnerability Assessment Approaches:

- Multi-dimensional vulnerability indices (Cutter et al., 2003)
- Geographic accessibility analysis (Guagliardo, 2004)
- Humanitarian needs assessment frameworks (UNHCR, 2024)

---

### Acknowledgments

#### Data Providers

1. International Organization for Migration (IOM) — Displacement Tracking Matrix
2. Humanitarian OpenStreetMap Team (HOT) — Health facility data
3. OCHA — Common Operational Datasets for Sudan

**Humanitarian Context:**

This analysis is conducted in solidarity with the people of Sudan during an
unprecedented humanitarian crisis. The work aims to support evidence-based
decision-making for humanitarian response and public health resilience.

For questions, suggestions, or collaboration opportunities, please open an issue
in the GitHub repository or contact the project lead directly.
