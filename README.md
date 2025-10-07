# Humanitarian Crisis Intelligence and Communication System (HCICS) 🇸🇩

## Project Overview

The **Humanitarian Crisis Intelligence and Communication System (HCICS)** is a
data-driven framework designed to address the catastrophic public health
information breakdown in **Sudan** following the ongoing conflict and
humanitarian crisis. The system’s core mission is to transform fragmented data
from disparate sources—such as humanitarian reports and geospatial
information—into **actionable intelligence** for public health decision-makers.
This is necessary because the crisis has created an unprecedented public health
emergency characterized by a devastated health system, mass displacement, and
significant disease outbreaks.

The project directly supports the Sudanese Federal Ministry of Health's need for
a tool that enables a shift from a reactive to an **adaptive posture** in
crisis response, thereby strengthening public health resilience.

## Minimum Viable Product (MVP) Objectives

As the graduation project for the MIT Emerging Talent Program, this repository
focuses on the development of a **Minimum Viable Product (MVP)**, which will
serve as a **proof-of-concept** for the full HCICS system. The MVP is designed
to establish the core data pipeline and a basic visualization platform.

| HCICS Component | Description & Key Functionality | Strategic Value for Public Health |
| :--- | :--- | :--- |
| **Data Aggregation Engine** | The foundation for collecting, cleaning, and **fusing** structured humanitarian and geospatial data (IOM DTM HOT OSM). It establishes API connections and performs initial data transformation. | Creates a **"single source of truth"** from multiple, unreliable, and fragmented data streams, addressing the challenge of data interoperability. |
| **Crisis Analysis Core (MVP Level)** | Applying **geospatial analysis** to combine the fused data. The core task is to calculate the spatial relationship between population centers (IDPs) and health services. | Identifies and visualizes **"maps of vulnerability"** by correlating locations of displaced populations with the availability of health facilities. |
| **Communication & Dissemination Platform** | A public-facing, web-based dashboard for visualizing key indicators. The MVP focuses on interactive maps and data visualization. | Translates complex data into easily digestible, **actionable insights** for resource allocation and public health awareness, moving from data collection to informed action. |

## Core Data Sources (MVP)

The MVP will integrate and analyze the following key open-source data streams:

* **IOM Displacement Tracking Matrix (DTM) Data**: Provides information on the
number, location, and movement of **internally displaced persons (IDPs)**.
This data is typically available via API.
* **Humanitarian OpenStreetMap Team (HOT) Data**: Provides geospatial data on
the locations and types of **health facilities** (e.g., 'hospital', 'clinic').

## Technology Stack (Anticipated)

| Category | Tools & Libraries |
| :--- | :--- |
| **Data Processing** | Python, Pandas, ETL Scripts |
| **Geospatial Analysis** | Python (e.g., GeoPandas, Folium, Shapely) |
| **Visualization/Dashboard** | Streamlit or Dash (for interactive web presentation) |
| **Version Control** | Git, GitHub |

---

## Project Milestones and Timeline

This project is aligned with the MIT ET Program's **Capstone Project
Deliverables** (ELO2 Track 2), following the standard CDSP milestone structure.
All milestones are expected to be completed and tagged in this repository.

| Milestone | Description | Due Date |
| :---: | :--- | :---: |
| **0** | **Cross-Cultural Collaboration & Setup:** Covers frameworks of cross-cultural communication, design and innovation. As an individual, the key task is to **prepare the repository** and project board for open-source contribution. | **October 7th** |
| **1** | **Problem Identification:** Conduct the initial domain study (contextualizing the crisis) and **frame an actionable research question(s)** that can be answered within the project's constraints. | **October 21st** |
| **2** | **Data Collection:** Decide how to model the problem domain in data, determine relevant data (IOM DTM, HOT OSM), and then **collect, clean, document, and host the data set**. | **November 4th** |
| **3** | **Data Analysis:** Focus on finding the appropriate analysis techniques (Geospatial Analysis) for the question and data, and producing the **results from your analysis** along with a non-technical summary. | **November 18th** |
| **4** | **Communicating Results:** Translate findings into a clear message and **prepare a communication strategy and artifact(s)** (the MVP dashboard) to reach the defined target audience. | **December 2nd** |
| **5** | **Final Presentation:** Prepare a 2.5-minute presentation for the program, covering the communication artifact, project evolution, learnings, and next steps. | **TBD** |

---

## Ethical Framework and Data Governance

Given the sensitivity of working with humanitarian data concerning vulnerable
displaced populations, the HCICS is built on a strong ethical foundation.

* **Data Protection**: The system requires security measures to protect the
privacy of individuals. A **Data Protection Impact Assessment** would be
conducted to mitigate potential risks associated with data handling.
* **Bias and Misinterpretation**: The use of geospatial correlation and
open-source data can introduce biases. The design incorporates a
**human-in-the-loop validation process** to ensure analysis is robust and
recommendations are carefully considered before being acted upon.
* **Transparency and Accountability**: The HCICS is intended to operate with a
high degree of transparency to ensure the Ministry of Health and humanitarian
partners are accountable for data-driven decisions.

---

## Future Expansion (Post-MVP)

The HCICS is designed to be scalable. Future expansion phases will integrate the
features deferred from the MVP to build a national-scale solution:

* **Unstructured Data Analysis**: Integration of social media feeds for
**Natural Language Processing (NLP)**, sentiment analysis, and
**"rumor tracking"** to counter misinformation (the "infodemic").
* **Time-Series Analysis**: Tracking population movements and disease outbreaks
over time to identify trends and anticipate future resource needs.
