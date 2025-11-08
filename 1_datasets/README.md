# Datasets – Humanitarian Crisis Intelligence and Communication System (HCICS)

This folder contains the raw and derived source datasets used by the
Data Aggregation Engine of the Humanitarian Crisis Intelligence and
Communication System (HCICS). These datasets form the foundation of the
MVP’s data pipeline, establishing core intelligence on Internally Displaced
Persons (IDPs), administrative boundaries, and health facility locations
across Sudan.

Note: The files listed under the "Cleaned Files" section represent the final
standardized datasets used as inputs to the HCICS MVP analysis modules.

---

## Data Sources Summary

1. IDP Displacement Data
   - Topic: Internally Displaced Persons (IDPs) and movement trends
   - Source Organization: IOM DTM
   - MVP Baseline Date: April 29, 2024
   - Geographic Granularity: ADM1 (State) and ADM2 (Locality)
   - Data Type: Movement and Caseload

2. Administrative Boundaries
   - Topic: Official administrative divisions (State, Locality)
   - Source Organization: OCHA COD-AB
   - MVP Baseline Date: April 4, 2023
   - Geographic Granularity: ADM2 (Locality)
   - Data Type: Geospatial Look-up

3. Health Facilities
   - Topic: Geospatial point data of health infrastructure
   - Source Organization: HOT OSM
   - MVP Baseline Date: November 4, 2025
   - Geographic Granularity: Point Level (Latitude/Longitude)
   - Data Type: Infrastructure

All datasets are sourced from the [Humanitarian Data Exchange (HDX)](https://data.humdata.org).
Each source follows open-data licensing and humanitarian data sharing standards.

All raw data files were retrieved via the “download_url” field included in the
HDX metadata (CSV or JSON format) for each dataset. This ensures that the files
correspond exactly to the versions described by the metadata, even if the HDX
dataset pages are later updated.

---

## Detailed Dataset Inventory

### 1. IDP Displacement Data (IOM DTM)

- Source: Sudan Displacement Situation – IDPs
- [Sudan Displacement Data - IDPs [IOM DTM]](https://data.humdata.org/dataset/sudan-displacement-data-idps-iom-dtm)
- File Type: Excel (.xlsx) containing ADM0–ADM2 tabs
- Baseline Used: April 29, 2024
- Cleaned Files:
  - clean_idps_state.csv
  - clean_idps_locality.csv
- Purpose: Provides caseload data for displaced populations across
  Sudanese administrative levels.

---

### 2. Administrative Boundaries (OCHA COD-AB)

- Source: Sudan – Administrative Boundaries (COD-AB)
- [Sudan - Subnational Administrative Boundaries](https://data.humdata.org/dataset/cod-ab-sdn)
- File Type: ESRI Shapefile bundle (.SHP, .SHX, .DBF, .PRJ, .CPG)
- Baseline Used: April 4, 2023
- Cleaned Files:
  - clean_boundaries_data.csv
  - lookup_localities.csv
  - lookup_states.csv
  - boundaries_state_summary.csv
- Purpose: Provides standardized ADM1 and ADM2 geospatial layers used
  as lookup references and aggregation units.

---

### 3. Health Facilities (HOT OSM)

- Source: Sudan Health Facilities (OpenStreetMap Export)
- [Sudan Health Facilities (OpenStreetMap Export)](https://data.humdata.org/dataset/hotosm_sdn_health_facilities)
- File Type: ESRI Shapefile bundle (.SHP, .SHX, .DBF, .PRJ, .CPG)
- Baseline Used: November 4, 2025
- Cleaned Files:
  - clean_health_facilities.csv
  - facilities_summary.csv
- Purpose: Contains latitude and longitude point data for hospitals,
  clinics, and health posts.

---

## Data Flow and Integration

- **Data Aggregation Engine**
  Input: All cleaned datasets
  Role: Fuses IDP, boundary, and facility data for unified geospatial modeling

- **Crisis Analysis Core**
  Input: IDPs, boundaries, and health facilities
  Role: Generates vulnerability overlays and hotspot analyses

- **Communication Dashboard**
  Input: Summary CSVs
  Role: Feeds the Streamlit dashboard for visualization and communication

---

## Data Consistency and Ethical Considerations

- Datasets reflect static, point-in-time conditions for MVP validation.
- The IDP and boundary data do not capture live updates or recent
  territorial changes.
- All datasets are openly licensed and contain no personally identifiable
  information (PII).
- The HCICS adheres to humanitarian data ethics, emphasizing:
  - Responsible data sharing
  - Transparency of methodology
  - Avoidance of data misuse or misrepresentation

---

## Related Documentation

- [guide.md](./guide.md): Describes dataset cleaning, transformation, and
  schema mapping.
- [../2_data_preparation/](../2_data_preparation/): Contains Python ETL
  scripts used for data processing and geospatial integration.
- [../README.md](../README.md): Project-level overview, MVP components,
  and methodology.

---

**Author:** Abdulrahman Sirelkhatim

**Program:** MIT Emerging Talent – Capstone Project (ELO2 Track 2)

**Last Updated:** November 7, 2025
