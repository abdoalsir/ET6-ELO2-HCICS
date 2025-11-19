"""
Complete Analysis Pipeline - HCICS MVP
Integrates descriptive geospatial analysis with inferential statistical validation.

This script runs the full analysis workflow:
    1. Crisis Analysis Core (geospatial proximity + vulnerability scoring)
    2. Inferential Analysis (spatial stats + ML + hypothesis testing)
    3. Visualization Generation (maps and reports)

Author: Claude AI
Date: November 16, 2025
"""

from pathlib import Path
import sys

# Add analysis modules to path
ANALYSIS_DIR = Path(__file__).parent
sys.path.insert(0, str(ANALYSIS_DIR))

# Track success/failure of each phase
pipeline_status = {
    "crisis_analysis": False,
    "inferential_analysis": False,
    "visualization": False,
}

print("\n" + "=" * 80)
print(" " * 20 + "HCICS MVP - COMPLETE ANALYSIS PIPELINE")
print(" " * 25 + "MIT Emerging Talent - Milestone 3")
print("=" * 80)

# ============================================================================
# PHASE 1: GEOSPATIAL CRISIS ANALYSIS
# ============================================================================

print("\n" + "🔵" * 40)
print("\nPHASE 1: RUNNING GEOSPATIAL CRISIS ANALYSIS...")
print("(Proximity metrics, vulnerability scoring, risk categorization)")
print("\n" + "🔵" * 40)

analysis_df = None
export_df = None

try:
    from crisis_analysis import main as run_crisis_analysis

    analysis_df, export_df = run_crisis_analysis()

    if analysis_df is None:
        print("\n❌ Crisis analysis failed. Cannot proceed.")
        sys.exit(1)

    print("\n✅ Phase 1 Complete: Geospatial analysis successful")
    pipeline_status["crisis_analysis"] = True

except ImportError as e:
    print(f"\n❌ Error: Could not import crisis_analysis module: {str(e)}")
    print("    Make sure crisis_analysis.py is in the same directory")
    sys.exit(1)

except Exception as e:
    print(f"\n❌ Error in Phase 1: {str(e)}")
    import traceback

    traceback.print_exc()
    sys.exit(1)


# ============================================================================
# PHASE 2: INFERENTIAL STATISTICAL ANALYSIS
# ============================================================================

print("\n" + "🟢" * 40)
print("\nPHASE 2: RUNNING INFERENTIAL ANALYSIS...")
print("(Spatial autocorrelation, ML validation, hypothesis testing)")
print("\n" + "🟢" * 40)

inferential_results = None

try:
    from inferential_analysis import run_inferential_analysis

    # Run inferential analysis using the results from Phase 1
    inferential_results = run_inferential_analysis(analysis_df)

    if inferential_results is None:
        print("\n⚠️  Warning: Inferential analysis encountered issues")
        print("    Continuing with visualization phase...")
    else:
        print("\n✅ Phase 2 Complete: Statistical validation successful")
        pipeline_status["inferential_analysis"] = True

except ImportError as e:
    print(f"\n⚠️  Warning: Could not import inferential_analysis module: {str(e)}")
    print("    Skipping statistical validation phase...")
    print("    Install required packages: pip install scikit-learn esda libpysal")

except Exception as e:
    print(f"\n⚠️  Warning: Inferential analysis failed: {str(e)}")
    print("    Continuing with visualization phase...")
    import traceback

    traceback.print_exc()


# ============================================================================
# PHASE 3: VISUALIZATION GENERATION
# ============================================================================

print("\n" + "🟡" * 40)
print("\nPHASE 3: GENERATING VISUALIZATIONS...")
print("(Maps, charts, and interactive dashboards)")
print("\n" + "🟡" * 40)

try:
    from visualization import generate_analysis_visualizations
    import geopandas as gpd

    # Load the exported GeoJSON data for visualization
    OUTPUT_PATH = Path("outputs")
    analysis_gdf = gpd.read_file(OUTPUT_PATH / "localities_vulnerability.geojson")
    facilities_gdf = gpd.read_file(OUTPUT_PATH / "health_facilities.geojson")

    generate_analysis_visualizations(analysis_gdf, facilities_gdf)

    print("\n✅ Phase 3 Complete: Visualizations generated")
    pipeline_status["visualization"] = True

except ImportError as e:
    print(f"\n⚠️  Warning: Could not import visualization module: {str(e)}")
    print("    Skipping visualization generation...")

except Exception as e:
    print(f"\n⚠️  Warning: Visualization generation encountered issues: {str(e)}")
    import traceback

    traceback.print_exc()


# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print(" " * 30 + "ANALYSIS COMPLETE!")
print("=" * 80)

# Pipeline status summary
print("\n📊 PIPELINE STATUS:")
for phase, success in pipeline_status.items():
    status = "✅ SUCCESS" if success else "⚠️  PARTIAL/SKIPPED"
    print(f"   {phase.replace('_', ' ').title()}: {status}")

print("\n📁 OUTPUT DIRECTORY STRUCTURE:")
print("   outputs/")
print("   ├── locality_vulnerability_analysis.csv    (Main results table)")
print("   ├── localities_vulnerability.geojson       (Map data)")
print("   ├── health_facilities.geojson              (Facility locations)")
print("   │")
print("   ├── maps/                                   (Visual outputs)")
print("   │   ├── vulnerability_index_map.png")
print("   │   ├── risk_categories_map.png")
print("   │   ├── accessibility_gap_map.png")
print("   │   └── interactive_vulnerability_map.html")
print("   │")
print("   └── inferential_analysis/                  (Statistical validation)")
print("       ├── morans_i_scatter.png")
print("       ├── feature_importance.png")
print("       ├── confusion_matrices.png")
print("       ├── regional_hypothesis_tests.png")
print("       └── inferential_analysis_report.txt")

# Display key statistics only if analysis succeeded
if export_df is not None:
    print("\n" + "=" * 80)
    print("📊 KEY FINDINGS SUMMARY")
    print("=" * 80)

    total_idps = export_df["total_idps"].sum()
    critical_localities = len(export_df[export_df["risk_category"] == "Critical"])
    mean_distance = export_df["dist_to_nearest_hospital_km"].mean()

    print("\n📍 GEOGRAPHIC SCOPE:")
    print(f"   • Total IDPs analyzed: {total_idps:,}")
    print(f"   • Localities assessed: {len(export_df)}")
    print(f"   • Critical risk localities: {critical_localities}")

    print("\n🏥 ACCESSIBILITY METRICS:")
    print(f"   • Mean distance to hospital: {mean_distance:.1f} km")
    print(
        f"   • Localities beyond 20km: {(export_df['dist_to_nearest_hospital_km'] > 20).sum()}"
    )

    # Top vulnerable localities
    print("\n🚨 TOP 5 MOST VULNERABLE LOCALITIES:")
    top_5 = export_df.nlargest(5, "vulnerability_index")[
        ["locality_name", "state_name", "vulnerability_index", "risk_category"]
    ]
    for i, (_, row) in enumerate(top_5.iterrows(), 1):
        print(f"   {i}. {row['locality_name']}, {row['state_name']}")
        print(
            f"      Score: {row['vulnerability_index']:.1f} | Risk: {row['risk_category']}"
        )

# Display inferential analysis key findings if available
if inferential_results:
    print("\n📈 STATISTICAL VALIDATION RESULTS:")

    # Spatial autocorrelation
    if inferential_results.get("spatial"):
        moran_i = inferential_results["spatial"]["statistic"]
        p_val = inferential_results["spatial"]["p_value"]
        print(f"   • Moran's I: {moran_i:.4f} (p = {p_val:.4f})")
        if p_val < 0.05:
            print("     → Significant geographic clustering detected")

    # Model accuracy
    if inferential_results.get("modeling"):
        rf_acc = inferential_results["modeling"]["random_forest"]["accuracy"]
        print(f"   • ML Prediction Accuracy: {rf_acc:.1%}")
        print("     → Vulnerability methodology validated")

        # Top predictors
        print("   • Top 3 Vulnerability Drivers:")
        for _, row in (
            inferential_results["modeling"]["feature_importance"].head(3).iterrows()
        ):
            print(f"     - {row['feature']}")

    # Regional comparison
    if inferential_results.get("hypothesis"):
        darfur_p = inferential_results["hypothesis"]["darfur_ttest"]["p_value"]
        if darfur_p < 0.05:
            print(
                f"   • Darfur vs Non-Darfur: SIGNIFICANT difference (p = {darfur_p:.4f})"
            )
        else:
            print(
                f"   • Darfur vs Non-Darfur: No significant difference (p = {darfur_p:.4f})"
            )

print("\n" + "=" * 80)

# Final message based on pipeline status
if all(pipeline_status.values()):
    print("✅ ANALYSIS PIPELINE COMPLETE - READY FOR MILESTONE 4 (DASHBOARD)")
elif pipeline_status["crisis_analysis"]:
    print("⚠️  ANALYSIS PARTIALLY COMPLETE - Core analysis succeeded")
    print("   Some optional components were skipped (see warnings above)")
else:
    print("❌ ANALYSIS INCOMPLETE - Review errors above")

print("=" * 80)

print("\n💡 NEXT STEPS:")
print("   1. Review outputs in the 'outputs/' directory")
if inferential_results:
    print("   2. Read inferential_analysis_report.txt for detailed findings")
print("   3. Open interactive_vulnerability_map.html in a browser")
print("   4. Proceed to Milestone 4: Dashboard implementation")

print("\n" + "=" * 80 + "\n")
