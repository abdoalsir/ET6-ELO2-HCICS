# Communication Strategy: Sudan IDP Crisis Analysis

This directory outlines the strategic framework for disseminating findings from
the **Humanitarian Crisis Intelligence & Communication System (HCICS)**.

The strategy bridges the gap between complex geospatial analysis and actionable
humanitarian response, ensuring insights reach decision-makers, field
coordinators, and technical partners.

## 🎯 Strategic Objectives

**1. Inform Response Planning**
Provide evidence-based metrics to prioritize aid allocation. Our analysis
specifically highlights the counter-intuitive vulnerability concentrations in
River Nile and Red Sea states, shifting focus from historical assumptions.

**2. Highlight Accessibility Gaps**
Draw immediate attention to the critical finding that 86% of localities exceed
the WHO maximum distance to health facilities, necessitating mobile health
interventions rather than static infrastructure.

**3. Validate Methodology**
Demonstrate statistical rigor (94.6% accuracy) to build trust. By publishing
our validation metrics (Moran's I, Confusion Matrices), we ensure stakeholders
trust the "Black Box" of machine learning.

**4. Modular Scalability**
Establish a communication architecture that can grow. As we integrate future
modules (APIs, NLP rumor tracking), the communication of these findings remains
organized and distinct.

## 📢 Target Audiences & Key Messages

### Humanitarian Coordinators (OCHA, IOM)

* **Interest:** Resource allocation and high-level strategy.
* **Message:** "River Nile hosts the highest vulnerability concentrations;
    156 localities require mobile health interventions."
* **Format:** Executive Summary, Dashboard KPI Section.

### Field Operations Managers

* **Interest:** Logistics, security, and site planning.
* **Message:** "Specific localities have zero facility access within 20km."
* **Format:** Interactive Map, Top 5 Localities CSV Export.

### Data Scientists & Technical Partners

* **Interest:** Methodology, reproducibility, and code quality.
* **Message:** "Random Forest validation confirms the predictive power of
    origin intensity and facility density."
* **Format:** Statistical Validation Report, GitHub Repository Structure.

## 💻 Core Technology Stack

This project leverages a modern, open-source geospatial and data
science stack to produce actionable intelligence:

* **Dashboard Framework:** **Streamlit** is used for rapid application
    development, turning Python scripts into interactive web apps.
* **Geospatial Visualization:** **Folium** (interactive maps) and
    **GeoPandas** (spatial data manipulation) handle the mapping.
* **Data Analysis:** **Pandas** and **NumPy** are used for data cleaning.
    The predictive modeling relies on **Scikit-learn** and specialized
    statistical libraries.
* **Charting:** **Plotly** is employed for generating static and
    interactive visualizations (feature importance, regional comparison).
* **CI/CD & Code Quality:** **GitHub Actions** manage the continuous
    integration workflow, utilizing **ls-lint** for file naming and
    **markdownlint** for documentation quality.

## 🛠️ Communication Artefacts & Architecture

This project uses a modular design to ensure maintainability and scalability.
Instead of a monolithic application, communication assets are distributed across
specialized components.

### 1. The Interactive Dashboard (Core Tool)

The dashboard is the primary interface for all stakeholders. It is architected
into distinct modules to allow for future expansion (e.g., adding NLP tabs
without breaking the map logic).

* **`app.py`**: The orchestration layer. It manages the flow of the story
    but delegates heavy lifting to specialized modules.
* **`dashboard_functions.py`**: Contains the logic for visualizations. By
    keeping this separate, we can update chart styles or add new plots (like
    future NLP sentiment analysis) without touching the main layout.
* **`dashboard_layout.py`**: Manages the UI/UX. This separation allows us
    to rebrand or theme the application for different partners without altering
    analytical code.
* **`config.py`**: Centralizes data paths and settings. This ensures that
    as data sources update (e.g., moving from static CSVs to live APIs), the
    change only needs to happen in one place.

### 2. Statistical Reports

Generated in `4_data_analysis/outputs/inferential_analysis/`.

* **Text Reports:** Detailed breakdowns of Moran's I and ML validation.
* **Static Visuals:** Confusion matrices and feature importance plots are
    saved as images to be embedded in offline PDF reports or emails.

### 3. Visual Assets

Located in `assets/` and `outputs/`.

* **Vulnerability Map:** High-resolution PNGs for slide decks.
* **Regional Comparison:** Box plots illustrating the "Darfur Paradox."

## 🚀 Future Roadmap & Expansion

This MVP lays the groundwork for advanced communication features:

* **API Integration:** The modular `config.py` is ready to switch from local
    file loading to fetching live IOM displacement data via API.
* **NLP Rumor Tracking:** A future module can be plugged into `app.py` to
    visualize social media sentiment regarding health access, cross-referencing
    it with our geospatial vulnerability data.
* **Automated Alerts:** Using the `dashboard_functions.py` logic to trigger
    email alerts when specific localities cross vulnerability thresholds.

## 🔄 Feedback Loop

To ensure the strategy remains effective, we solicit feedback via:

* **Dashboard Metrics:** Tracking usage of specific tabs (Map vs. Methodology).
* **GitHub Issues:** For bug reports and feature requests from technical users.
* **Direct Engagement:** Regular reviews with humanitarian partners to refine
    vulnerability indicators.
