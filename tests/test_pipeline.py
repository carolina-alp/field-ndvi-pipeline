import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from src.pipeline import process_ndvi_time_series
from src.vector_loader import load_input_geometry


def test_load_input_geometry_single_point():
    """Prueba la carga de entrada con un punto único [lon, lat]."""
    point_input = "[4.61825, 50.66153]"
    gdf = load_input_geometry(point_input, buffer_meters=30.0)

    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == 1
    assert gdf.crs.to_epsg() == 4326
    assert gdf.iloc[0]["field_id"] == "Target_Point"
    assert isinstance(gdf.geometry.iloc[0], Polygon)


def test_load_input_geometry_bbox():
    """Prueba la carga de entrada con un BBOX [min_lon, min_lat, max_lon, max_lat]."""
    bbox_input = "[4.61725, 50.66053, 4.61925, 50.66253]"
    gdf = load_input_geometry(bbox_input)

    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == 1
    assert gdf.crs.to_epsg() == 4326
    assert gdf.iloc[0]["field_id"] == "Target_Field"
    assert isinstance(gdf.geometry.iloc[0], Polygon)


def test_load_input_geometry_invalid_file():
    """Prueba que una ruta de archivo inexistente lance FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_input_geometry("path/to/non_existent_file.geojson")


def test_process_ndvi_time_series_returns_dataframe():
    """Prueba la ejecución general del pipeline para un rango corto."""
    bbox_input = "[4.61725, 50.66053, 4.61925, 50.66253]"
    df = process_ndvi_time_series(
        source=bbox_input, start_date="2026-03-01", end_date="2026-04-30"
    )

    assert df is not None
    assert "mean_ndvi" in df.columns
    assert "year_month" in df.columns