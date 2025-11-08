"""
A module for cleaning and preparing IDP (Internally Displaced Persons) data at
state and locality administrative levels.

Module contents:
    - clean_idps_locality_data: Cleans and processes raw IDP data at the locality level.
    - clean_idps_state_data: Cleans and processes raw IDP data at the state level.
    - generate_cleaning_summary: Prints a summary report comparing cleaned datasets
      and highlighting key indicators.

Created on 05-11-25
@author: Abdulrahman + Claude AI
"""

import pandas as pd
import numpy as np
from pathlib import Path

RAW_DATA_PATH = Path("../1_datasets/raw")
CLEAN_DATA_PATH = Path("../1_datasets/clean")

CLEAN_DATA_PATH.mkdir(parents=True, exist_ok=True)


def clean_idps_locality_data():
    """
    Cleans IDP data at the locality (administrative level 2) level.

    Steps:
        1. Loads the raw CSV file and removes unnecessary header rows.
        2. Drops records with missing displacement state information.
        3. Renames columns for consistency and readability.
        4. Converts numeric columns to integers and replaces missing values with 0.
        5. Derives key indicators including:
            - has_origin_breakdown
            - nationality_data_complete
            - average household size
            - non-Sudanese population percentage
        6. Exports the cleaned dataset to the 'clean' directory.

    Returns:
        pd.DataFrame: The cleaned locality-level IDP dataset.

    Raises:
        FileNotFoundError: If the raw data file is missing.
        KeyError: If expected columns are not found in the dataset.
    """

    df = pd.read_csv(RAW_DATA_PATH / "raw_idps_locality_data.csv", skiprows=3)
    df = df[~df.iloc[:, 0].astype(str).str.startswith("#")].reset_index(drop=True)
    drop_cols = [
        "ADM2_REF",
        "ADM2ALT1_EN",
        "ADM2ALT2_EN",
        "ADM2ALT1_AR",
        "ADM2ALT2_AR",
        "VALIDTO",
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    df = df.dropna(subset=["STATE OF DISPLACEMET"])

    column_mapping = {
        "STATE OF DISPLACEMET": "state_displacement",
        "STATE CODE": "state_code",
        "LOCALITY OF DISPLACEMENT": "locality_displacement",
        "LOCALITY CODE": "locality_code",
        "IDPs": "total_idps",
        "HHs": "total_households",
        "  SUDANESE  ": "sudanese_nationals",
        " NON SUDANESE": "non_sudanese_nationals",
    }

    df = df.rename(columns=column_mapping)

    origin_cols = [
        "Aj Jazirah",
        "Central Darfur",
        "East Darfur",
        "Khartoum",
        "North Darfur",
        "North Kordofan",
        "Sennar",
        "South Darfur",
        "South Kordofan",
        "West Darfur",
        "West Kordofan",
        "White Nile",
    ]

    origin_mapping = {
        col: f"origin_{col.lower().replace(' ', '_')}" for col in origin_cols
    }
    df = df.rename(columns=origin_mapping)

    numeric_cols = [
        "total_idps",
        "total_households",
        "sudanese_nationals",
        "non_sudanese_nationals",
    ]
    numeric_cols.extend(origin_mapping.values())

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df["has_origin_breakdown"] = (
        df[[col for col in df.columns if col.startswith("origin_")]].sum(axis=1) > 0
    )

    df["nationality_data_complete"] = (
        df["sudanese_nationals"] + df["non_sudanese_nationals"] == df["total_idps"]
    )

    df["avg_household_size"] = np.where(
        df["total_households"] > 0, df["total_idps"] / df["total_households"], np.nan
    )

    df["non_sudanese_percentage"] = np.where(
        df["total_idps"] > 0, (df["non_sudanese_nationals"] / df["total_idps"]) * 100, 0
    )

    output_path = CLEAN_DATA_PATH / "clean_idps_locality.csv"
    df.to_csv(output_path, index=False)

    return df


def clean_idps_state_data():
    """
    Cleans IDP data at the state (administrative level 1) level.

    Steps:
        1. Loads raw CSV data and drops invalid records.
        2. Standardizes column names.
        3. Converts numeric data types and fills missing values.
        4. Calculates:
            - Average household size
            - Non-Sudanese percentage
            - IDP concentration by state
        5. Exports the cleaned state-level dataset.

    Returns:
        pd.DataFrame: The cleaned state-level IDP dataset.

    Raises:
        FileNotFoundError: If the raw data file is missing.
        KeyError: If expected columns are not found.
    """

    df = pd.read_csv(RAW_DATA_PATH / "raw_idps_state_data.csv", skiprows=3)
    df = df[~df.iloc[:, 0].astype(str).str.startswith("#")].reset_index(drop=True)

    df = df.dropna(subset=["STATE OF DISPLACEMET"])

    column_mapping = {
        "STATE OF DISPLACEMET": "state_displacement",
        "STATE CODE": "state_code",
        "IDPs": "total_idps",
        "HHs": "total_households",
        "  SUDANESE  ": "sudanese_nationals",
        " NON SUDANESE": "non_sudanese_nationals",
    }

    df = df.rename(columns=column_mapping)

    origin_cols = [
        "Aj Jazirah",
        "Central Darfur",
        "East Darfur",
        "Khartoum",
        "North Darfur",
        "North Kordofan",
        "Sennar",
        "South Darfur",
        "South Kordofan",
        "West Darfur",
        "West Kordofan",
        "White Nile",
    ]

    origin_mapping = {
        col: f"origin_{col.lower().replace(' ', '_')}" for col in origin_cols
    }
    df = df.rename(columns=origin_mapping)

    numeric_cols = [
        "total_idps",
        "total_households",
        "sudanese_nationals",
        "non_sudanese_nationals",
    ]
    numeric_cols.extend(origin_mapping.values())

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    df["avg_household_size"] = np.where(
        df["total_households"] > 0, df["total_idps"] / df["total_households"], np.nan
    )

    df["non_sudanese_percentage"] = np.where(
        df["total_idps"] > 0, (df["non_sudanese_nationals"] / df["total_idps"]) * 100, 0
    )

    total_all_idps = df["total_idps"].sum()
    df["displacement_concentration_pct"] = df["total_idps"] / total_all_idps * 100

    output_path = CLEAN_DATA_PATH / "clean_idps_state.csv"
    df.to_csv(output_path, index=False)

    return df


def generate_cleaning_summary(locality_df, state_df):
    """
    Generate a concise summary report of the cleaning process results.

    Args:
        locality_df: Cleaned locality-level dataframe
        state_df: Cleaned state-level dataframe
    """
    print("DATA CLEANING SUMMARY: ")

    print("\nLOCALITY-LEVEL DATA (Cleaned):")
    print(f" • Records: {len(locality_df):,}")
    print(f" • Unique states: {locality_df['state_displacement'].nunique()}")
    print(f" • Unique localities: {locality_df['locality_displacement'].nunique()}")
    print(f" • Total IDPs: {locality_df['total_idps'].sum():,}")
    print(f" • Avg. household size: {locality_df['avg_household_size'].mean():.2f}")

    print("\nSTATE-LEVEL DATA (Cleaned):")
    print(f" • Records: {len(state_df):,}")
    print(f" • Total IDPs: {state_df['total_idps'].sum():,}")
    print(f" • Avg. household size: {state_df['avg_household_size'].mean():.2f}")

    print("\nDATA QUALITY CHECK:")
    locality_total = locality_df["total_idps"].sum()
    state_total = state_df["total_idps"].sum()
    if locality_total == state_total:
        print(" • Locality totals match state totals: ✓ PASS")
    else:
        print(
            f" • Locality totals match state totals: ✗ FAIL (Difference: {abs(locality_total - state_total):,})"
        )

    print("\nTOP 3 STATES BY IDP CONCENTRATION:")
    top_states = state_df.nlargest(3, "total_idps")[
        ["state_displacement", "total_idps", "displacement_concentration_pct"]
    ]
    for _, row in top_states.iterrows():
        print(
            f" • {row['state_displacement']}: "
            f"{row['total_idps']:,} IDPs "
            f"({row['displacement_concentration_pct']:.1f}%)"
        )

    print("\n" + "=" * 30)


if __name__ == "__main__":
    locality_df = clean_idps_locality_data()
    state_df = clean_idps_state_data()

    generate_cleaning_summary(locality_df, state_df)
