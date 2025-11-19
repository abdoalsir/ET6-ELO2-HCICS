"""
A module for performing geospatial proximity analysis to identify gaps between
IDP populations and health facility access in Sudan.

This module conducts comprehensive vulnerability assessment by analyzing the spatial
distribution of internally displaced persons relative to critical health infrastructure,
generating actionable insights for humanitarian response planning.

Module contents:
    - load_and_prepare_data: Loads all cleaned datasets required for analysis.
    - create_facility_geodataframe: Converts health facilities to GeoDataFrame with point geometries.
    - create_locality_centroids: Creates geographic centroids for IDP localities.
    - haversine_distance: Calculates great circle distance between coordinate pairs.
    - calculate_proximity_metrics: Computes distance and accessibility metrics for localities.
    - calculate_vulnerability_index: Generates composite vulnerability scores.
    - export_analysis_results: Exports analysis outputs for dashboard integration.
    - generate_summary_report: Creates human-readable summary of key findings.
    - main: Executes the complete analysis pipeline.

Created on 14-11-25
@author: Gemini
"""

import pandas as pd
import numpy as np
import geopandas as gpd
from pathlib import Path
from shapely.geometry import Point
from scipy.spatial import cKDTree
import warnings

warnings.filterwarnings("ignore")

# ============================================================================
# CONFIGURATION
# ============================================================================

CLEAN_DATA = Path("../1_datasets/clean")
OUTPUT_PATH = Path("outputs")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# Analysis parameters
CRITICAL_FACILITY_TYPES = ["hospital", "clinic"]
ACCESSIBILITY_THRESHOLDS = [5, 10, 20]  # kilometers
VULNERABILITY_WEIGHTS = {
    "idp_burden": 0.4,
    "facility_access": 0.4,
    "origin_intensity": 0.2,
}

# ============================================================================
# PHASE 1: GEOSPATIAL DATA PREPARATION
# ============================================================================


def load_and_prepare_data():
    """
    Loads all cleaned datasets required for geospatial analysis.

    Steps:
        1. Loads locality-level IDP data
        2. Loads state-level IDP data
        3. Loads health facility locations
        4. Loads administrative boundary data
        5. Prints loading confirmation with record counts

    Returns:
        tuple: Contains four DataFrames in order:
            - idps_locality (pd.DataFrame): Locality-level IDP records
            - idps_state (pd.DataFrame): State-level IDP aggregates
            - facilities (pd.DataFrame): Health facility coordinates and metadata
            - boundaries (pd.DataFrame): Administrative boundary information

    Raises:
        FileNotFoundError: If any required clean data file is missing.
        pd.errors.EmptyDataError: If any CSV file is empty or corrupted.
    """
    print("\n" + "=" * 70)
    print("PHASE 1: GEOSPATIAL DATA PREPARATION")
    print("=" * 70)

    # Load datasets
    print("\nLoading datasets...")
    idps_locality = pd.read_csv(CLEAN_DATA / "clean_idps_locality.csv")
    idps_state = pd.read_csv(CLEAN_DATA / "clean_idps_state.csv")
    facilities = pd.read_csv(CLEAN_DATA / "clean_health_facilities.csv")
    boundaries = pd.read_csv(CLEAN_DATA / "clean_boundaries_data.csv")

    print(f"  ✓ Loaded {len(idps_locality)} locality IDP records")
    print(f"  ✓ Loaded {len(idps_state)} state IDP records")
    print(f"  ✓ Loaded {len(facilities)} health facilities")
    print(f"  ✓ Loaded {len(boundaries)} boundary records")

    return idps_locality, idps_state, facilities, boundaries


def create_facility_geodataframe(facilities):
    """
    Converts health facilities DataFrame to GeoDataFrame with point geometries.

    Steps:
        1. Creates Point geometries from longitude/latitude coordinates
        2. Initializes GeoDataFrame with EPSG:4326 (WGS84) coordinate system
        3. Filters facilities by critical types (hospitals and clinics)
        4. Reports facility counts

    Args:
        facilities (pd.DataFrame): Health facility data with longitude and latitude columns.

    Returns:
        tuple: Contains two GeoDataFrames:
            - facilities_gdf (gpd.GeoDataFrame): All facilities with point geometries
            - critical_facilities (gpd.GeoDataFrame): Subset containing only hospitals/clinics

    Raises:
        KeyError: If required columns (longitude, latitude, facility_type_standard) are missing.
        ValueError: If coordinate values are invalid or out of range.
    """
    print("\nCreating facility GeoDataFrame...")

    # Create point geometries
    geometry = [
        Point(lon, lat)
        for lon, lat in zip(facilities["longitude"], facilities["latitude"])
    ]

    facilities_gdf = gpd.GeoDataFrame(facilities, geometry=geometry, crs="EPSG:4326")

    # Filter critical facilities
    critical_facilities = facilities_gdf[
        facilities_gdf["facility_type_standard"].isin(CRITICAL_FACILITY_TYPES)
    ].copy()

    print(f"  ✓ Created GeoDataFrame with {len(facilities_gdf)} facilities")
    print(f"  ✓ Identified {len(critical_facilities)} critical facilities")

    return facilities_gdf, critical_facilities


def create_locality_centroids(idps_locality, boundaries):
    """
    Creates geographic centroids for IDP localities using verified coordinates
    where available, with approximate locations as fallback.

    Steps:
        1. Merges IDP data with boundary information to get locality metadata
        2. Attempts to import verified coordinate overrides module
        3. Generates centroids using either:
           - Verified coordinates for major localities (if available)
           - Approximate state-based locations with random offset (fallback)
        4. Creates GeoDataFrame with locality centroids
        5. Reports centroid creation status and coordinate quality

    Args:
        idps_locality (pd.DataFrame): Locality-level IDP displacement data.
        boundaries (pd.DataFrame): Administrative boundary data with locality codes.

    Returns:
        gpd.GeoDataFrame: Localities with Point geometries representing centroids,
                          includes all IDP data merged with boundary metadata.

    Raises:
        KeyError: If required merge columns are missing from input DataFrames.

    Notes:
        - Uses locality_coordinate module for verified coordinates when available
        - Falls back to approximate state-level centroids with random offsets
        - Random seed (42) ensures reproducibility of approximate locations
        - MVP limitation: Some coordinates are approximations pending full geocoding
    """
    print("\nCreating locality centroids...")

    # Merge IDP data with boundaries to get locality information
    localities_merged = idps_locality.merge(
        boundaries[["locality_code", "locality_name_en", "state_name_en", "area_sqkm"]],
        on="locality_code",
        how="left",
        suffixes=("", "_boundary"),
    )

    # Import coordinate fixes module
    try:
        from locality_coordinate import get_locality_coordinates

        print("  ✓ Using verified coordinate overrides where available")
        use_verified = True
    except ImportError:
        print("  Coordinate fixes module not found, using approximate centroids")
        use_verified = False

    np.random.seed(42)  # Reproducibility for approximate locations

    # State centers for fallback
    state_centers = {
        "Khartoum": (15.5, 32.5),
        "North Darfur": (13.6, 25.3),
        "South Darfur": (11.7, 24.9),
        "East Darfur": (11.5, 26.1),
        "West Darfur": (12.5, 23.0),
        "Central Darfur": (12.8, 24.3),
        "River Nile": (17.7, 33.9),
        "Northern": (19.2, 30.5),
        "Red Sea": (19.6, 37.2),
        "Kassala": (15.5, 36.4),
        "Gedaref": (14.0, 35.4),
        "Sennar": (13.6, 33.6),
        "Blue Nile": (11.7, 34.4),
        "White Nile": (13.3, 32.7),
        "Aj Jazirah": (14.4, 33.5),
        "North Kordofan": (13.6, 29.4),
        "South Kordofan": (11.2, 29.4),
        "West Kordofan": (11.4, 27.7),
        "Abyei PCA": (10.0, 28.4),
    }

    # Generate centroids
    centroids = []
    verified_count = 0

    for _, row in localities_merged.iterrows():
        locality_name = row["locality_displacement"]
        state = row["state_displacement"]

        if use_verified:
            lat, lon = get_locality_coordinates(locality_name, state)
            centroids.append(Point(lon, lat))
            # Check if this was a verified coordinate (simplified check)
            if state == "Red Sea" and "Port Sudan" in locality_name:
                verified_count += 1
        else:
            # Fallback to approximate centroids
            if state in state_centers:
                center_lat, center_lon = state_centers[state]
                lat = center_lat + np.random.uniform(-1.0, 1.0)
                lon = center_lon + np.random.uniform(-1.0, 1.0)
                centroids.append(Point(lon, lat))
            else:
                centroids.append(Point(32.5, 15.5))

    localities_gdf = gpd.GeoDataFrame(
        localities_merged, geometry=centroids, crs="EPSG:4326"
    )

    print(f"  ✓ Created {len(localities_gdf)} locality centroids")
    if use_verified:
        print("✓ Applied verified coordinates for major localities")
    print("⚠ Note: Some coordinates are approximate (MVP limitation)")

    return localities_gdf


# ============================================================================
# PHASE 2: PROXIMITY ANALYSIS
# ============================================================================


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates great circle distance between two geographic points in kilometers.

    Uses the Haversine formula to compute the shortest distance over Earth's surface,
    accounting for spherical geometry. Suitable for distances where Earth curvature
    matters (>1km).

    Args:
        lat1 (float): Latitude of first point in decimal degrees.
        lon1 (float): Longitude of first point in decimal degrees.
        lat2 (float): Latitude of second point in decimal degrees.
        lon2 (float): Longitude of second point in decimal degrees.

    Returns:
        float: Distance between the two points in kilometers.

    Notes:
        - Uses Earth's mean radius of 6,371 km
        - Assumes spherical Earth (adequate for humanitarian analysis scale)
        - More accurate than Euclidean distance for geographic coordinates

    Example:
        >>> haversine_distance(15.5, 32.5, 15.6, 32.6)
        13.9  # Approximate distance in km
    """
    # Earth's radius in kilometers
    R = 6371

    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return R * c


def calculate_proximity_metrics(localities_gdf, facilities_gdf, critical_facilities):
    """
    Calculates distance and accessibility metrics for each IDP locality relative
    to health facilities.

    Steps:
        1. Extracts coordinate arrays from GeoDataFrames
        2. Builds KD-trees for efficient spatial queries
        3. For each locality, calculates:
           - Distance to nearest critical facility (hospital/clinic)
           - Distance to nearest facility of any type
           - Count of facilities within 5km, 10km, and 20km thresholds
        4. Compiles results into structured DataFrame
        5. Reports summary statistics

    Args:
        localities_gdf (gpd.GeoDataFrame): IDP localities with point geometries.
        facilities_gdf (gpd.GeoDataFrame): All health facilities with geometries.
        critical_facilities (gpd.GeoDataFrame): Subset of critical facilities only.

    Returns:
        pd.DataFrame: Proximity metrics for each locality containing:
            - locality_code: Administrative identifier
            - locality_name: Locality name
            - state_name: State name
            - total_idps: IDP population count
            - dist_nearest_critical_km: Distance to nearest hospital/clinic
            - dist_nearest_any_km: Distance to nearest facility (any type)
            - critical_within_5km/10km/20km: Count of critical facilities in radius
            - all_facilities_within_5km/10km/20km: Count of all facilities in radius

    Raises:
        ValueError: If GeoDataFrames contain invalid or missing geometries.

    Notes:
        - Uses KD-tree for O(log n) nearest neighbor queries
        - Rough degree-to-km conversion (1° ≈ 111km) for ball queries
        - Haversine distance provides accurate great-circle measurements
    """
    print("\n" + "=" * 70)
    print("PHASE 2: PROXIMITY ANALYSIS")
    print("=" * 70)

    print("\nCalculating distance metrics...")

    # Extract coordinates
    facility_coords = np.array([(geom.x, geom.y) for geom in facilities_gdf.geometry])
    critical_coords = np.array(
        [(geom.x, geom.y) for geom in critical_facilities.geometry]
    )

    # Build KD-trees for efficient nearest neighbor search
    facility_tree = cKDTree(facility_coords)
    critical_tree = cKDTree(critical_coords)

    # Calculate distances
    results = []

    for idx, row in localities_gdf.iterrows():
        loc_point = (row.geometry.x, row.geometry.y)

        # Distance to nearest critical facility
        dist_critical, idx_critical = critical_tree.query(loc_point)
        dist_critical_km = haversine_distance(
            row.geometry.y,
            row.geometry.x,
            critical_facilities.iloc[idx_critical].geometry.y,
            critical_facilities.iloc[idx_critical].geometry.x,
        )

        # Distance to nearest any facility
        dist_any, idx_any = facility_tree.query(loc_point)
        dist_any_km = haversine_distance(
            row.geometry.y,
            row.geometry.x,
            facilities_gdf.iloc[idx_any].geometry.y,
            facilities_gdf.iloc[idx_any].geometry.x,
        )

        # Count facilities within thresholds
        facilities_within = {}
        critical_within = {}

        for threshold in ACCESSIBILITY_THRESHOLDS:
            # All facilities within threshold
            indices_all = facility_tree.query_ball_point(loc_point, threshold / 111)
            facilities_within[f"{threshold}km"] = len(indices_all)

            # Critical facilities within threshold
            indices_critical = critical_tree.query_ball_point(
                loc_point, threshold / 111
            )
            critical_within[f"{threshold}km"] = len(indices_critical)

        # Store results
        results.append(
            {
                "locality_code": row["locality_code"],
                "locality_name": row["locality_displacement"],
                "state_name": row["state_displacement"],
                "dist_nearest_critical_km": round(dist_critical_km, 2),
                "dist_nearest_any_km": round(dist_any_km, 2),
                "critical_within_5km": critical_within["5km"],
                "critical_within_10km": critical_within["10km"],
                "critical_within_20km": critical_within["20km"],
                "all_facilities_within_5km": facilities_within["5km"],
                "all_facilities_within_10km": facilities_within["10km"],
                "all_facilities_within_20km": facilities_within["20km"],
            }
        )

    proximity_df = pd.DataFrame(results)

    print(f"  ✓ Calculated proximity metrics for {len(proximity_df)} localities")
    print("\n  Summary Statistics:")
    print(
        f"    Mean distance to critical facility: {proximity_df['dist_nearest_critical_km'].mean():.1f} km"
    )
    print(
        f"    Max distance to critical facility: {proximity_df['dist_nearest_critical_km'].max():.1f} km"
    )
    print(
        f"    Localities beyond 20km threshold: {(proximity_df['dist_nearest_critical_km'] > 20).sum()}"
    )

    return proximity_df


# ============================================================================
# PHASE 3: VULNERABILITY ASSESSMENT
# ============================================================================


def calculate_vulnerability_index(localities_gdf, proximity_df):
    """
    Calculates composite vulnerability score for each locality based on IDP burden,
    facility access, and displacement origin patterns.

    Steps:
        1. Merges proximity metrics with IDP demographic data
        2. Calculates three normalized component scores (0-100):
           a. IDP Burden Score: Population size relative to maximum
           b. Facility Access Score: Combined distance and facility density
           c. Origin Intensity Score: Proportion from conflict-affected Khartoum
        3. Computes weighted composite Vulnerability Index
        4. Classifies localities into risk categories (Critical/High/Moderate/Low)
        5. Reports risk distribution statistics

    Args:
        localities_gdf (gpd.GeoDataFrame): Locality geometries with IDP data.
        proximity_df (pd.DataFrame): Calculated proximity metrics from Phase 2.

    Returns:
        pd.DataFrame: Complete analysis dataset containing:
            - All original IDP and proximity data
            - idp_burden_score: Normalized population burden (0-100)
            - facility_access_score: Combined access metric (0-100, higher=worse)
            - origin_intensity_score: Conflict displacement indicator (0-100)
            - vulnerability_index: Weighted composite score (0-100)
            - risk_category: Classification (Critical/High/Moderate/Low)

    Raises:
        KeyError: If required columns are missing from input DataFrames.

    Notes:
        - Vulnerability weights: IDP burden (40%), facility access (40%), origin (20%)
        - Access score combines distance (60%) and facility count (40%)
        - Risk thresholds: Critical ≥80, High ≥60, Moderate ≥40, Low <40
        - Higher scores indicate greater vulnerability and humanitarian need
    """
    print("\n" + "=" * 70)
    print("PHASE 3: VULNERABILITY ASSESSMENT")
    print("=" * 70)

    # Merge proximity metrics with IDP data
    analysis_df = localities_gdf.merge(proximity_df, on="locality_code", how="left")

    print("\nCalculating vulnerability components...")

    # Component 1: IDP Burden Score (0-100)
    max_idps = analysis_df["total_idps"].max()
    analysis_df["idp_burden_score"] = (analysis_df["total_idps"] / max_idps) * 100

    # Component 2: Facility Access Score (0-100, inverted so higher = worse access)
    # Normalize distance (inverse relationship)
    max_distance = analysis_df["dist_nearest_critical_km"].max()
    analysis_df["distance_score"] = (
        analysis_df["dist_nearest_critical_km"] / max_distance
    ) * 100

    # Normalize facility count (inverse relationship)
    max_facilities = analysis_df["critical_within_20km"].max()
    if max_facilities > 0:
        analysis_df["facility_count_score"] = (
            1 - analysis_df["critical_within_20km"] / max_facilities
        ) * 100
    else:
        analysis_df["facility_count_score"] = 100

    # Combined access score (average of distance and facility count)
    analysis_df["facility_access_score"] = (
        analysis_df["distance_score"] * 0.6 + analysis_df["facility_count_score"] * 0.4
    )

    # Component 3: Origin Intensity Score (0-100)
    # Higher proportion from Khartoum indicates recent, conflict-driven displacement
    if "origin_khartoum" in analysis_df.columns:
        analysis_df["origin_intensity_score"] = (
            analysis_df["origin_khartoum"] / analysis_df["total_idps"]
        ) * 100
    else:
        analysis_df["origin_intensity_score"] = 0

    # Calculate Composite Vulnerability Index
    analysis_df["vulnerability_index"] = (
        VULNERABILITY_WEIGHTS["idp_burden"] * analysis_df["idp_burden_score"]
        + VULNERABILITY_WEIGHTS["facility_access"]
        * analysis_df["facility_access_score"]
        + VULNERABILITY_WEIGHTS["origin_intensity"]
        * analysis_df["origin_intensity_score"]
    )

    # Classify risk categories
    def classify_risk(score):
        if score >= 80:
            return "Critical"
        elif score >= 60:
            return "High"
        elif score >= 40:
            return "Moderate"
        else:
            return "Low"

    analysis_df["risk_category"] = analysis_df["vulnerability_index"].apply(
        classify_risk
    )

    print("  ✓ Calculated vulnerability scores")
    print("\n  Risk Distribution:")
    risk_counts = analysis_df["risk_category"].value_counts()
    for category in ["Critical", "High", "Moderate", "Low"]:
        count = risk_counts.get(category, 0)
        pct = (count / len(analysis_df)) * 100
        print(f"    {category}: {count} localities ({pct:.1f}%)")

    return analysis_df


# ============================================================================
# PHASE 4: EXPORT AND SUMMARY
# ============================================================================


def export_analysis_results(analysis_df, facilities_gdf):
    """
    Exports analysis results in multiple formats for dashboard integration and GIS tools.

    Steps:
        1. Dynamically identifies column names (handles merge suffixes)
        2. Selects and renames key columns for clarity
        3. Exports CSV file with vulnerability analysis results
        4. Exports GeoJSON file with locality geometries for mapping
        5. Exports health facilities GeoJSON for overlay visualization
        6. Reports export success and handles errors gracefully

    Args:
        analysis_df (pd.DataFrame): Complete analysis with vulnerability scores.
        facilities_gdf (gpd.GeoDataFrame): Health facilities for map overlay.

    Returns:
        pd.DataFrame: Clean export dataset with standardized column names.

    Raises:
        IOError: If export directory is not writable.

    Notes:
        - CSV format for tabular analysis and dashboard integration
        - GeoJSON format for web mapping and GIS interoperability
        - Graceful error handling for GeoJSON exports (optional outputs)
        - Output location: ../4_analysis/outputs/ directory
    """
    print("\n" + "=" * 70)
    print("PHASE 4: EXPORT ANALYSIS RESULTS")
    print("=" * 70)

    # Debug: Print available columns
    print("\nDEBUG - Available columns in analysis_df:")
    print(analysis_df.columns.tolist())

    # Identify actual column names (handle merge suffixes dynamically)
    locality_col = [
        c
        for c in analysis_df.columns
        if "locality" in c.lower() and "displacement" in c.lower()
    ][0]
    state_col = [
        c
        for c in analysis_df.columns
        if "state" in c.lower() and "displacement" in c.lower()
    ][0]

    # Select columns for export
    export_cols = [
        "locality_code",
        locality_col,
        state_col,
        "total_idps",
        "dist_nearest_critical_km",
        "critical_within_20km",
        "idp_burden_score",
        "facility_access_score",
        "origin_intensity_score",
        "vulnerability_index",
        "risk_category",
    ]

    # Rename for clarity
    export_df = analysis_df[export_cols].copy()
    export_df.columns = [
        "locality_code",
        "locality_name",
        "state_name",
        "total_idps",
        "dist_to_nearest_hospital_km",
        "hospitals_within_20km",
        "idp_burden_score",
        "facility_access_score",
        "origin_intensity_score",
        "vulnerability_index",
        "risk_category",
    ]

    # Export CSV
    csv_path = OUTPUT_PATH / "locality_vulnerability_analysis.csv"
    export_df.to_csv(csv_path, index=False)
    print(f"\n  ✓ Exported: {csv_path}")

    # Export GeoJSON for mapping
    try:
        geojson_path = OUTPUT_PATH / "localities_vulnerability.geojson"
        analysis_gdf = gpd.GeoDataFrame(
            export_df, geometry=analysis_df.geometry, crs="EPSG:4326"
        )
        analysis_gdf.to_file(geojson_path, driver="GeoJSON")
        print(f"  ✓ Exported: {geojson_path}")
    except Exception as e:
        print(f"  ⚠ Warning: Could not export GeoJSON - {str(e)}")

    # Export facilities GeoJSON
    try:
        facilities_path = OUTPUT_PATH / "health_facilities.geojson"
        facilities_gdf.to_file(facilities_path, driver="GeoJSON")
        print(f"  ✓ Exported: {facilities_path}")
    except Exception as e:
        print(f"  ⚠ Warning: Could not export facilities GeoJSON - {str(e)}")

    return export_df


def generate_summary_report(analysis_df):
    """
    Generates human-readable summary report highlighting key findings and priority areas.

    Steps:
        1. Calculates national-level statistics
        2. Identifies top 10 most vulnerable localities
        3. Analyzes critical service gap localities
        4. Reports geographic accessibility challenges
        5. Prints formatted summary to console

    Args:
        analysis_df (pd.DataFrame): Complete vulnerability analysis dataset.

    Returns:
        None: Prints formatted report to stdout.

    Notes:
        - Summary designed for quick situational awareness
        - Highlights actionable insights for humanitarian response
        - Identifies localities requiring immediate intervention
        - Reports IDP populations affected by service gaps
    """
    print("\n" + "=" * 70)
    print("ANALYSIS SUMMARY REPORT")
    print("=" * 70)

    # Identify column names dynamically
    locality_col = [
        c
        for c in analysis_df.columns
        if "locality" in c.lower() and "displacement" in c.lower()
    ][0]
    state_col = [
        c
        for c in analysis_df.columns
        if "state" in c.lower() and "displacement" in c.lower()
    ][0]

    # National statistics
    total_idps = analysis_df["total_idps"].sum()
    mean_distance = analysis_df["dist_nearest_critical_km"].mean()

    print("\n📊 NATIONAL OVERVIEW")
    print(f"   Total IDPs analyzed: {total_idps:,}")
    print(f"   Total localities: {len(analysis_df)}")
    print(f"   Average distance to critical facility: {mean_distance:.1f} km")

    # Most vulnerable localities
    print("\n🚨 TOP 10 MOST VULNERABLE LOCALITIES")
    print(f"   {'Locality':<30} {'State':<20} {'Score':>8} {'Risk':>10}")
    print(f"   {'-' * 70}")

    top_10 = analysis_df.nlargest(10, "vulnerability_index")
    for _, row in top_10.iterrows():
        locality_name = str(row[locality_col])[:28]
        state_name = str(row[state_col])[:18]
        print(
            f"   {locality_name:<30} "
            f"{state_name:<20} "
            f"{row['vulnerability_index']:>8.1f} "
            f"{row['risk_category']:>10}"
        )

    # Critical gaps
    critical_localities = analysis_df[analysis_df["risk_category"] == "Critical"]
    print("\n⚠️ CRITICAL SERVICE GAPS")
    print(f"   {len(critical_localities)} localities in CRITICAL risk category")
    print(f"   These localities host {critical_localities['total_idps'].sum():,} IDPs")
    print(
        f"   Representing {critical_localities['total_idps'].sum() / total_idps * 100:.1f}% of total IDP population"
    )

    # Distance statistics
    beyond_20km = analysis_df[analysis_df["dist_nearest_critical_km"] > 20]
    print("\n🗺️ GEOGRAPHIC ACCESSIBILITY")
    print(f"   Localities beyond 20km from hospital/clinic: {len(beyond_20km)}")
    print(f"   IDPs in these distant localities: {beyond_20km['total_idps'].sum():,}")

    print("\n" + "=" * 70)
    print("Analysis complete! Results exported to outputs/ directory")
    print("=" * 70)


# ============================================================================
# MAIN EXECUTION
# ============================================================================


def main():
    """
    Executes the complete geospatial analysis pipeline.

    Pipeline Phases:
        Phase 1: Load and prepare geospatial data
        Phase 2: Calculate proximity and accessibility metrics
        Phase 3: Assess vulnerability and risk categories
        Phase 4: Export results and generate summary report

    Returns:
        tuple: Contains two DataFrames:
            - analysis_df: Complete analysis with all calculated metrics
            - export_df: Clean export dataset with standardized columns
            Returns (None, None) if pipeline fails.

    Raises:
        Exception: Catches all exceptions, prints error details, and returns None.

    Notes:
        - Comprehensive error handling with traceback for debugging
        - Progress reporting at each phase
        - Exports multiple file formats for different use cases
        - Designed for integration with dashboard visualization layer
    """
    print("\n" + "=" * 70)
    print("HUMANITARIAN CRISIS ANALYSIS CORE - HCICS MVP")
    print("Milestone 3: Data Analysis Phase")
    print("=" * 70)

    try:
        # Phase 1: Load and prepare data
        idps_locality, idps_state, facilities, boundaries = load_and_prepare_data()
        facilities_gdf, critical_facilities = create_facility_geodataframe(facilities)
        localities_gdf = create_locality_centroids(idps_locality, boundaries)

        # Phase 2: Proximity analysis
        proximity_df = calculate_proximity_metrics(
            localities_gdf, facilities_gdf, critical_facilities
        )

        # Phase 3: Vulnerability assessment
        analysis_df = calculate_vulnerability_index(localities_gdf, proximity_df)

        # Phase 4: Export and summary
        export_df = export_analysis_results(analysis_df, facilities_gdf)
        generate_summary_report(analysis_df)

        print("\n✅ SUCCESS: Analysis pipeline completed!")
        print("   Check outputs/ directory for results")

        return analysis_df, export_df

    except Exception as e:
        print(f"\n❌ ERROR: Analysis failed - {str(e)}")
        import traceback

        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    analysis_results, export_results = main()
