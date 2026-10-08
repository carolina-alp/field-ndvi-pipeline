import numpy as np
from src.pipeline import calculate_ndvi
from src.vector_loader import load_input_geometry

def test_calculate_ndvi_valid():
    nir = np.array([0.8, 0.6])
    red = np.array([0.2, 0.1])
    expected = np.array([0.6, 0.71428571])

    result = calculate_ndvi(nir, red)
    np.testing.assert_allclose(result, expected, rtol=1e-5)

def test_calculate_ndvi_zero_division():
    nir = np.array([0.0])
    red = np.array([0.0])
    result = calculate_ndvi(nir, red)
    assert result[0] == 0.0

def test_load_input_geometry_bbox():
    bbox = [-66.12, -17.40, -66.11, -17.38]
    gdf = load_input_geometry(bbox)
    assert len(gdf) == 1
    assert gdf.crs.to_epsg() == 4326