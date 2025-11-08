"""
A module for cleaning and preparing Sudan administrative boundaries data
(Administrative Levels 0–2) for geospatial analysis.

Module contents:
    - clean_boundaries_data: Cleans and standardizes raw boundaries data.
    - generate_state_summary: Generates summary statistics by state.
    - create_lookup_tables: Creates lookup tables for states and localities.

Input: raw_boundaries_data.csv (raw gazetteer data)
Output:
    - clean_boundaries_admin2.csv (cleaned dataset)
    - boundaries_state_summary.csv (summary statistics)
    - lookup_states.csv (state-level reference table)
    - lookup_localities.csv (locality-level reference table)

Created on 07-11-25
@author: Gemini Assistant
"""

import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path("../1_datasets/raw")
CLEAN_DATA_PATH = Path("../1_datasets/clean")

CLEAN_DATA_PATH.mkdir(parents=True, exist_ok=True)


def clean_boundaries_data() -> pd.DataFrame:
    """
    Clean and prepare Sudan administrative boundaries data.

    Steps:
        1. Read raw boundaries CSV.
        2. Rename and standardize column names.
        3. Convert date and area columns to proper data types.
        4. Clean and strip text and code columns.
        5. Add derived columns (size category, standardized names, special areas).
        6. Save cleaned data to CSV.

    Returns:
        pd.DataFrame: Cleaned administrative boundaries at level 2.
    """
    df = pd.read_csv(RAW_DATA_PATH / "raw_boundaries_data.csv")
    drop_cols = [
        "ADM2_REF",
        "ADM2ALT1_EN",
        "ADM2ALT2_EN",
        "ADM2ALT1_AR",
        "ADM2ALT2_AR",
        "VALIDTO",
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    column_mapping = {
        "ADM2_EN": "locality_name_en",
        "ADM2_AR": "locality_name_ar",
        "ADM2_PCODE": "locality_code",
        "ADM1_EN": "state_name_en",
        "ADM1_AR": "state_name_ar",
        "ADM1_PCODE": "state_code",
        "ADM0_EN": "country_name_en",
        "ADM0_AR": "country_name_ar",
        "ADM0_PCODE": "country_code",
        "DATE": "data_date",
        "VALIDON": "valid_from",
        "AREA_SQKM": "area_sqkm",
    }

    df = df.rename(columns=column_mapping)

    date_cols = ["data_date", "valid_from"]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    df["area_sqkm"] = pd.to_numeric(df["area_sqkm"], errors="coerce")

    text_cols = [c for c in df.columns if ("name" in c or "alt" in c)]
    code_cols = ["locality_code", "state_code", "country_code", "locality_ref"]

    for col in text_cols:
        df[col] = df[col].fillna("").astype(str).str.strip()

    if "country_name_en" in df.columns:
        df["country_name_en"] = (
            df["country_name_en"]
            .str.replace(r"\s*\(the\)\s*", "", regex=True)
            .str.strip()
        )
    for col in code_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df["size_category"] = pd.cut(
        df["area_sqkm"],
        bins=[0, 1000, 5000, 20000, float("inf")],
        labels=["Small", "Medium", "Large", "Very Large"],
    )

    df["state_name_standardized"] = df["state_name_en"].str.strip()
    df["is_special_admin"] = df["state_name_en"].str.contains("Abyei PCA", na=False)

    output_path = CLEAN_DATA_PATH / "clean_boundaries_data.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    return df


def generate_state_summary(df: pd.DataFrame):
    """
    Generate summary statistics of localities grouped by state.

    Parameters:
        df (pd.DataFrame): Cleaned boundaries dataframe.

    Outputs:
        boundaries_state_summary.csv — summary table with:
            - Number of localities per state
            - Total area (sq km)
            - Average locality area
    """
    summary = (
        df.groupby("state_name_en")
        .agg({"locality_name_en": "count", "area_sqkm": ["sum", "mean"]})
        .round(2)
    )

    summary.columns = ["num_localities", "total_area_sqkm", "avg_locality_area"]
    summary = summary.sort_values("total_area_sqkm", ascending=False)

    summary_path = CLEAN_DATA_PATH / "boundaries_state_summary.csv"
    summary.to_csv(summary_path)


def create_lookup_tables(df: pd.DataFrame):
    """
    Create lookup tables for states and localities.

    Parameters:
        df (pd.DataFrame): Cleaned boundaries dataframe.

    Outputs:
        lookup_states.csv — unique state reference table.
        lookup_localities.csv — detailed locality reference table.
    """
    state_lookup = (
        df[["state_code", "state_name_en", "state_name_ar", "state_name_standardized"]]
        .drop_duplicates()
        .sort_values("state_code")
    )

    state_lookup.to_csv(
        CLEAN_DATA_PATH / "lookup_states.csv", index=False, encoding="utf-8-sig"
    )

    locality_lookup = df[
        [
            "locality_code",
            "locality_name_en",
            "locality_name_ar",
            "state_code",
            "state_name_en",
            "area_sqkm",
            "size_category",
        ]
    ].sort_values(["state_code", "locality_code"])

    locality_lookup.to_csv(
        CLEAN_DATA_PATH / "lookup_localities.csv", index=False, encoding="utf-8-sig"
    )


if __name__ == "__main__":
    data = clean_boundaries_data()
    generate_state_summary(data)
    create_lookup_tables(data)
