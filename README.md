# 🌾 Cloud-Native Agricultural Field NDVI Pipeline

[![CI Pipeline](https://github.com/YOUR_GITHUB_USERNAME/field-ndvi-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/field-ndvi-pipeline/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-green.svg)](https://www.python.org/)

An end-to-end, Cloud-Native Geospatial Data Pipeline designed to ingest multi-format vector geometries (Shapefiles, GeoJSON, Bounding Boxes), query SpatioTemporal Asset Catalogs (STAC) on AWS for cloud-optimized Sentinel-2 scenes, and compute zonal Normalized Difference Vegetation Index (NDVI) statistics without downloading raw satellite raster files.

---

## 📐 Architecture Overview

```mermaid
flowchart TD
    A[Vector Input: .shp / .geojson / BBOX] --> B[src/vector_loader.py]
    B -->|Validate & Reproject to EPSG:4326| C[GeoPandas GeoDataFrame]
    C --> D[src/pipeline.py]
    D -->|Query Bounding Box| E[AWS STAC Catalog Element84]
    E -->|Return Sentinel-2 COG Metadata| D
    D -->|Compute Array Operations| F[NumPy Vectorized NDVI Engine]
    F --> G[Zonal NDVI DataFrame Output]
