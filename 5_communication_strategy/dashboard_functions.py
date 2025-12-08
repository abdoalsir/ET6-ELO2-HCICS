"""
Core visualization and rendering logic for the dashboard components.

Module contents:
    - render_kpis: Displays high-level metrics and aggregate statistics.
    - create_vulnerability_map: Generates the interactive Folium map.
    - render_top_vulnerable_table: Creates the styled dataframe of priority areas.
    - render_feature_importance: Plots the machine learning feature importance chart.
    - render_regional_comparison: Visualizes the Darfur vs. Non-Darfur statistical gap.
    - render_statistical_validation: Displays statistical proofs (Moran's I, confusion matrices).
    - render_methodology: Renders expandable documentation sections.
    - render_download_center: Provides file download functionality.

Created on 05-11-25
@author: Abdulrahman Sirelkhatim
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import folium
import plotly.graph_objects as go
from config import RISK_COLORS, OUTPUT_PATH, REPO_ROOT


def render_kpis(analysis_df):
    """
    Calculates and renders the top-level Key Performance Indicators (KPIs).

    Steps:
        1. Aggregates total IDP population from the dataset.
        2. Counts localities in 'Critical' and 'High' risk categories.
        3. Calculates the mean distance to the nearest hospital.
        4. Creates a 5-column layout.
        5. Displays metrics for Total IDPs, Critical Risk, High Risk, Avg Distance,
           and Model Accuracy with delta indicators.

    Args:
        analysis_df (pd.DataFrame): The dataset containing vulnerability analysis.
    """
    st.markdown(
        '<h2 class="section-header">📊 Key Performance Indicators</h2>',
        unsafe_allow_html=True,
    )

    total_idps = analysis_df["total_idps"].sum()
    critical_localities = len(analysis_df[analysis_df["risk_category"] == "Critical"])
    high_localities = len(analysis_df[analysis_df["risk_category"] == "High"])
    avg_distance = analysis_df["dist_to_nearest_hospital_km"].mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Total IDPs",
            value=f"{total_idps:,}",
            delta="6.55M Analyzed",
            help="Total internally displaced persons across all localities",
        )

    with col2:
        st.metric(
            label="Critical Risk",
            value=critical_localities,
            delta="0 Localities",
            help="Localities with vulnerability index ≥80",
        )

    with col3:
        st.metric(
            label="High Risk",
            value=high_localities,
            delta="3.3% of Total",
            help="Localities with vulnerability index 60-79",
        )

    with col4:
        st.metric(
            label="Avg Distance",
            value=f"{avg_distance:.1f} km",
            delta="17.6× WHO max",
            delta_color="inverse",
            help="Mean distance to nearest hospital/clinic",
        )

    with col5:
        st.metric(
            label="Model Accuracy",
            value="94.6%",
            delta="ML Validated",
            help="Random Forest classification accuracy",
        )


def create_vulnerability_map(localities_gdf, facilities_gdf):
    """
    Constructs an interactive geospatial visualization using Folium.

    Steps:
        1. Initializes a Folium map centered on Sudan.
        2. Injects a custom HTML title overlay.
        3. Iterates through localities to create CircleMarkers:
            - Size based on IDP population.
            - Color based on Risk Category.
            - Popup containing detailed metrics (Score, Distance, Hospitals).
        4. Iterates through facilities to create Marker icons (Hospitals/Clinics).
        5. Adds layer controls and a custom HTML legend.

    Args:
        localities_gdf (gpd.GeoDataFrame): Geospatial data for localities.
        facilities_gdf (gpd.GeoDataFrame): Geospatial data for health facilities.

    Returns:
        folium.Map: The configured interactive map object.
    """

    center_lat = 15.5
    center_lon = 32.5

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    title_html = """
    <div style="position: fixed;
                top: 10px; left: 50px; width: 500px; height: 90px;
                background-color: white; border: 2px solid grey; z-index: 9999;
                font-size: 14px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <h4 style="margin: 0 0 5px 0; color: #1e3a8a;">Sudan: IDP Vulnerability Analysis</h4>
        <p style="margin: 0; font-size: 12px; color: #6b7280;">
            Interactive map showing vulnerability by locality<br>
            <strong>Circle size</strong>: IDP population | <strong>Color</strong>: Risk category
        </p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    locality_layer = folium.FeatureGroup(name="Localities (Vulnerability)", show=True)
    facility_layer = folium.FeatureGroup(
        name="Critical Facilities (Hospitals/Clinics)", show=True
    )

    for idx, row in localities_gdf.iterrows():
        color = RISK_COLORS.get(row["risk_category"], "#gray")

        radius = max(3, row["total_idps"] / 10000)

        popup_html = f"""
        <div style="font-family: Arial; width: 250px;">
            <h4 style="margin: 0 0 10px 0; color: #1e3a8a;">{row["locality_name"]}</h4>
            <table style="width: 100%; font-size: 12px;">
                <tr><td><strong>State:</strong></td><td>{row["state_name"]}</td></tr>
                <tr><td><strong>Total IDPs:</strong></td><td>{row["total_idps"]:,}</td></tr>
                <tr style="background-color: #f3f4f6;">
                    <td><strong>Vulnerability Score:</strong></td>
                    <td><strong>{row["vulnerability_index"]:.1f}</strong></td>
                </tr>
                <tr><td><strong>Risk Category:</strong></td>
                    <td><span style="color: {color}; font-weight: bold;">{row["risk_category"]}</span></td>
                </tr>
                <tr style="background-color: #f3f4f6;">
                    <td><strong>Distance to Hospital:</strong></td>
                    <td>{row["dist_to_nearest_hospital_km"]:.1f} km</td>
                </tr>
                <tr><td><strong>Hospitals within 20km:</strong></td>
                    <td>{row["hospitals_within_20km"]}</td>
                </tr>
            </table>
        </div>
        """

        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=300),
            color="black",
            fillColor=color,
            fillOpacity=0.7,
            weight=1,
            tooltip=f"{row['locality_name']} ({row['risk_category']})",
        ).add_to(locality_layer)

    critical_facilities = facilities_gdf[
        facilities_gdf["facility_type_standard"].isin(["hospital", "clinic"])
    ]

    for idx, row in critical_facilities.iterrows():
        icon_color = "red" if row["facility_type_standard"] == "hospital" else "orange"
        icon = "plus-sign"

        popup_text = f"""
        <div style="font-family: Arial;">
            <h5 style="margin: 0 0 5px 0;">{row["facility_name_display"]}</h5>
            <p style="margin: 0; font-size: 12px;">
                <strong>Type:</strong> {row["facility_type_standard"].title()}<br>
            </p>
        </div>
        """

        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=folium.Popup(popup_text, max_width=250),
            icon=folium.Icon(color=icon_color, icon=icon, prefix="glyphicon"),
            tooltip=f"{row['facility_name_display']}",
        ).add_to(facility_layer)

    locality_layer.add_to(m)
    facility_layer.add_to(m)

    folium.LayerControl(position="topright").add_to(m)

    legend_html = f"""
    <div style="position: fixed;
                bottom: 50px; right: 50px; width: 220px;
                background-color: white; border: 2px solid grey; z-index: 9999;
                font-size: 12px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <p style="margin: 0 0 8px 0; font-weight: bold; font-size: 13px;">Risk Categories</p>
        <p style="margin: 3px 0;"><span style="color: {RISK_COLORS["Critical"]};">●</span> Critical (≥80)</p>
        <p style="margin: 3px 0;"><span style="color: {RISK_COLORS["High"]};">●</span> High (60-79)</p>
        <p style="margin: 3px 0;"><span style="color: {RISK_COLORS["Moderate"]};">●</span> Moderate (40-59)</p>
        <p style="margin: 3px 0;"><span style="color: {RISK_COLORS["Low"]};">●</span> Low (<40)</p>
        <hr style="margin: 8px 0;">
        <p style="margin: 0 0 8px 0; font-weight: bold; font-size: 13px;">Facilities</p>
        <p style="margin: 3px 0;"><span style="color: red;">📍</span> Hospital</p>
        <p style="margin: 3px 0;"><span style="color: orange;">📍</span> Clinic</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    return m


def render_top_vulnerable_table(analysis_df):
    """
    Renders a styled table of the top 5 most vulnerable localities.

    Steps:
        1. Filters and sorts the dataframe to find the top 5 by vulnerability index.
        2. Renames columns for presentation (UI-friendly names).
        3. Applies conditional formatting (color coding) to the Risk Category column.
        4. Displays the interactive dataframe.
        5. Generates a CSV download button for the filtered data.
        6. Displays context metrics (River Nile concentration and Avg Distance gap).

    Args:
        analysis_df (pd.DataFrame): The dataset containing vulnerability analysis.
    """

    st.markdown(
        '<h2 class="section-header">🚨 Top 5 Most Vulnerable Localities</h2>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="background-color: #fef2f2; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #dc2626;">
        <strong>⚠️ Priority Intervention Areas:</strong> These localities require immediate humanitarian focus based on IDP burden, facility access, and displacement patterns.
    </div>
    """,
        unsafe_allow_html=True,
    )

    top_5 = analysis_df.nlargest(5, "vulnerability_index")[
        [
            "locality_name",
            "state_name",
            "total_idps",
            "vulnerability_index",
            "risk_category",
            "dist_to_nearest_hospital_km",
        ]
    ].copy()

    top_5.columns = [
        "Locality",
        "State",
        "Total IDPs",
        "Vulnerability Score",
        "Risk Category",
        "Distance to Hospital (km)",
    ]

    top_5.insert(0, "Rank", range(1, 6))

    def color_risk_category(val):
        """Color code risk categories."""
        color_map = {
            "Critical": "background-color: #fee2e2; color: #991b1b; font-weight: bold",
            "High": "background-color: #fed7aa; color: #9a3412; font-weight: bold",
            "Moderate": "background-color: #fef3c7; color: #92400e; font-weight: bold",
            "Low": "background-color: #d1fae5; color: #065f46; font-weight: bold",
        }
        return color_map.get(val, "")

    styled_df = top_5.style.applymap(
        color_risk_category, subset=["Risk Category"]
    ).format(
        {
            "Total IDPs": "{:,.0f}",
            "Vulnerability Score": "{:.1f}",
            "Distance to Hospital (km)": "{:.1f}",
        }
    )

    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    csv = top_5.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Top 5 as CSV",
        data=csv,
        file_name="top_5_vulnerable_localities.csv",
        mime="text/csv",
    )

    col1, col2 = st.columns(2)

    with col1:
        river_nile_count = len(top_5[top_5["State"] == "River Nile"])
        st.metric(
            "River Nile Localities in Top 5",
            river_nile_count,
            help="River Nile state dominates vulnerability rankings",
        )

    with col2:
        avg_distance_top5 = top_5["Distance to Hospital (km)"].mean()
        st.metric(
            "Avg Distance (Top 5)",
            f"{avg_distance_top5:.1f} km",
            delta=f"{avg_distance_top5 - 88.1:.1f} km vs overall",
            delta_color="inverse",
        )


def render_feature_importance():
    """
    Visualizes the predictive drivers of vulnerability based on ML analysis.

    Steps:
        1. Defines the feature importance data (IDP Burden, Origin Intensity, Facility Access).
        2. Constructs a horizontal bar chart using Plotly Graph Objects.
        3. Customizes layout, colors, and hover templates.
        4. Renders the chart via Streamlit.
        5. detailed explanatory text blocks interpreting each feature's impact.
    """

    st.markdown(
        '<h2 class="section-header">📈 Vulnerability Drivers Analysis</h2>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background-color: #eff6ff; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #2563eb;">
            <strong>🔍 What Makes a Locality Vulnerable?</strong> Based on Random Forest machine learning analysis (94.6% accuracy), these factors predict vulnerability:
        </div>
    """,
        unsafe_allow_html=True,
    )

    features = {
        "Feature": [
            "IDP Burden Score",
            "Origin Intensity Score",
            "Facility Access Score",
        ],
        "Importance": [0.3841, 0.3476, 0.2683],
        "Description": [
            "Population size relative to maximum",
            "Proportion from conflict zones (Khartoum)",
            "Distance + facility density",
        ],
    }

    df_features = pd.DataFrame(features)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df_features["Importance"],
            y=df_features["Feature"],
            orientation="h",
            marker=dict(
                color=["#dc2626", "#ea580c", "#ca8a04"],
                line=dict(color="#1e293b", width=1),
            ),
            text=df_features["Importance"].apply(lambda x: f"{x:.4f}"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Importance: %{x:.4f}<br>%{customdata}<extra></extra>",
            customdata=df_features["Description"],
        )
    )

    fig.update_layout(
        title={
            "text": "Feature Importance for Vulnerability Prediction",
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 18, "color": "#1e3a8a", "family": "Arial Black"},
        },
        xaxis_title="Importance Score",
        yaxis_title="",
        height=350,
        template="plotly_white",
        margin=dict(l=20, r=100, t=60, b=40),
        font=dict(size=12),
    )

    fig.update_xaxes(range=[0, 0.45])

    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("""
            **IDP Burden (38.4%)**
            Larger displaced populations create greater strain on local resources.
        """)

    with col2:
        st.info("""
            **Origin Intensity (34.8%)**
            IDPs from conflict epicenter (Khartoum) indicate acute crisis displacement.
        """)

    with col3:
        st.info("""
            **Facility Access (26.8%)**
            Distance to hospitals and facility density affect healthcare access.
        """)


def render_regional_comparison(analysis_df):
    """
    Analyzes and visualizes the disparity between Darfur and Non-Darfur regions.

    Steps:
        1. Segments the data into Darfur and Non-Darfur subsets.
        2. Computes mean vulnerability indices for both groups.
        3. Creates a Plotly Box Plot to visualize the distribution comparison.
        4. Displays statistical metrics including the t-test p-value significance.
        5. Renders explanatory text regarding the "Darfur Paradox" (displacement dynamics).

    Args:
        analysis_df (pd.DataFrame): The dataset containing vulnerability analysis.
    """

    st.markdown(
        '<h2 class="section-header">🌍 Regional Comparison: The Darfur Paradox</h2>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background-color: #fefce8; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #eab308;">
            <strong>🔍 Counterintuitive Finding:</strong> Despite being the conflict epicenter, Darfur shows significantly <strong>lower</strong> vulnerability than non-Darfur regions (p < 0.001).
        </div>
    """,
        unsafe_allow_html=True,
    )

    darfur = analysis_df[analysis_df["state_name"].str.contains("Darfur", na=False)]
    non_darfur = analysis_df[
        ~analysis_df["state_name"].str.contains("Darfur", na=False)
    ]

    darfur_mean = darfur["vulnerability_index"].mean()
    non_darfur_mean = non_darfur["vulnerability_index"].mean()

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = go.Figure()

        fig.add_trace(
            go.Box(
                y=darfur["vulnerability_index"],
                name="Darfur",
                marker=dict(color="#dc2626"),
                boxmean="sd",
            )
        )

        fig.add_trace(
            go.Box(
                y=non_darfur["vulnerability_index"],
                name="Non-Darfur",
                marker=dict(color="#2563eb"),
                boxmean="sd",
            )
        )

        fig.update_layout(
            title={
                "text": "Vulnerability Distribution by Region",
                "x": 0.5,
                "xanchor": "center",
                "font": {"size": 16, "color": "#1e3a8a"},
            },
            yaxis_title="Vulnerability Index",
            height=400,
            template="plotly_white",
            showlegend=True,
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.metric(
            "Darfur Mean",
            f"{darfur_mean:.2f}",
            help=f"Based on {len(darfur)} localities",
        )

        st.metric(
            "Non-Darfur Mean",
            f"{non_darfur_mean:.2f}",
            delta=f"+{non_darfur_mean - darfur_mean:.2f}",
            delta_color="normal",
            help=f"Based on {len(non_darfur)} localities",
        )

        st.metric(
            "Statistical Test",
            "p < 0.001",
            help="Independent t-test p-value: highly significant difference",
        )

        st.metric(
            "Localities Sampled",
            f"Darfur: {len(darfur)}",
            delta=f"Non-Darfur: {len(non_darfur)}",
        )

    st.markdown("#### 💡 Why the Paradox?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.warning("""
            **Outward Displacement**
            IDPs fled FROM Darfur TO other states, creating burden concentration in receiving areas.
        """)

    with col2:
        st.warning("""
            **Infrastructure Capacity**
            Non-Darfur regions suddenly absorbed massive IDP influxes without proportional infrastructure.
        """)

    with col3:
        st.warning("""
            **Data Capture**
            Darfur's insecurity may result in undercounting IDPs in conflict zones vs. safer displacement sites.
        """)


def render_statistical_validation():
    """
    Displays the statistical rigor and validation metrics of the analysis.

    Steps:
        1. Renders top-level metrics for Moran's I, Random Forest Accuracy, and CV scores.
        2. Loads and displays static visualization images:
            - Moran's I Scatter Plot (Spatial Autocorrelation).
            - Feature Importance Chart.
            - Confusion Matrices.
        3. Provides error handling if validation images are missing.
        4. Renders interpretation text for spatial clustering and ML performance.
    """

    st.markdown(
        '<h2 class="section-header">✅ Statistical Validation</h2>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background-color: #f0fdf4; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #16a34a;">
            <strong>🔬 Methodology Validation:</strong> The vulnerability assessment methodology was rigorously tested using spatial statistics, machine learning, and hypothesis testing.
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Moran's I",
            "0.4918",
            delta="p < 0.001",
            help="Spatial autocorrelation: Significant geographic clustering detected",
        )

    with col2:
        st.metric(
            "Random Forest",
            "94.6%",
            delta="Accuracy",
            help="ML model accuracy in predicting risk categories",
        )

    with col3:
        st.metric(
            "Logistic Regression",
            "94.6%",
            delta="Accuracy",
            help="Baseline model performance",
        )

    with col4:
        st.metric(
            "Cross-Validation",
            "88.2%",
            delta="±10.4%",
            help="5-fold CV mean accuracy (Random Forest)",
        )

    st.markdown("---")

    st.markdown("#### 🌐 Spatial Autocorrelation Analysis")

    col1, col2 = st.columns([3, 2])

    with col1:
        morans_path = (
            REPO_ROOT
            / "4_data_analysis"
            / "outputs"
            / "inferential_analysis"
            / "morans_i_scatter.png"
        )

        if morans_path.exists():
            st.image(
                str(morans_path),
                caption="Moran's I Scatter Plot - Testing for Spatial Clustering",
                use_container_width=True,
            )
        else:
            st.warning(
                "⚠️ Moran's I visualization not found. Run inferential analysis to generate."
            )

    with col2:
        st.info("""
            **Finding:**
            Moran's I = 0.4918 (p < 0.001)

            **Interpretation:**
            Significant positive spatial autocorrelation detected. High-vulnerability localities cluster geographically.

            **Implication:**
            Regional targeting of humanitarian interventions is statistically justified.
        """)

    st.markdown("---")

    st.markdown("#### 🤖 Machine Learning Validation")

    col1, col2 = st.columns(2)

    with col1:
        feature_path = (
            REPO_ROOT
            / "4_data_analysis"
            / "outputs"
            / "inferential_analysis"
            / "feature_importance.png"
        )
        if feature_path.exists():
            st.image(
                str(feature_path),
                caption="Feature Importance Rankings",
                use_container_width=True,
            )
        else:
            st.warning("⚠️ Feature importance plot not found.")

    with col2:
        # Confusion Matrices
        confusion_path = (
            REPO_ROOT
            / "4_data_analysis"
            / "outputs"
            / "inferential_analysis"
            / "confusion_matrices.png"
        )

        if confusion_path.exists():
            st.image(
                str(confusion_path),
                caption="Model Performance: Confusion Matrices",
                use_container_width=True,
            )
        else:
            st.warning("⚠️ Confusion matrices not found.")

    st.success("""
        **✅ Validation Conclusion:**
        The vulnerability scoring methodology is statistically robust, achieving 94.6% accuracy in predicting risk categories.
        Both spatial analysis and machine learning confirm the validity of the geospatial approach.
    """)


def render_methodology():
    """
    Renders the comprehensive technical documentation in expandable sections.

    Steps:
        1. Creates expandable containers for:
            - Vulnerability Index Formula (mathematical breakdown).
            - Data Sources & Quality (dates, completeness, limitations).
            - Limitations & Assumptions (coordinate precision, operational status).
            - Analysis Workflow Diagram (step-by-step pipeline).
            - Critical Findings & Interpretation (contextual analysis).
        2. Renders formatted Markdown text within each expander.
    """

    st.markdown(
        '<h2 class="section-header">📚 Methodology & Documentation</h2>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="background-color: #f8fafc; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #64748b;">
            <strong>📖 Technical Documentation:</strong> Comprehensive explanation of the analytical framework, data sources, and limitations.
        </div>
    """,
        unsafe_allow_html=True,
    )

    with st.expander("🧮 **Vulnerability Index Formula**", expanded=False):
        st.markdown("""
            ### Composite Vulnerability Index

            The vulnerability score is calculated as a weighted average of three components:
```
            Vulnerability Index = (0.4 × IDP Burden) + (0.4 × Facility Access) + (0.2 × Origin Intensity)
```

            **Component Calculations:**

            1. **IDP Burden Score (40% weight)**
```
               score = (locality_idps / max_idps) × 100
```
               - Measures population pressure relative to the most burdened locality

            2. **Facility Access Score (40% weight)**
```
               distance_component = (distance / max_distance) × 100
               facility_component = (1 - facilities / max_facilities) × 100
               access_score = (0.6 × distance) + (0.4 × facility_count)
```
               - Combines distance to nearest hospital with facility density
               - Higher score = worse access (inverted scale)

            3. **Origin Intensity Score (20% weight)**
```
               score = (idps_from_khartoum / total_idps) × 100
```
               - Proportion displaced from conflict epicenter (Khartoum)
               - Indicates acute, conflict-driven displacement

            ### Risk Classification Thresholds

            | Risk Category | Vulnerability Index | Color Code |
            |---------------|---------------------|------------|
            | **Critical**  | ≥ 80               | 🔴 Red     |
            | **High**      | 60 - 79            | 🟠 Orange  |
            | **Moderate**  | 40 - 59            | 🟡 Yellow  |
            | **Low**       | < 40               | 🟢 Green   |
        """)

    with st.expander("📊 **Data Sources & Quality**", expanded=False):
        st.markdown("""
            ### Primary Data Sources

            | Dataset | Source | Date | Records |
            |---------|--------|------|---------|
            | **IDP Displacement Data** | IOM DTM | April 29, 2024 | 181 localities |
            | **Health Facilities** | HOT OSM | November 4, 2025 | 1,126 facilities |
            | **Administrative Boundaries** | OCHA COD-AB | April 4, 2023 | 189 localities |

            ### Data Quality Metrics

            - ✅ **IDP Data:** 100% completeness at locality level, totals match state aggregates
            - ✅ **Facility Data:** 97% have names, 100% have valid coordinates
            - ✅ **Geospatial:** All coordinates within Sudan boundaries (21.8-39°E, 3-23°N)
            - ⚠️ **Coordinate Precision:** ~50 localities use verified coordinates, ~131 use state-level approximations

            ### Data Governance

            All datasets are:
            - Publicly available from humanitarian data repositories
            - Subject to open data licensing
            - Contain no personally identifiable information (PII)
            - Documented with full provenance and methodology
        """)

    with st.expander("⚠️ **Limitations & Assumptions**", expanded=False):
        st.markdown("""
            ### Current Limitations

            1. **Temporal Scope**
               - Analysis represents single time point (April 2024 IDP data)
               - Does not capture population movement trends or seasonal variations
               - Facility data may not reflect current operational status

            2. **Coordinate Precision**
               - ~72% of locality coordinates are state-level approximations with random offsets
               - Distance calculations have ±5km uncertainty for approximate locations
               - Production system requires official locality boundary shapefiles

            3. **Facility Functionality**
               - Assumes all mapped facilities are operational
               - Does not account for capacity, staffing, or service availability
               - No integration with WHO HeRAMS operational status data

            4. **Access Modeling**
               - Uses Euclidean (straight-line) distance as proxy for travel time
               - Does not account for road networks, terrain, or security barriers
               - Seasonal factors (rainy season impassability) not considered

            ### Key Assumptions

            - Health facility locations accurately represent service availability
            - IDP populations are concentrated near locality centroids
            - Distance is primary barrier to healthcare access
            - All IDPs have equal healthcare needs (no stratification by vulnerability sub-groups)

            ### Recommended Enhancements

            **Short-term:**
            - Acquire official OCHA COD-AB locality boundary shapefiles
            - Integrate WHO HeRAMS facility operational status
            - Add facility capacity data (beds, staff, specialties)

            **Long-term:**
            - Real-time API integration for dynamic IDP tracking
            - Network analysis using OSM road data for travel time modeling
            - Disease outbreak data integration (cholera, malaria, measles)
            - Predictive modeling for future displacement patterns
        """)

    with st.expander("🔄 **Analysis Workflow Diagram**", expanded=False):
        st.markdown("""
            ### End-to-End Pipeline
```
            Data Loading → Proximity Calculation → Vulnerability Scoring → Statistical Validation → Visualization
```

            **Phase 1: Geospatial Data Preparation**
            - Load IDP data (181 localities, 6.55M IDPs)
            - Load health facilities (1,126 facilities, 238 critical)
            - Create GeoDataFrames with point geometries
            - Generate locality centroids (verified + approximate)

            **Phase 2: Proximity Analysis**
            - Calculate haversine distances (great circle)
            - Nearest neighbor queries via KD-tree (O(log n))
            - Facility counts within 5km, 10km, 20km radii

            **Phase 3: Vulnerability Assessment**
            - Compute IDP burden scores (0-100)
            - Compute facility access scores (0-100, inverted)
            - Compute origin intensity scores (0-100)
            - Calculate weighted composite index
            - Classify into risk categories

            **Phase 4: Statistical Validation**
            - Spatial autocorrelation (Moran's I)
            - Machine learning classification (Random Forest, Logistic Regression)
            - Regional hypothesis testing (t-tests, ANOVA, chi-square)
            - Feature importance analysis

            **Phase 5: Visualization & Communication**
            - Generate static maps (PNG)
            - Create interactive maps (Folium/HTML)
            - Build dashboard (Streamlit)
            - Export analysis outputs (CSV, GeoJSON)
        """)

    with st.expander("🔍 **Critical Findings & Interpretation**", expanded=False):
        st.markdown("""
            ### Why Are There No "Critical" Risk Localities?

            The analysis identified **zero localities** meeting the Critical threshold (vulnerability index ≥80). This reflects:

            1. **Distributed Crisis Pattern:** Sudan's humanitarian crisis manifests as widespread moderate vulnerability across many localities rather than extreme localized hotspots.

            2. **Scoring Methodology Design:** The composite weighted index was calibrated for **relative prioritization** rather than absolute severity classification.

            3. **Data Granularity Limitations:** State-level facility aggregation may mask severe sub-locality gaps where IDPs concentrate in areas distant from mapped facility coordinates.

            **Implication:** The absence of "Critical" localities does **not** indicate absence of crisis. Rather, **156 localities (86%)** require intervention, with resource allocation differentiated by High/Moderate priority tiers.

            ---

            ### The Darfur Paradox: Why Lower Vulnerability Scores?

            Despite being the conflict epicenter, **Darfur states show significantly lower vulnerability scores** (31.90 vs 42.33, p<0.001) than non-Darfur regions. This likely reflects:

            1. **Outward Displacement:** IDPs fled **from** Darfur **to** other states (Khartoum, River Nile, Red Sea), creating burden concentration in receiving areas.

            2. **Pre-existing Infrastructure:** Darfur's baseline health facility density, while low, may be proportionally better than the infrastructure capacity of regions suddenly absorbing massive IDP influxes.

            3. **Data Capture Limitations:** Darfur's insecurity may result in undercounting of IDPs who remain in conflict zones versus those who reached safer displacement sites covered by IOM DTM surveys.

            **Implication:** **River Nile state** (4 of top 5 vulnerable localities) and **Red Sea state** (Port Sudan) require immediate humanitarian focus as overwhelmed IDP hosting areas.

            ---

            ### The Accessibility Crisis: 86% Beyond Threshold

            **156 localities (86.2%)** exceed the 20km hospital access threshold, representing **5,090,385 IDPs (77.7%)** with severely compromised healthcare access. The **88.1km mean distance** is:

            - **17.6× the WHO recommended maximum** (5km)
            - **4.4× the humanitarian emergency threshold** (20km)
            - **Equivalent to 2+ hours travel time** under ideal conditions (impassable during rainy season/conflict)

            **Implication:** Fixed facility expansion alone cannot address this crisis. Response requires:
            - Mobile health clinics targeting clusters of distant localities
            - Community health worker programs in IDP settlements
            - Telemedicine pilots where connectivity exists
            - Pre-positioned emergency medical supplies in high-burden localities
        """)


def render_download_center():
    """
    Provides a centralized interface for downloading all analytical outputs.

    Steps:
        1. Checks for the existence of output files (CSVs, GeoJSONs, Reports).
        2. Creates download buttons for:
            - Analysis CSV.
            - Localities GeoJSON.
            - Health Facilities GeoJSON.
            - Statistical Analysis Text Report.
        3. Provides instructions on where to find static visualization assets.
    """

    st.markdown(
        '<h2 class="section-header">📥 Download Center</h2>', unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="background-color: #f0f9ff; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #0284c7;">
            <strong>💾 Export Analysis Outputs:</strong> Download all data files, visualizations, and reports for further analysis or integration.
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Data Files")

        csv_path = OUTPUT_PATH / "locality_vulnerability_analysis.csv"
        if csv_path.exists():
            with open(csv_path, "rb") as f:
                st.download_button(
                    label="📄 Download Analysis CSV",
                    data=f,
                    file_name="locality_vulnerability_analysis.csv",
                    mime="text/csv",
                    help="Main analysis results table",
                )

        localities_geojson_path = OUTPUT_PATH / "localities_vulnerability.geojson"
        if localities_geojson_path.exists():
            with open(localities_geojson_path, "rb") as f:
                st.download_button(
                    label="🗺️ Download Localities GeoJSON",
                    data=f,
                    file_name="localities_vulnerability.geojson",
                    mime="application/json",
                    help="Locality geometries with vulnerability data",
                )

        facilities_geojson_path = OUTPUT_PATH / "health_facilities.geojson"
        if facilities_geojson_path.exists():
            with open(facilities_geojson_path, "rb") as f:
                st.download_button(
                    label="🏥 Download Facilities GeoJSON",
                    data=f,
                    file_name="health_facilities.geojson",
                    mime="application/json",
                    help="Health facility locations",
                )

    with col2:
        st.markdown("### 📈 Analysis Reports")

        report_path = Path(
            REPO_ROOT
            / "4_data_analysis"
            / "outputs"
            / "inferential_analysis"
            / "inferential_analysis_report.txt"
        )
        if report_path.exists():
            with open(report_path, "rb") as f:
                st.download_button(
                    label="📑 Download Statistical Report",
                    data=f,
                    file_name="inferential_analysis_report.txt",
                    mime="text/plain",
                    help="Comprehensive statistical validation report",
                )

        st.markdown("### 🖼️ Visualizations")

        st.info("""
            **Static Maps Available:**
            - Vulnerability index map (PNG)
            - Risk categories map (PNG)
            - Accessibility gap map (PNG)
            - Interactive map (HTML)

            **Statistical Visuals:**
            - Moran's I scatter plot (PNG)
            - Feature importance chart (PNG)
            - Confusion matrices (PNG)
            - Regional comparison plots (PNG)

            📂 All files located in: `outputs/` directory
        """)

    st.success("All analysis outputs are available for download and further use.")
