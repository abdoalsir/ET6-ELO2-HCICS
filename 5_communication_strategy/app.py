"""
The main entry point for the HCICS Dashboard application.

Module contents:
    - main: The primary execution function that orchestrates the dashboard layout,
      data loading, and visualization rendering sequence.

Orchestrates the integration of layout components, data configuration, and
analytical functions to produce the interactive Streamlit interface.

Created on 05-11-25
@author: Abdulrahman Sirelkhatim
"""

import streamlit as st

from dashboard_layout import (
    setup_page,
    render_header,
    render_sidebar,
    render_footer,
    create_anchor,
)

from dashboard_functions import (
    render_kpis,
    create_vulnerability_map,
    render_top_vulnerable_table,
    render_feature_importance,
    render_regional_comparison,
    render_statistical_validation,
    render_methodology,
    render_download_center,
)

from config import (
    load_geojson_data,
    load_csv_data,
)

from streamlit_folium import st_folium


def main():
    """
    Main application entry point that drives the dashboard execution flow.

    Steps:
        1. Initializes the page configuration and applies global styles.
        2. Renders the static structural elements (header and sidebar).
        3. Loads and validates geospatial (GeoJSON) and analytical (CSV) datasets.
        4. Handles data loading errors with user-friendly error messages.
        5. Sequentially renders dashboard sections:
            - Executive Summary
            - Key Performance Indicators (KPIs)
            - Interactive Vulnerability Map
            - Top 5 Vulnerable Localities Table
            - Feature Importance Analysis
            - Regional Comparisons (Darfur vs Non-Darfur)
            - Statistical Validation
            - Methodology Documentation
            - Download Center
        6. Renders the application footer.

    Returns:
        None
    """

    setup_page()
    render_header()
    render_sidebar()

    with st.spinner("🔄 Loading geospatial data..."):
        localities_gdf, facilities_gdf = load_geojson_data()
        analysis_df = load_csv_data()

    if localities_gdf is None or facilities_gdf is None or analysis_df is None:
        st.error("""
        ❌ **Data Loading Failed**

        Unable to load required data files. Please ensure:
        - `locality_vulnerability_analysis.csv` exists in outputs/
        - `localities_vulnerability.geojson` exists in outputs/
        - `health_facilities.geojson` exists in outputs/

        Run the data analysis scripts before launching the dashboard.
        """)
        st.stop()

    create_anchor("overview")

    st.markdown(
        """
    <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
                padding: 2rem; border-radius: 12px; border-left: 5px solid #3b82f6; margin-bottom: 2rem;">
        <h2 style="color: #1e40af; margin-top: 0;">📋 Executive Summary</h2>
        <p style="color: #475569; font-size: 1.05rem; line-height: 1.7; margin-bottom: 0;">
            This dashboard presents a comprehensive geospatial analysis of <strong>internally displaced person (IDP)
            vulnerability</strong> across Sudan's humanitarian crisis. Using machine learning and spatial statistics,
            we assessed <strong>181 localities</strong> hosting <strong>6.55 million IDPs</strong> based on population
            burden, healthcare facility access, and displacement patterns. The analysis identifies priority intervention
            areas and reveals critical accessibility gaps requiring immediate humanitarian response.
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    create_anchor("key-indicators")
    render_kpis(analysis_df)

    st.markdown("<br>", unsafe_allow_html=True)

    create_anchor("vulnerability-map")
    st.markdown(
        '<h2 class="section-header">🗺️ Interactive Vulnerability Map</h2>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="background-color: #f0f9ff; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #0284c7;">
        <strong>🧭 Map Guide:</strong> Click on localities for detailed vulnerability metrics.
        Use layer controls (top-right) to toggle facilities on/off. Circle size indicates IDP population;
        color indicates risk level.
    </div>
    """,
        unsafe_allow_html=True,
    )

    vulnerability_map = create_vulnerability_map(localities_gdf, facilities_gdf)

    st_folium(
        vulnerability_map,
        width=None,
        height=700,
        returned_objects=[],
    )

    st.markdown("<br>", unsafe_allow_html=True)

    create_anchor("top-5-localities")
    render_top_vulnerable_table(analysis_df)

    st.markdown("<br>", unsafe_allow_html=True)

    create_anchor("vulnerability-drivers")
    render_feature_importance()

    st.markdown("<br>", unsafe_allow_html=True)

    create_anchor("regional-comparison")
    render_regional_comparison(analysis_df)

    st.markdown("<br>", unsafe_allow_html=True)

    create_anchor("statistical-validation")
    render_statistical_validation()

    st.markdown("<br>", unsafe_allow_html=True)

    create_anchor("methodology")
    render_methodology()

    st.markdown("<br>", unsafe_allow_html=True)

    create_anchor("downloads")
    render_download_center()

    st.markdown("<br><br>", unsafe_allow_html=True)

    render_footer()


if __name__ == "__main__":
    main()
