"""
Visualization Module - Generate Maps of Vulnerability

This module creates static and interactive geospatial visualizations based on the
vulnerability analysis results. It generates three static maps for reporting and
one interactive Folium map for dashboard preview, visualizing IDP burden,
facility access gaps, and final risk categorization.

Author: Abdulrahman Sirelkhatim + Gemini
Date: November 14, 2025
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path
import folium
import warnings

# Suppress minor GeoPandas warnings during plotting
warnings.filterwarnings("ignore", category=UserWarning)

# --- Configuration ---
OUTPUT_PATH = Path("outputs")
MAPS_PATH = OUTPUT_PATH / "maps"
MAPS_PATH.mkdir(parents=True, exist_ok=True)

# Color schemes for consistency: Red, Orange, Yellow, Green
RISK_COLORS = {
    "Critical": "#d32f2f",
    "High": "#f57c00",
    "Moderate": "#fbc02d",
    "Low": "#388e3c",
}

VULNERABILITY_CMAP = "YlOrRd"


def create_static_vulnerability_map(analysis_df: gpd.GeoDataFrame):
    """
    Generate static scatter map of locality vulnerability scores.

    This uses a scatter plot with point size determined by IDP population and
    color determined by the vulnerability index, serving as a proxy for
    a choropleth map (since true boundaries are unavailable).

    Args:
        analysis_df (gpd.GeoDataFrame): Locality data with vulnerability scores.
    """

    print("\n Generating vulnerability index map...")

    fig, ax = plt.subplots(figsize=(14, 10))

    scatter = ax.scatter(
        [geom.x for geom in analysis_df.geometry],
        [geom.y for geom in analysis_df.geometry],
        c=analysis_df["vulnerability_index"],
        s=analysis_df["total_idps"] / 50,
        cmap=VULNERABILITY_CMAP,
        alpha=0.7,
        edgecolors="black",
        linewidth=0.5,
    )

    plt.colorbar(scatter, ax=ax, label="Vulnerability Index (0-100)")

    # Styling
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(
        "Sudan: Locality Vulnerability Index\nIDP Population vs. Health Facility Access",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.grid(True, alpha=0.3, linestyle="--")

    # Add legend for point sizes with more spacing
    legend_sizes = [50000, 100000, 150000]
    legend_points = [
        plt.scatter([], [], s=size / 500, c="gray", alpha=0.7, edgecolors="black")
        for size in legend_sizes
    ]
    legend_labels = [f"{s / 1000:.0f}k IDPs" for s in legend_sizes]
    ax.legend(
        legend_points,
        legend_labels,
        title="IDP Population",
        loc="upper left",
        frameon=True,
        fontsize=10,
        labelspacing=1.5,
        borderpad=1,
        handletextpad=1.5,
    )
    plt.tight_layout()

    # Save
    output_file = MAPS_PATH / "vulnerability_index_map.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"  ✓ Saved: {output_file}")

    plt.close()


def create_risk_category_map(analysis_df: gpd.GeoDataFrame):
    """
    Generate static scatter map colored by the final risk category.

    Args:
        analysis_df (gpd.GeoDataFrame): Locality data with assigned risk categories.
    """

    print("\n Generating risk category map...")

    fig, ax = plt.subplots(figsize=(14, 10))

    # Plot each risk category separately
    for category in ["Low", "Moderate", "High", "Critical"]:
        subset = analysis_df[analysis_df["risk_category"] == category]
        if len(subset) > 0:
            ax.scatter(
                [geom.x for geom in subset.geometry],
                [geom.y for geom in subset.geometry],
                c=RISK_COLORS[category],
                s=subset["total_idps"] / 300,
                label=f"{category} ({len(subset)} localities)",
                alpha=0.7,
                edgecolors="black",
                linewidth=0.5,
            )

    # Styling
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(
        "Sudan: Humanitarian Risk Categories\nBased on IDP Burden and Facility Access",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(
        title="Risk Level",
        loc="upper left",
        frameon=True,
        fontsize=11,
        labelspacing=1.2,
        borderpad=1,
        handletextpad=1.5,
    )

    plt.tight_layout()

    # Save
    output_file = MAPS_PATH / "risk_categories_map.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"  ✓ Saved: {output_file}")

    plt.close()


def create_accessibility_map(
    analysis_df: gpd.GeoDataFrame, facilities_gdf: gpd.GeoDataFrame
):
    """
    Generate map showing IDP locations colored by distance to the nearest critical
    facility, overlaid with the facility locations themselves.

    Args:
        analysis_df (gpd.GeoDataFrame): Locality data with distance metrics.
        facilities_gdf (gpd.GeoDataFrame): All health facilities.
    """

    print("\n Generating accessibility gap map...")

    fig, ax = plt.subplots(figsize=(14, 10))

    # Plot localities colored by distance to nearest facility (using final column name)
    scatter_localities = ax.scatter(
        [geom.x for geom in analysis_df.geometry],
        [geom.y for geom in analysis_df.geometry],
        c=analysis_df["dist_to_nearest_hospital_km"],
        s=analysis_df["total_idps"] / 100,
        cmap="RdYlGn_r",
        alpha=0.7,
        edgecolors="black",
        linewidth=0.5,
        label="Localities (sized by IDPs)",
    )

    # Overlay critical health facilities
    critical = facilities_gdf[
        facilities_gdf["facility_type_standard"].isin(["hospital", "clinic"])
    ]

    ax.scatter(
        [geom.x for geom in critical.geometry],
        [geom.y for geom in critical.geometry],
        c="blue",
        s=40,
        marker="+",
        linewidths=2.5,
        label=f"Critical Facilities (n={len(critical)})",
        zorder=5,
    )

    # Color bar
    plt.colorbar(
        scatter_localities, ax=ax, label="Distance to Nearest Hospital/Clinic (km)"
    )

    # Styling
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title(
        "Sudan: Geographic Accessibility Analysis\nIDP Locations vs. Critical Health Facilities",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.grid(True, alpha=0.3, linestyle="--")
    # Create custom legend handles with proper sizing
    locality_handle = Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor="green",
        markersize=10,
        alpha=0.7,
        markeredgecolor="black",
        markeredgewidth=0.5,
        linestyle="",
    )
    facility_handle = Line2D(
        [0],
        [0],
        marker="+",
        color="blue",
        markersize=12,
        markeredgewidth=2.5,
        linestyle="",
    )

    ax.legend(
        handles=[locality_handle, facility_handle],
        labels=[
            "Localities (sized by IDPs)",
            f"Critical Facilities (n={len(critical)})",
        ],
        loc="upper left",
        frameon=True,
        fontsize=10,
        labelspacing=1.5,
        borderpad=1,
        handletextpad=1.5,
    )

    plt.tight_layout()

    # Save
    output_file = MAPS_PATH / "accessibility_gap_map.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"  ✓ Saved: {output_file}")

    plt.close()


def create_interactive_folium_map(
    analysis_df: gpd.GeoDataFrame, facilities_gdf: gpd.GeoDataFrame
):
    """
    Creates an interactive Folium map with layered data for dashboard preview.
    The map includes vulnerability-colored localities (sized by IDPs) and
    markers for health facilities.

    Args:
        analysis_df (gpd.GeoDataFrame): Locality data (uses final column names).
        facilities_gdf (gpd.GeoDataFrame): All health facilities.

    Returns:
        folium.Map: The generated Folium map object.
    """

    print("\n Generating interactive Folium map...")

    # Center on Sudan
    sudan_center = [15.5, 32.5]

    # Create base map
    m = folium.Map(
        location=sudan_center, zoom_start=6, tiles="OpenStreetMap", control_scale=True
    )

    # Add title
    title_html = """
    <div style="position: fixed;
                 top: 10px; left: 50px; width: 400px; height: 90px;
                 background-color: white; border:2px solid grey; z-index:9999;
                 font-size:14px; padding: 10px">
    <h4 style="margin-bottom: 5px;">Sudan: Humanitarian Crisis Analysis</h4>
    <p style="margin: 0; font-size: 12px;">IDP Population vs. Health Facility Access</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))

    # Create feature groups for layer control
    locality_layer = folium.FeatureGroup(name="Localities (Vulnerability)")
    facility_layer = folium.FeatureGroup(name="All Health Facilities")
    critical_layer = folium.FeatureGroup(name="Hospitals & Clinics")

    # Add localities as circles colored by vulnerability
    for _, row in analysis_df.iterrows():
        color = RISK_COLORS.get(row["risk_category"], "gray")

        # Use final, clean column names from the exported GeoJSON
        locality_name = str(row["locality_name"])
        state_name = str(row["state_name"])

        # Create popup text
        popup_text = f"""
        <b>{locality_name}</b><br>
        State: {state_name}<br>
        IDPs: {row["total_idps"]:,}<br>
        <hr>
        <b>Vulnerability Score: {row["vulnerability_index"]:.1f}</b><br>
        Risk Category: <span style="color:{color}"><b>{row["risk_category"]}</b></span><br>
        <hr>
        Distance to Hospital: {row["dist_to_nearest_hospital_km"]:.1f} km<br>
        Hospitals within 20km: {row["hospitals_within_20km"]}
        """

        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=max(3, row["total_idps"] / 10000),
            popup=folium.Popup(popup_text, max_width=300),
            color="black",
            fillColor=color,
            fillOpacity=0.7,
            weight=1,
        ).add_to(locality_layer)

    # Add all facilities (General Layer)
    for _, row in facilities_gdf.iterrows():
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=3,
            popup=f"<b>{row['facility_name_display']}</b><br>Type: {row['facility_type_standard']}",
            color="blue",
            fillColor="lightblue",
            fillOpacity=0.6,
            weight=1,
        ).add_to(facility_layer)

    # Add critical facilities (Specific Layer with distinct markers)
    critical = facilities_gdf[
        facilities_gdf["facility_type_standard"].isin(["hospital", "clinic"])
    ]

    for _, row in critical.iterrows():
        icon_color = "red" if row["facility_type_standard"] == "hospital" else "orange"
        icon = "plus-sign"

        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=f"<b>{row['facility_name_display']}</b><br>Type: {row['facility_type_standard'].title()}",
            icon=folium.Icon(color=icon_color, icon=icon, prefix="glyphicon"),
        ).add_to(critical_layer)

    # Add layers and controls
    locality_layer.add_to(m)
    critical_layer.add_to(m)
    facility_layer.add_to(m)
    folium.LayerControl().add_to(m)

    # Add legend
    legend_html = f"""
    <div style="position: fixed;
                bottom: 50px; right: 50px; width: 200px; height: 240px;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:12px; padding: 10px">
    <p style="margin: 0; font-weight: bold;">Risk Categories (Localities)</p>
    <p style="margin: 5px 0;"><span style="color:{RISK_COLORS["Critical"]}">●</span> Critical</p>
    <p style="margin: 5px 0;"><span style="color:{RISK_COLORS["High"]}">●</span> High</p>
    <p style="margin: 5px 0;"><span style="color:{RISK_COLORS["Moderate"]}">●</span> Moderate</p>
    <p style="margin: 5px 0;"><span style="color:{RISK_COLORS["Low"]}">●</span> Low</p>
    <hr>
    <p style="margin: 5px 0; font-weight: bold;">Facilities</p>
    <p style="margin: 5px 0;"><span style="color:red">📍</span> Hospital</p>
    <p style="margin: 5px 0;"><span style="color:orange">📍</span> Clinic</p>
    </div>
"""
    m.get_root().html.add_child(folium.Element(legend_html))

    # Save
    output_file = MAPS_PATH / "interactive_vulnerability_map.html"
    m.save(str(output_file))
    print(f"  ✓ Saved: {output_file}")
    print("    (Open in browser to interact)")

    return m


def generate_analysis_visualizations(
    analysis_df: gpd.GeoDataFrame, facilities_gdf: gpd.GeoDataFrame
):
    """
    Generate complete set of analysis visualizations.

    This is the main function to call from the crisis analysis pipeline.

    Args:
        analysis_df (gpd.GeoDataFrame): Final analysis data (localities) with geometry.
        facilities_gdf (gpd.GeoDataFrame): All health facilities data with geometry.
    """

    print("\n" + "=" * 70)
    print("GENERATING ANALYSIS VISUALIZATIONS")
    print("=" * 70)

    # Static maps for reporting
    create_static_vulnerability_map(analysis_df)
    create_risk_category_map(analysis_df)
    create_accessibility_map(analysis_df, facilities_gdf)

    # Interactive map for dashboard preview
    create_interactive_folium_map(analysis_df, facilities_gdf)

    print("\n" + "=" * 70)
    print("✓ All visualizations generated successfully!")
    print(f"  Maps saved to: {MAPS_PATH}")
    print("=" * 70)


if __name__ == "__main__":
    # Example execution if run standalone (assumes data is already output)
    print("Loading analysis results from outputs...")

    # Load final results using the consistent output path structure
    try:
        ANALYSIS_OUTPUT_PATH = Path("outputs")
        analysis_df = gpd.read_file(
            ANALYSIS_OUTPUT_PATH / "localities_vulnerability.geojson"
        )
        facilities_gdf = gpd.read_file(
            ANALYSIS_OUTPUT_PATH / "health_facilities.geojson"
        )

        # Generate visualizations
        generate_analysis_visualizations(analysis_df, facilities_gdf)

    except FileNotFoundError as e:
        print(
            "ERROR: Could not load required GeoJSON files. Please run 'crisis_analysis.py' first."
        )
        print(f"Missing file: {e}")
