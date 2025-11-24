"""
Configuration module managing constants, file paths, and data loading operations.

Module contents:
    - load_geojson_data: Caches and loads spatial data for localities and facilities.
    - load_csv_data: Caches and loads the tabular vulnerability analysis results.
    - load_logo: Handles the secure loading and base64 encoding of the project logo.
    - RISK_COLORS: Dictionary defining the color scheme for risk categories.
    - OUTPUT_PATH: Path object pointing to the data directory.

Created on 05-11-25
@author: Abdulrahman Sirelkhatim
"""

from pathlib import Path
import streamlit as st
import pandas as pd
import geopandas as gpd
import base64
from io import BytesIO

OUTPUT_PATH = Path("../4_data_analysis/outputs")

RISK_COLORS = {
    "Critical": "#d32f2f",
    "High": "#f57c00",
    "Moderate": "#fbc02d",
    "Low": "#388e3c",
}


@st.cache_data
def load_geojson_data():
    """
    Loads and caches geospatial datasets for the dashboard.

    Steps:
        1. Reads the localities vulnerability GeoJSON file.
        2. Reads the health facilities GeoJSON file.
        3. Utilizes Streamlit's caching mechanism to optimize performance.
        4. Catches and reports file I/O exceptions.

    Returns:
        tuple: A tuple containing (localities_gdf, facilities_gdf) as GeoDataFrames.
               Returns (None, None) if loading fails.
    """
    try:
        localities_gdf = gpd.read_file(OUTPUT_PATH / "localities_vulnerability.geojson")
        facilities_gdf = gpd.read_file(OUTPUT_PATH / "health_facilities.geojson")
        return localities_gdf, facilities_gdf
    except Exception as e:
        st.error(f"Error loading GeoJSON data: {str(e)}")
        return None, None


@st.cache_data
def load_csv_data():
    """
    Loads and caches the tabular analysis results.

    Steps:
        1. Reads the CSV file containing locality vulnerability scores.
        2. Utilizes Streamlit's caching mechanism.
        3. Catches and reports file I/O exceptions.

    Returns:
        pd.DataFrame: The analysis dataframe, or None if loading fails.
    """
    try:
        analysis_df = pd.read_csv(OUTPUT_PATH / "locality_vulnerability_analysis.csv")
        return analysis_df
    except Exception as e:
        st.error(f"Error loading CSV data: {str(e)}")
        return None


@st.cache_data
def load_logo():
    """
    Processes the application logo for web display.

    Steps:
        1. Verifies the existence of the logo image file.
        2. Resizes the image using LANCZOS resampling if width exceeds 800px.
        3. Encodes the image to a Base64 string for embedding in HTML components.
        4. Handles file not found or processing errors gracefully.

    Returns:
        tuple: (PIL.Image, str) containing the image object and its Base64 data URI.
               Returns (None, None) on error.
    """
    try:
        logo_path = Path("assets/logo.png")
        if not logo_path.exists():
            print("Logo loading error: assets/logo.png not found.")
            return None, None

        from PIL import Image

        img_pil = Image.open(logo_path)

        if img_pil.width > 800:
            ratio = 800 / img_pil.width
            new_height = int(img_pil.height * ratio)

            img_pil = img_pil.resize((800, new_height), Image.Resampling.LANCZOS)

        buffered = BytesIO()
        img_pil.save(buffered, format="PNG")
        encoded_string = base64.b64encode(buffered.getvalue()).decode()
        logo_base64_uri = f"data:image/png;base64,{encoded_string}"

        return img_pil, logo_base64_uri
    except Exception as e:
        print(f"Logo loading error: {e}")
        return None, None
