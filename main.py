import argparse
from src.pipeline import process_field_ndvi

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cloud-Native Agricultural Field NDVI Processing Engine"
    )
    parser.add_argument(
        "--source",
        type=str,
        default="data/sample_fields.geojson",
        help="Path to Shapefile (.shp), GeoJSON (.geojson), or GeoPackage (.gpkg)"
    )
    parser.add_argument("--start-date", type=str, default="2024-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, default="2024-03-30", help="End date (YYYY-MM-DD)")

    args = parser.parse_args()

    print("🚀 Starting Cloud-Native Field NDVI Pipeline...")
    df_results = process_field_ndvi(args.source, args.start_date, args.end_date)
    
    print("\n📊 Processed Zonal Results:")
    print(df_results.to_string(index=False))