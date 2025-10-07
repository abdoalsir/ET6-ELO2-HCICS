# Constraints

Some boundaries around the **Humanitarian Crisis Intelligence and Communication
System (HCICS)** project.

---

## External

Constraints coming from outside factors that I have no direct control over:

- **Project Deadlines:**
  The project must follow the official **MIT Emerging Talent Capstone timeline**
  (September–December 2025), with all milestones completed and tagged according
  to the ELO2 structure.

- **Data Availability and Reliability:**
  The project relies on **open-source humanitarian datasets** (IOM DTM, HOT OSM)
  that may have **delays, missing values, or irregular updates** due to
  communication breakdowns in Sudan.

- **Connectivity and Power Stability:**
  Internet and power interruptions can affect real-time data pulls, software
  updates, and cloud synchronization.
  The MVP must therefore function offline or semi-offline when necessary.

- **Ethical and Legal Standards:**
  The use of humanitarian data is governed by international standards on
  **privacy, data protection, and informed consent**.
  These external guidelines limit how data can be stored, shared, or visualized.

---

## Internal: Involuntary

Constraints arising from factors within my individual situation that I cannot
change:

- **Time Availability:**
  I can dedicate approximately **20 hours per week**, divided into
  **3 hours daily**, excluding weekends and Thursday evenings (GMT 6:00).

- **Skill Development Curve:**
  While I have strong foundations in Python and data analysis, I am still
  consolidating advanced skills in **geospatial analysis** and
  **interactive dashboard development**.
  This may limit the technical complexity of the MVP during the program
  timeline.

---

## Internal: Voluntary

Constraints I have chosen to adopt to ensure project focus, clarity, and
quality:

- **MVP Scope Definition:**
  Limit the project to two essential modules for the proof-of-concept:
  1. **Data Aggregation Engine** (IOM DTM + HOT OSM integration)
  2. **Basic Geospatial Dashboard** for visualization.
  Post-MVP features such as **NLP-based rumor tracking** and **time-series
  forecasting** will be deferred to later phases.

- **Coding Standards:**
  Follow clean coding practices with tools such as **Black** and **Ruff** for
  formatting and linting.
  Use clear docstrings, modular scripts, and maintain full reproducibility for
  data processing.

- **Documentation and Transparency:**
  Keep all progress, milestone notes, and deliverables public in the GitHub
  repository to demonstrate version control, iterative learning, and ethical
  transparency.

- **Ethical Commitment:**
  No personally identifiable information (PII) will be used or shared.
  A **Data Protection Impact Assessment (DPIA)** will be planned post-MVP to
  guide the system’s ethical expansion.

---
