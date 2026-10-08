import geopandas as gpd
import pytest
from shapely.geometry import Polygon
from src.vector_loader import load_input_geometry


def test_load_input_geometry_single_point():
    """Prueba que un punto [lon, lat] genere un GeoDataFrame valido con buffer."""
    point_input = "[4.61825, 50.66153]"
    gdf = load_input_geometry(point_input, buffer_meters=30.0)

    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == 1
    assert gdf.crs.to_epsg() == 4326
    assert gdf.iloc[0]["field_id"] == "Target_Point"
    # El resultado debe ser un Polygon producto del buffer
    assert isinstance(gdf.geometry.iloc[0], Polygon)


def test_load_input_geometry_bbox():
    """Prueba que un BBOX [min_lon, min_lat, max_lon, max_lat] genere un GeoDataFrame."""
    bbox_input = "[4.61725, 50.66053, 4.61925, 50.66253]"
    gdf = load_input_geometry(bbox_input)

    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == 1
    assert gdf.crs.to_epsg() == 4326
    assert gdf.iloc[0]["field_id"] == "Target_Field"
    assert isinstance(gdf.geometry.iloc[0], Polygon)


def test_load_input_geometry_invalid_file():
    """Prueba que una ruta inexistente devuelva FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_input_geometry("path/to/non_existent_file.geojson")