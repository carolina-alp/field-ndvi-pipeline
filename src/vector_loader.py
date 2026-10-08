from pathlib import Path
from typing import Union, List
import geopandas as gpd
from shapely.geometry import box

def load_input_geometry(
    source: Union[str, Path, List[float], tuple]
) -> gpd.GeoDataFrame:
    """
    Flexible vector ingestion engine. Accepts Shapefiles (.shp), GeoJSON (.geojson),
    GeoPackages (.gpkg), or a raw Bounding Box list/tuple [minx, miny, maxx, maxy].
    Automatically reprojects input geometries to WGS84 (EPSG:4326) for STAC compatibility.
    """
    # Case 1: Raw Bounding Box coordinates [min_lon, min_lat, max_lon, max_lat]
    if isinstance(source, (list, tuple)):
        if len(source) != 4:
            raise ValueError(
                "Bounding box coordinate input must contain exactly 4 numbers: [minx, miny, maxx, maxy]"
            )
        geom = box(*source)
        return gpd.GeoDataFrame({"field_id": ["bbox_field_01"]}, geometry=[geom], crs="EPSG:4326")

    # Case 2: File path input (.shp, .geojson, .gpkg)
    source_path = Path(source)
    if not source_path.exists():
        raise FileNotFoundError(f"Vector source file not found at path: {source_path.resolve()}")

    print(f"📥 Loading spatial data from: {source_path.name}")
    gdf = gpd.read_file(source_path)

    # Validate & reproject CRS to EPSG:4326
    if gdf.crs is None:
        print("⚠️ Warning: No CRS found in input data. Defaulting to EPSG:4326 (WGS84).")
        gdf.set_crs(epsg=4326, inplace=True)
    elif gdf.crs.to_epsg() != 4326:
        print(f"🔄 Reprojecting input geometries from {gdf.crs.to_string()} to EPSG:4326 (WGS84)...")
        gdf = gdf.to_crs(epsg=4326)

    return gdf