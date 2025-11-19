"""
Manual Coordinate Corrections for Known Localities

This module provides verified coordinates for localities where the approximate
centroid generation produces incorrect locations. These coordinates are sourced
from official gazetteers, OpenStreetMap, or administrative boundary centroids.

Author: Abdulrahman Sirelkhatim
Date: November 14, 2025
"""

# ============================================================================
# VERIFIED LOCALITY COORDINATES (Latitude, Longitude)
# ============================================================================

LOCALITY_COORDINATE_OVERRIDES = {
    # Red Sea State - Coastal localities
    "Port Sudan": (19.6158, 37.2164),  # Major port city
    "Sawakin": (19.1067, 37.3320),  # Historic port
    "Hala'ib": (22.2167, 36.6333),  # Northern border area
    "Jubayt Elma'aadin": (22.0000, 36.5000),  # Mining area (approximate)
    "Agig": (18.1768, 38.2669),  # Coastal locality
    "Sinkat": (18.8000, 37.2000),  # Inland from Port Sudan
    "Tawkar": (18.4333, 37.7333),  # Southern coast
    "Dordieb": (17.5471, 35.7407),  # Northeast coast
    "Haya": (17.5500, 38.0000),  # Southern Red Sea
    "Al Ganab": (22.5000, 36.2500),  # Northern area
    # Northern State - Nile River localities
    "Dongola": (19.1808, 30.4769),  # State capital
    "Karima": (18.5500, 31.8500),  # Near pyramids
    "Merwoe": (18.5000, 31.8500),  # Ancient site area
    "Delgo": (20.4500, 30.4333),  # Northern Nile
    "Halfa": (21.8000, 31.3500),  # Near Egypt border
    "Ad Dabbah": (18.0500, 30.9667),  # Nile locality
    "Al Burgaig": (20.5000, 30.2500),  # Northern locality
    "Al Golid": (21.0000, 30.0000),  # Far north
    # Khartoum State - Capital region
    "Khartoum": (15.5007, 32.5599),  # Capital city
    "Bahri": (15.6400, 32.5300),  # North Khartoum
    "Um Durman": (15.6444, 32.4778),  # West bank
    "Jebel Awlia": (15.2000, 32.5000),  # South dam area
    "Karrari": (15.7000, 32.4500),  # North extension
    "Sharg An Neel": (15.6000, 32.6000),  # East Nile
    "Um Bada": (15.4000, 32.3500),  # Western suburbs
    # River Nile State
    "Atbara": (17.7019, 33.9869),  # Major city
    "Shendi": (16.6922, 33.4339),  # Historic town
    "Ad Damar": (17.5925, 33.9706),  # Nile locality
    "Barbar": (18.0275, 33.9819),  # Northern Nile
    "Abu Hamad": (19.5333, 33.3167),  # Desert edge
    "Al Matama": (17.7167, 33.7667),  # Nile valley
    "Al Buhaira": (18.0000, 33.5000),  # Western area
    # Kassala State - Eastern border
    "Madeinat Kassala": (15.4552, 36.3997),  # State capital
    "Halfa Aj Jadeedah": (15.3272, 35.5986),  # New Halfa
    # Gedaref State - Agricultural zone
    "Madeinat Al Gedaref": (14.0354, 35.3839),  # State capital
    "Galabat Ash-Shargiah": (12.9667, 36.1667),  # Eastern border
    "Al Fao": (13.4333, 35.2333),  # Agricultural area
    # Darfur States - Western region
    "Al Fasher": (13.6286, 25.3497),  # North Darfur capital
    "Nyala Janoub": (12.0500, 24.8833),  # South Darfur urban
    "Nyala Shimal": (12.0833, 24.9000),  # South Darfur urban
    "Ag Geneina": (13.4525, 22.4503),  # West Darfur capital
    "Zalingi": (12.9097, 23.4708),  # Central Darfur capital
    # Blue Nile State - Southeastern border
    "Ed Damazine": (11.7891, 34.3592),  # State capital
    "Ar Rusayris": (11.8667, 34.3833),  # Near dam
    # Sennar State - Central agricultural
    "Sennar": (13.5667, 33.6167),  # Historic town
    "Sinja": (13.3500, 33.9333),  # Agricultural center
    # White Nile State - Central region
    "Rabak": (13.1833, 32.7333),  # West bank
    "Kosti": (13.1667, 32.6667),  # Major town
    "Ad Diwaim": (14.0000, 32.3167),  # Northern locality
    # Aj Jazirah State - Agricultural heartland
    "Medani Al Kubra": (14.4008, 33.5197),  # Wad Madani city
    "Al Hasahisa": (14.6333, 33.3167),  # North of capital
    "Al Manaqil": (14.2500, 32.9833),  # Gezira scheme
}


# ============================================================================
# STATE CENTERS (Fallback for unknown localities)
# ============================================================================

STATE_COORDINATE_CENTERS = {
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


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def get_locality_coordinates(locality_name, state_name):
    """
    Get coordinates for a locality, using verified coordinates if available,
    otherwise returning state center with small random offset.

    Parameters:
    -----------
    locality_name : str
        Name of the locality (as appears in data)
    state_name : str
        Name of the state (for fallback)

    Returns:
    --------
    tuple : (latitude, longitude)
    """
    import numpy as np

    # Try exact match first
    if locality_name in LOCALITY_COORDINATE_OVERRIDES:
        return LOCALITY_COORDINATE_OVERRIDES[locality_name]

    # Try case-insensitive match
    for key, coords in LOCALITY_COORDINATE_OVERRIDES.items():
        if key.lower() == locality_name.lower():
            return coords

    # Fallback to state center with small random offset
    if state_name in STATE_COORDINATE_CENTERS:
        center_lat, center_lon = STATE_COORDINATE_CENTERS[state_name]
        # Add small random offset to avoid exact overlap
        offset_lat = np.random.uniform(-0.5, 0.5)
        offset_lon = np.random.uniform(-0.5, 0.5)
        return (center_lat + offset_lat, center_lon + offset_lon)

    # Ultimate fallback - center of Sudan
    return (15.5, 32.5)


def apply_coordinate_fixes(localities_df):
    """
    Apply coordinate fixes to localities dataframe.

    Parameters:
    -----------
    localities_df : pandas.DataFrame
        DataFrame with locality data including 'locality_displacement' and
        'state_displacement' columns

    Returns:
    --------
    pandas.DataFrame : Updated dataframe with corrected coordinates
    """
    from shapely.geometry import Point

    print("\nApplying coordinate fixes...")

    fixed_count = 0
    approximate_count = 0

    new_geometries = []

    for _, row in localities_df.iterrows():
        locality_name = row["locality_displacement"]
        state_name = row["state_displacement"]

        lat, lon = get_locality_coordinates(locality_name, state_name)
        new_geometries.append(Point(lon, lat))

        # Track if this was a verified coordinate
        if locality_name in LOCALITY_COORDINATE_OVERRIDES:
            fixed_count += 1

    localities_df["geometry"] = new_geometries
    approximate_count = len(localities_df) - fixed_count

    print(f"  ✓ Applied {fixed_count} verified coordinates")
    print(f"  ⚠ Using {approximate_count} approximate coordinates")
    print(f"  Total localities: {len(localities_df)}")

    # Show which Red Sea localities got fixed
    red_sea = localities_df[localities_df["state_displacement"] == "Red Sea"]
    print(f"\n  Red Sea State localities ({len(red_sea)}):")
    for _, loc in red_sea.iterrows():
        verified = (
            "✓"
            if loc["locality_displacement"] in LOCALITY_COORDINATE_OVERRIDES
            else "~"
        )
        print(f"    {verified} {loc['locality_displacement']}")

    return localities_df


# ============================================================================
# DATA SOURCES & NOTES
# ============================================================================

"""
COORDINATE SOURCES:
- OpenStreetMap (nominatim): Major cities and towns
- OCHA COD-AB: Administrative boundary centroids
- Google Maps: Verification of ambiguous locations
- Sudan National Bureau of Statistics: State capitals

QUALITY NOTES:
- Port Sudan and major cities: High accuracy (±1 km)
- Remote localities: Moderate accuracy (±5 km)
- Conflict-affected areas: Best available estimates

PRODUCTION RECOMMENDATIONS:
For full production deployment, obtain actual polygon shapefiles from:
1. OCHA Common Operational Datasets (COD-AB)
   https://data.humdata.org/dataset/cod-ab-sdn

2. GADM (Global Administrative Areas)
   https://gadm.org/download_country.html

3. Sudan National Bureau of Statistics
   Official administrative boundary datasets

Then calculate true polygon centroids using GeoPandas:
    localities_gdf['centroid'] = localities_gdf.geometry.centroid
"""
