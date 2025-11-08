"""
A module for cleaning and preparing local geospatial health facilities data
sourced from Humanitarian OpenStreetMap Team (HOT OSM) via a pre-downloaded
shapefile ZIP archive.

Module contents:
    - extract_shapefile_from_local_zip: Extracts a .shp file from a local ZIP archive.
    - generate_generic_name: Generates simple names for unnamed facilities.
    - enhance_facility_names: Processes names and translates to English.
    - clean_health_facilities: Main function orchestrating local extraction,
      geospatial processing (GeoPandas), attribute cleaning, and filtering.
    - generate_facilities_summary: Prints and saves a summary report of the
      cleaned facilities data.

Input:
    raw_health_facilities.zip (pre-downloaded shapefile archive)

Output:
    clean_health_facilities.csv (cleaned facilities data)
    facilities_summary.csv (summary report)

Created on 2025-11-05
@author:
    Abdulrahman Ali + Claude AI
"""

import shutil
import time
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
from deep_translator import GoogleTranslator

RAW_DATA_PATH = Path("../1_datasets/raw")
CLEAN_DATA_PATH = Path("../1_datasets/clean")
LOCAL_ZIP_FILENAME = "raw_health_facilities.zip"

CLEAN_DATA_PATH.mkdir(parents=True, exist_ok=True)


def extract_shapefile_from_local_zip(zip_path: Path, output_dir: Path) -> Path:
    """Extract a .shp file from a local ZIP archive.

    Args:
        zip_path: Path to the local ZIP archive file.
        output_dir: Temporary directory to extract files into.

    Returns:
        Path to the extracted shapefile.

    Raises:
        zipfile.BadZipFile: If the file is corrupted.
        FileNotFoundError: If no .shp file is found after extraction.
    """
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(output_dir)

    shp_files = list(output_dir.glob("*.shp"))
    if shp_files:
        return shp_files[0]

    shutil.rmtree(output_dir, ignore_errors=True)
    raise FileNotFoundError("No .shp file found in the extracted archive.")


def generate_generic_name(row: pd.Series) -> str:
    """Generate a generic name for facilities missing names.

    Args:
        row: DataFrame row containing facility data.

    Returns:
        Generated generic name, e.g., "Unnamed Hospital".
    """
    facility_type = row.get("facility_type_standard", "facility").capitalize()
    return f"Unnamed {facility_type}"


def translate_arabic_to_english(text: str | None) -> str | None:
    """Translate Arabic text to English using deep-translator.

    Args:
        text: Arabic text to translate.

    Returns:
        Translated English text, or original text if translation fails.
    """
    if not text or not isinstance(text, str):
        return None

    if not any("\u0600" <= char <= "\u06ff" for char in text):
        return text

    translator = GoogleTranslator(source="ar", target="en")
    return translator.translate(text)


def add_english_translation(df: pd.DataFrame, batch_size: int = 50) -> pd.DataFrame:
    """Add English translations for Arabic facility names.

    Args:
        df: DataFrame with facility data.
        batch_size: Number of translations before pausing.

    Returns:
        DataFrame with 'facility_name_english' column added.
    """
    print("\n" + "=" * 50)
    print("TRANSLATING FACILITY NAMES")
    print("=" * 50)

    df["facility_name_english"] = None
    needs_translation = df["facility_name"].notna() & df["has_original_name"]
    translation_indices = df[needs_translation].index.tolist()

    total = len(translation_indices)
    print(f"\nFound {total} facility names to translate...")
    print("This may take several minutes...\n")

    successful = 0
    failed = 0

    for i, idx in enumerate(translation_indices, 1):
        if i % 50 == 0 or i == 1:
            print(
                f"Progress: {i}/{total} ({i / total * 100:.1f}%) | "
                f"Success: {successful} | Failed: {failed}"
            )

        if i > 1 and i % batch_size == 0:
            time.sleep(2)

        arabic_name = df.loc[idx, "facility_name"]
        english_name = translate_arabic_to_english(arabic_name)

        if english_name and english_name != arabic_name:
            df.loc[idx, "facility_name_english"] = english_name
            successful += 1
            if successful <= 3:
                print(f"  ✓ {arabic_name} → {english_name}")
        else:
            df.loc[idx, "facility_name_english"] = arabic_name
            failed += 1

    print("\n" + "=" * 50)
    print("✓ Translation complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed/Kept original: {failed}")
    print("=" * 50 + "\n")

    df["facility_name_display"] = df.apply(
        lambda row: (
            row["facility_name_english"]
            if pd.notna(row["facility_name_english"])
            else row.get("facility_name_generated", "Unnamed Facility")
        ),
        axis=1,
    )
    return df


def enhance_facility_names(df: pd.DataFrame) -> pd.DataFrame:
    """Enhance facility names: fill missing and translate Arabic ones.

    Args:
        df: DataFrame with facility data.

    Returns:
        Enhanced DataFrame with English translations.
    """
    missing_names = df["facility_name"].isna() | (df["facility_name"] == "")
    df.loc[missing_names, "facility_name_generated"] = df[missing_names].apply(
        generate_generic_name,
        axis=1,
    )

    df["facility_name_display"] = df.apply(
        lambda row: (
            row["facility_name"]
            if pd.notna(row["facility_name"]) and row["facility_name"] != ""
            else row.get("facility_name_generated", "Unnamed Facility")
        ),
        axis=1,
    )

    df["has_original_name"] = df["has_name"].copy()
    df = add_english_translation(df, batch_size=50)
    return df


def clean_health_facilities() -> pd.DataFrame:
    """Clean and process raw health facilities data from a local zip file.

    Steps:
        1. Extract shapefile locally.
        2. Read shapefile into GeoDataFrame.
        3. Extract coordinates.
        4. Rename and standardize columns.
        5. Classify and clean facility types.
        6. Add quality flags.
        7. Translate Arabic names.
        8. Filter to Sudan’s bounding box.
        9. Save cleaned CSV.

    Returns:
        Cleaned and geographically filtered facilities DataFrame.
    """
    local_zip_path = RAW_DATA_PATH / LOCAL_ZIP_FILENAME
    temp_dir = RAW_DATA_PATH / "temp_facilities"
    temp_dir.mkdir(exist_ok=True)

    shp_path = extract_shapefile_from_local_zip(local_zip_path, temp_dir)
    gdf = gpd.read_file(shp_path)

    gdf["longitude"] = gdf.geometry.x
    gdf["latitude"] = gdf.geometry.y

    column_mapping = {
        "name": "facility_name",
        "amenity": "facility_type",
        "healthcare": "healthcare_type",
        "operator": "operator_name",
        "operator:t": "operator_type",
        "source": "data_source",
        "addr:city": "city",
        "addr:state": "state",
    }
    existing_mapping = {k: v for k, v in column_mapping.items() if k in gdf.columns}
    gdf = gdf.rename(columns=existing_mapping)
    df = pd.DataFrame(gdf.drop(columns="geometry"))

    if "facility_type" in df.columns:
        df["facility_type"] = df["facility_type"].str.lower().str.strip()
        type_mapping = {
            "clinic": "clinic",
            "hospital": "hospital",
            "doctors": "clinic",
            "health_post": "health_post",
            "pharmacy": "pharmacy",
            "dentist": "dental_clinic",
        }
        df["facility_type_standard"] = (
            df["facility_type"].map(type_mapping).fillna("other")
        )
    else:
        df["facility_type_standard"] = "unknown"

    if "facility_name" in df.columns:
        df["facility_name"] = df["facility_name"].str.strip()
        df["has_name"] = df["facility_name"].notna()
    else:
        df["facility_name"] = None
        df["has_name"] = False

    df["coordinates_valid"] = df["longitude"].between(-180, 180) & df[
        "latitude"
    ].between(-90, 90)

    df["location_precision"] = df.apply(
        lambda row: (
            "high"
            if row["has_name"] and row["coordinates_valid"]
            else "medium"
            if row["coordinates_valid"]
            else "low"
        ),
        axis=1,
    )

    df = enhance_facility_names(df)

    df_filtered = df[
        (df["longitude"].between(21.8, 39.0)) & (df["latitude"].between(3.0, 23.0))
    ].copy()

    output_cols = [
        "facility_name",
        "facility_name_english",
        "facility_name_display",
        "facility_type_standard",
        "longitude",
        "latitude",
        "has_original_name",
        "coordinates_valid",
        "location_precision",
    ]

    optional_cols = ["operator_name", "operator_type", "city", "state"]
    for col in optional_cols:
        if col in df_filtered.columns:
            output_cols.append(col)

    df_clean = df_filtered[output_cols].copy()
    output_path = CLEAN_DATA_PATH / "clean_health_facilities.csv"
    df_clean.to_csv(output_path, index=False, encoding="utf-8-sig")

    shutil.rmtree(temp_dir, ignore_errors=True)
    return df_clean


def generate_facilities_summary(df: pd.DataFrame) -> None:
    """Generate and print a summary report for the cleaned facilities data."""
    print("\nHEALTH FACILITIES SUMMARY")
    print("-" * 25)
    print(f"Total facilities: {len(df):,}")
    print(f"Facilities with names: {df['has_original_name'].sum():,}")

    type_summary = df["facility_type_standard"].value_counts()
    print("\nFacility Types:")
    print(type_summary)

    summary_data = {
        "metric": [
            "total_facilities",
            "facilities_with_names",
            "high_precision_locations",
            "hospitals",
            "clinics",
            "other_facilities",
        ],
        "value": [
            len(df),
            df["has_original_name"].sum(),
            (df["location_precision"] == "high").sum(),
            (df["facility_type_standard"] == "hospital").sum(),
            (df["facility_type_standard"] == "clinic").sum(),
            (
                (df["facility_type_standard"] != "hospital")
                & (df["facility_type_standard"] != "clinic")
            ).sum(),
        ],
    }

    summary_df = pd.DataFrame(summary_data)
    summary_path = CLEAN_DATA_PATH / "facilities_summary.csv"
    summary_df.to_csv(summary_path, index=False)


if __name__ == "__main__":
    facilities_df = clean_health_facilities()
    generate_facilities_summary(facilities_df)
