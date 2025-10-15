# Crisis Geoanalytics

## I. Contextualizing the Public Health Crisis in Sudan

### A. The Current State of Health and Humanitarian Needs

The ongoing conflict and humanitarian crisis in Sudan have created an
unprecedented public health emergency, characterized by a devastated health
system, mass displacement of populations, and a significant burden of disease
outbreaks. The scale and complexity of the crisis require a data-driven approach
to inform an effective and resilient response. [1]

The humanitarian situation is dire: over **40 % of the population —
approximately 20.3 million people — require urgent health assistance**. [1]
The conflict has produced the **world’s largest internally displaced
population**, with **nearly 11.1 million people displaced since April 2023**
and an additional **2.1 million refugees across borders**. [2] This massive and
ongoing movement of people places an immense strain on Sudan’s already fragile
health infrastructure.

According to WHO and UNICEF situation analyses, a substantial portion of the
health system is non-functional: **38 % of hospitals are completely out of
service** and another **62 % are only partially functional**. [1] Attacks on
healthcare have been recorded, with more than 150 verified incidents causing
hundreds of casualties among health workers and patients. [1] Millions are left
without access to essential care, including an estimated **2.5 million displaced
women and girls in Darfur** who lack access to reproductive-health services. [1]

The collapse of the health system and the scale of displacement have produced
multiple, overlapping public-health threats:

- **Vector- and communicable-disease outbreaks**, including malaria, dengue,
  and measles. [1]
- **Cholera:** > 18 000 reported cases and **535 associated deaths** across ten
  states. [3]
- **Acute malnutrition:** ~ 3.7 million people require nutrition interventions;
  surveys in > 30 localities report GAM rates above 15 %. [1]

This convergence of conflict, disease, and malnutrition illustrates a
**cascade of inter-linked failures**. Destruction of health facilities
exacerbates vulnerability among displaced populations, creating a
**geographic mismatch** between the areas of highest humanitarian need and the
locations of functional health facilities. A successful response must therefore
combine epidemiological surveillance with **spatial analytics** to understand
where populations are concentrated relative to remaining service capacity.
[1] [10] [17]

**Analytical framing.**
The intersection of displacement, infrastructure collapse, and disease burden
underscores the need for **data-driven humanitarian decision-making**.
Traditional emergency-response mechanisms are insufficient for a crisis of this
mobility and geographic complexity. Integrating geospatial and
population-mobility data provides an evidence base for anticipating needs,
optimizing resource distribution, and building adaptive public-health
resilience. [13][17]

---

### B. The Information Ecosystem and Communication Gaps

In a chaotic, volatile environment, collecting and disseminating accurate
information is a formidable challenge. Telecommunications outages and insecurity
often render traditional field assessments slow or unfeasible. [4] Humanitarian
organizations have adapted by deploying networks of field enumerators and key
informants. [5] While indispensable, these human networks introduce reporting
lag and bias, making complementary data streams essential.

Key elements of the current information ecosystem include:

- **Displacement and population-mobility data:** IOM’s Displacement Tracking
  Matrix (DTM) provides structured, publicly accessible data on IDP numbers,
  locations, and movements — an essential quantitative layer for situational
  awareness. [5] [6] [7]
- **Health-infrastructure data:** Humanitarian OpenStreetMap Team (HOT)
  exports supply open geospatial data on the locations and attributes of
  health facilities, forming the spatial backbone for accessibility mapping.
  [10] [16]
- **Epidemiological and nutrition indicators:** WHO and UNICEF datasets track
  outbreak and malnutrition trends, supporting prioritization of interventions.
  [2] [6]
- **Open-source intelligence (OSINT):** Satellite imagery and verified
  social-media data can corroborate ground reports and fill temporal gaps in
  official data. [4] [11]

However, fragmentation among these sources impedes timely synthesis. Moreover,
Sudan’s information environment is affected by an **infodemic** — the rapid
spread of misinformation that undermines public-health interventions such as
vaccination campaigns. [8] [9] [11] Effective crisis-response frameworks must
therefore manage both **data integrity** and **information integrity**, pairing
technical analytics with rumor-tracking and prebunking strategies.

**Expanded data-ecosystem context.**
No single dataset provides a complete picture of Sudan’s humanitarian crisis.
The fusion of structured humanitarian data (e.g., IOM DTM, HOT OSM) with
complementary feeds (WHO, UNICEF, OSINT) enables a **multi-modal intelligence
approach** that captures both quantitative indicators and qualitative human
narratives. This integrative strategy is central to the design philosophy of
the Humanitarian Crisis Intelligence and Communication System (HCICS), ensuring
that fragmented data becomes actionable, verified insight. [4] [6] [10] [16]

---

### Actionable Research Question (MVP Scope)

**Can geospatial analysis of available, structured humanitarian data (IOM DTM
and HOT OSM) effectively and efficiently identify and visualize the critical
gaps and geographic mismatches between the location of internally displaced
persons (IDPs) and the proximity of functional health facilities in Sudan?**
[10] [15]

This Minimum Viable Product (MVP) leverages the two most reliable and accessible
datasets to produce a **“Map of Vulnerability”** for strategic resource
allocation — providing the highest-impact, time-sensitive output within the
project’s limited timeframe. [1] [10] [15]

**Link to the broader HCICS vision.**
While this MVP addresses a specific analytical objective, it represents the
**technical foundation** of a scalable national system. In later phases, the
HCICS will extend this prototype to integrate additional humanitarian,
epidemiological, and open-source feeds, creating a
**real-time crisis-intelligence platform** that supports adaptive
decision-making by the Ministry of Health. This approach aligns with global
best practices for digital-health resilience and data governance.
[12] [13] [14] [15] [17]

---

### C. Core Data Sources (MVP Focus)

The HCICS MVP integrates the following open-source datasets:

1. **IOM Displacement Tracking Matrix (DTM)**
   - **Relevance:** Quantifies displaced populations, their locations, and
     mobility patterns — critical for mapping humanitarian demand and
     anticipating shifts. [6] [5] [7]

2. **Humanitarian OpenStreetMap Team (HOT) Health-Facility Data**
   - **Relevance:** Provides geocoded locations and facility types (e.g.,
     hospital, clinic), forming the supply-side layer for spatial accessibility
     analysis. [10] [16]

Supplementary sources (WHO cholera data [3], UNICEF nutrition reports [2],
validated OSINT feeds [4] [11]) can enrich analysis and strengthen real-time
situational awareness.

---

### Core Methodology (MVP)

The MVP’s analytical workflow emphasizes **data fusion + geospatial analysis**:

1. **Ingestion & Cleaning:** Extract IOM DTM and HOT OSM datasets
   (GeoJSON/Shapefiles); clean, geocode, and harmonize key attributes. [5] [10]
2. **Integration:** Join population- and facility-level data to a unified
   spatial database; compute proximity and coverage metrics. [10] [15]
3. **Visualization:** Generate an interactive “Map of Vulnerability” and
   dashboards highlighting critical gaps between IDPs and functional health
   facilities. [15]
4. **Scalability:** Prepare the architecture for integration of additional data
   feeds (e.g., WHO, OSINT) in future HCICS phases. [6] [12] [14] [17]

The result is a reproducible, modular geospatial framework capable of guiding
immediate humanitarian response while serving as the foundational layer of the
national HCICS platform. [13] [15] [17]

---

### References and Sources

1. [**Sudan: a deepening health crisis that calls for urgent attention**
– WHO EMRO][1] — accessed on September 21, 2025.
2. [**Humanitarian Situation Report No. 20** – UNICEF][2]
— accessed on September 21, 2025.
3. [**Humanitarian Situation Report No. 23** – UNICEF][3]
— accessed on September 21, 2025.
4. [**Yale public health researchers use social media posts and satellite images
to corroborate human rights atrocities in Sudan** – Yale Daily News][4]
— accessed on September 21, 2025.
5. [**Sudan | Displacement Tracking Matrix** – IOM][5] — accessed on September
21, 2025.
6. [**Data – Sudan** – ReliefWeb Response][6] — accessed on September 21, 2025.
7. [**Sudan Displacement Data – IDPs [IOM DTM] Humanitarian Dataset (HDX)**][7]
— accessed on September 21, 2025.
8. [**Rumour tracking | UNHCR Information Integrity Toolkit**][8]
— accessed on September 21, 2025.
9. [**Public Health & Crisis Communications Resource Hub** – ASTHO][9]
— accessed on September 21, 2025.
10. [**Sudan Health Facilities (OpenStreetMap Export)**
– Humanitarian Data Exchange (HOT OSM)][10] — accessed on September 21, 2025.
11. [**Manual: Rumor Tracking Tools** – IFRC Digital Transformation][11]
— accessed on September 21, 2025.
12. [**Digital health intervention reconnects war-affected people living with
HIV to healthcare: Ukraine case study** – *Oxford Academic*][12]
— accessed on September 21, 2025.
13. [**Health Data Governance for the Digital Age** – OECD][13]
— accessed on September 21, 2025.
14. [**Artificial intelligence in public health: promises, challenges, and an
agenda for policy makers and public health institutions** – *PMC*][14]
— accessed on September 21, 2025.
15. [**Visual communication of public health data: a scoping review**
– *Frontiers in Digital Health*][15] — accessed on September 21, 2025.
16. [**Humanitarian OSM Team** – OpenStreetMap Wiki][16]
— accessed on September 21, 2025.
17. [**Data Governance in Health** – World Bank Documents and Reports][17]
— accessed on September 21, 2025.

[1]: https://www.emro.who.int/sdn/sudan-news/sudan-a-deepening-health-crisis-that-calls-for-urgent-attention.html
[2]: https://www.unicef.org/media/159806/file/Sudan-Humanitarian-SitRep-Mid-Year-2024.pdf
[3]: https://www.unicef.org/media/164906/file/Sudan-Humanitrian-SitRep-September-2024.pdf
[4]: https://yaledailynews.com/blog/2023/09/18/absolutely-harrowing-yale-public-health-researchers-use-social-media-posts-and-satellite-images-to-corroborate-human-rights-atrocities-in-sudan
[5]: https://dtm.iom.int/sudan
[6]: https://response.reliefweb.int/sudan/data?page=2
[7]: https://data.humdata.org/dataset/sudan-displacement-data-idps-iom-dtm
[8]: https://www.unhcr.org/handbooks/informationintegrity/practical-tools/response-strategies/community-based-approaches/rumour-tracking
[9]: https://www.astho.org/topic/crisis-communications/
[10]: https://data.humdata.org/dataset/hotosm_sdn_health_facilities
[11]: https://digital.ifrc.org/sites/default/files/media/document/2023-04/manual_rumortrackingtools_0.pdf
[12]: https://academic.oup.com/oodh/article/doi/10.1093/oodh/oqaf001/7945619
[13]: https://www.oecd.org/en/publications/health-data-governance-for-the-digital-age_68b60796-en.html
[14]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12040707/
[15]: https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2025.1555231/full
[16]: https://wiki.openstreetmap.org/wiki/Humanitarian_OSM_Team
[17]: https://documents.worldbank.org/en/publication/documents-reports/documentdetail/099081723223522777
