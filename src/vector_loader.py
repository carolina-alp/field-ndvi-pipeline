import json
from pathlib import Path
from typing import Union, List
import geopandas as gpd
from shapely.geometry import Point, box


def load_input_geometry(
    source: Union[str, Path, List[float]], buffer_meters: float = 30.0
) -> gpd.GeoDataFrame:
    """
    Loads spatial geometry from a GeoJSON/Shapefile path, a Point [lon, lat],
    or a Bounding Box [min_lon, min_lat, max_lon, max_lat].
    """
    # 1. Convert string list representation "[lon, lat]" to Python list
    if isinstance(source, str) and source.startswith("[") and source.endswith("]"):
        try:
            source = json.loads(source)
        except json.JSONDecodeError:
            pass

    # 2. Handle single Point [lon, lat]
    if isinstance(source, (list, tuple)) and len(source) == 2:
        lon, lat = [float(c) for c in source]
        # Create Point and convert to UTM projection to add buffer in meters
        gdf_point = gpd.GeoDataFrame([{"geometry": Point(lon, lat)}], crs="EPSG:4326")
        
        # Estimate UTM zone automatically to apply meter-based buffer
        utm_crs = gdf_point.estimate_utm_crs()
        gdf_buffered = gdf_point.to_crs(utm_crs)
        gdf_buffered["geometry"] = gdf_buffered.buffer(buffer_meters)
        
        # Convert back to EPSG:4326 for STAC catalog query
        gdf = gdf_buffered.to_crs(epsg=4326)
        gdf["field_id"] = "Target_Point"
        gdf["crop"] = "Unknown"
        return gdf

    # 3. Handle Bounding Box [min_lon, min_lat, max_lon, max_lat]
    if isinstance(source, (list, tuple)) and len(source) == 4:
        min_lon, min_lat, max_lon, max_lat = [float(coord) for coord in source]
        geom = box(min_lon, min_lat, max_lon, max_lat)
        gdf = gpd.GeoDataFrame(
            [{"field_id": "Target_Field", "crop": "Unknown", "geometry": geom}],
            crs="EPSG:4326",
        )
        return gdf

    # 4. Handle File Path (.geojson / .shp)
    source_path = Path(source)
    if not source_path.exists():
        raise FileNotFoundError(
            f"Vector source file not found at path: {source_path.resolve()}"
        )

    gdf = gpd.read_file(source_path)
    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)

    return gdf