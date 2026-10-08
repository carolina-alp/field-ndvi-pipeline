# 🌾 Cloud-Native Agricultural Field NDVI Pipeline

[![CI Pipeline](https://github.com/carolina-alp/field-ndvi-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/carolina-alp/field-ndvi-pipeline/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-green.svg)](https://www.python.org/)


An end-to-end cloud-native pipeline for processing Sentinel-2 STAC imagery to extract and visualize phenological NDVI time series for agricultural fields, custom bounding boxes, or single point coordinates.

---

## Features

- **Flexible Input Support**: Load spatial geometries directly from:
  - Vector files (`.geojson`, `.shp`).
  - Bounding Box arrays (`[min_lon, min_lat, max_lon, max_lat]`).
  - Single Coordinates (`[lon, lat]`) with automatic meter-based buffering.
- **STAC Catalog Integration**: Dynamically queries AWS Sentinel-2 L2A STAC collections via `pystac-client`.
- **Monthly Aggregation**: Computes monthly mean NDVI values across target spatial regions.
- **Automated Visualization**: Generates high-resolution phenological curve plots with dynamic X-axis labeling and agronomic baseline thresholds (Bare Soil vs Peak Canopy).
- **Dockerized Environment**: Fully containerized pipeline eliminating C-dependency setup issues (`GDAL`/`fiona`/`geopandas`).
- **Automated Testing**: Integrated `pytest` suite ensuring robust vector loading and pipeline performance.

---

## Tech Stack

* **Python 3.11**
* **Geospatial**: `geopandas`, `shapely`, `fiona`, `rasterio`
* **STAC & Raster Processing**: `pystac-client`, `stackstac`, `xarray`
* **Data & Visualization**: `pandas`, `matplotlib`
* **Testing & Containerization**: `pytest`, `Docker`

---

## Quick Start with Docker

### 1. Build the Docker Image

docker build -t field-ndvi-pipeline .

## Pipeline Architecture

```mermaid
flowchart TD
    subgraph Inputs [Spatial & Temporal Inputs]
        A1[GeoJSON / Shapefile] -->|Path| B[vector_loader.py]
        A2[BBOX: min_lon, min_lat, max_lon, max_lat] -->|4 Coords| B
        A3[Point: lon, lat] -->|2 Coords + Auto Buffer| B
    end

    subgraph Core [Cloud-Native Processing Engine]
        B -->|GeoDataFrame EPSG:4326| C[STAC Catalog Query]
        C -->|pystac-client| D[AWS Sentinel-2 L2A]
        D -->|Lazy xarray / stackstac| E[NDVI Time-Series Calculation]
        E -->|Resample & Aggregation| F[Monthly Mean NDVI Summary]
    end

    subgraph Output [Artifacts & Verification]
        F -->|Console Output| G[Pandas Summary Table]
        F -->|Matplotlib Engine| H[ndvi_phenological_curve.png]
        I[Pytest Suite] -->|Automated Tests| B
        I -->|Automated Tests| E
    end