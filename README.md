# SWOT Water Depth Analysis for Channel Country River System

This repository contains a Jupyter notebook for analyzing SWOT (Surface Water and Ocean Topography) satellite data to derive floodwater depth measurements for the Channel Country river system in inland Australia.

## Overview

In April 2025, the Channel Country river system experienced one of the most severe flood events on record. This workflow demonstrates the derivation of floodwater depth from SWOT Pixel Cloud (PIXC) observations, integrated with LiDAR-derived Digital Elevation Model (DEM) data and complementary optical satellite imagery.

## Features

- **SWOT L2 HR Pixel Cloud data retrieval** from NASA Earthdata
- **Sentinel-2 optical imagery** for water extent mapping (MNDWI-based)
- **Quality assurance filtering** (water fraction, classification, false detection)
- **Tidal and atmospheric corrections** (pole tide, load tide, solid earth tide)
- **Coordinate transformations** (WGS84 ellipsoidal → Australian Height Datum)
- **DEM-based depth derivation** using AUSGeoid and LiDAR DEM
- **Statistical outlier removal** using KDTree spatial analysis
- **Visualization and export** to multiple geospatial formats

## Requirements

### System Requirements
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab
- Minimum 8GB RAM (16GB recommended for large datasets)
- Internet connection for data download

### Python Dependencies

```bash
numpy
pandas
geopandas
shapely
xarray
rasterio
earthengine-api
geemap
earthaccess
pyproj
matplotlib
scipy
netCDF4
dask
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/akr706/SWOT_CooperFlood.git
cd SWOT_CooperFlood
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

The notebook includes an automatic installation cell, or you can install manually:

```bash
pip install numpy pandas geopandas shapely xarray rasterio earthengine-api geemap earthaccess pyproj matplotlib scipy netCDF4 dask
```

## Authentication Setup

### NASA Earthdata Login

1. Create a free account at https://urs.earthdata.nasa.gov/
2. Create a `.netrc` file in your home directory:

```bash
# On Linux/Mac
nano ~/.netrc
```

Add the following content:

```
machine urs.earthdata.nasa.gov
    login YOUR_USERNAME
    password YOUR_PASSWORD
```

Set proper permissions:

```bash
chmod 600 ~/.netrc
```

### Google Earth Engine

1. Sign up for Google Earth Engine: https://earthengine.google.com/
2. Create a service account or use local authentication:
   - **Service Account**: Download JSON credentials and update path in notebook
   - **Local Authentication**: Run `ee.Authenticate()` when prompted

Place your service account JSON file in the repository:
```
cbym-451205-5ff0ef5f6b76.json
```

## Data Requirements

### Required Input Files

1. **AUSGeoid DEM** (for datum correction)
   - File: `au_ga_AUSGeoid09_V1.01.tif`
   - Source: Geoscience Australia
   - Place in repository root

2. **LiDAR DEM** (for riverbed elevation - optional)
   - File: `CooperLiDAR_DEM_25m.tif`
   - Source: State/Federal LiDAR datasets
   - Place in repository root

### Automatically Retrieved Data

- SWOT L2 HR PIXC data (via NASA Earthdata)
- Sentinel-2 imagery (via Google Earth Engine)
- SWORD river network (via Google Earth Engine)

## Running the Notebook

### 1. Open Jupyter Notebook

```bash
jupyter notebook SWOT_Water_Depth_Analysis.ipynb
```

Or with JupyterLab:

```bash
jupyter lab SWOT_Water_Depth_Analysis.ipynb
```

### 2. Configure Parameters

Edit the configuration cell (Step 2) to customize:

```python
# Study Area Parameters
SELECTED_REACH_ID = 56829100071  # Thomson River reach identifier
SELECTED_NODE_ID = 56829100070271  # Node within reach

# Data Download Parameters
SWOT_DATES = ('2025-03-30', '2025-03-30')  # SWOT observation dates
SENTINEL_DATES = ('2025-03-29', '2025-04-01')  # Sentinel-2 date range

# Output directory
OUTPUT_BASE_DIR = f'/path/to/output/{SELECTED_REACH_ID}'
```

### 3. Run All Cells

Execute cells sequentially:
- Cell 1: Install packages
- Cell 5: Import libraries
- Cell 7: Configure parameters
- Cell 9: Initialize Google Earth Engine
- Cell 11: Define study area
- Cell 13: Acquire Sentinel-2 water mask
- Cell 15: Download SWOT data
- Cell 16: Generate KML file
- Cell 18: Load and filter SWOT data
- Cell 21: Apply quality filters and tidal corrections
- Cell 23: Transform coordinates to AHD
- Cell 25: Derive water surface elevation
- Cell 27: Statistical outlier removal
- Cell 29-30: Visualization
- Cell 32: Export results

## Workflow Steps

### Step 1-2: Environment Setup
- Install dependencies
- Import libraries
- Configure paths and parameters

### Step 3-4: Study Area Definition
- Initialize Google Earth Engine
- Load SWORD river network dataset
- Select reach and node
- Create 6km buffer AOI

### Step 5: Satellite Data Acquisition
- **Sentinel-2**: MNDWI-based water mask creation
- **SWOT**: Download L2 HR PIXC NetCDF files from NASA Earthdata

### Step 6: SWOT Data Loading
- Load NetCDF pixel cloud data
- Apply spatial bounding box filter
- Extract water-related variables

### Step 7: Quality Assurance
- Convert to 2D slant-plane arrays
- Apply classification filters (water, dark water, low coherence)
- Water fraction filtering (1-99%)
- False detection rate threshold (<2%)
- Tidal corrections (pole tide, load tide, solid earth tide)

### Step 8: Coordinate Transformation
- Transform from WGS84 ellipsoidal to GDA94 (Australian Datum)
- Prepare for DEM integration

### Step 9: Water Surface Elevation
- **Datum correction**: Convert ellipsoidal height to AHD using AUSGeoid
- **Output**: Water surface elevation in Australian Height Datum

> **Note**: For full water depth calculation, subtract LiDAR DEM riverbed elevation:
> `depth = height_ahd - riverbed_elevation`

### Step 10: Outlier Removal
- KDTree-based statistical outlier detection
- Adaptive k-nearest neighbors
- Remove anomalous points

### Step 11: Visualization
- Spatial scatter plots with depth color coding
- Statistical distributions (histogram, box plot)
- Summary statistics

### Step 12: Export
- GeoDataFrame creation
- Export to Shapefile, GeoPackage, CSV
- Save processed results for GIS integration

## Output Files

All outputs are saved to: `OUTPUT_BASE_DIR/<reach_id>/`

### Generated Files

1. **SWOT NetCDF Data**
   - Location: `OUTPUT_BASE_DIR/<reach_id>/<date>/`
   - Files: `SWOT_L2_HR_PIXC_*.nc`

2. **Sentinel-2 Water Mask**
   - Location: `OUTPUT_BASE_DIR/<reach_id>/kml/`
   - Files: 
     - `sentinel2_water_mask.tif` (GeoTIFF)
     - `Sentinel2_water_extent_<date>.kml` (KML polygon)

3. **Processed Water Depth Data**
   - Location: `OUTPUT_BASE_DIR/<reach_id>/`
   - Files:
     - `swot_depth_processed.shp` (Shapefile)
     - `swot_depth_processed.gpkg` (GeoPackage)
     - `swot_depth_processed.csv` (CSV)

## Customization

### Adapt for Other River Systems

1. **Change Study Area**:
   ```python
   SELECTED_REACH_ID = <your_reach_id>
   SELECTED_NODE_ID = <your_node_id>
   ```

2. **Update Bounding Box**:
   ```python
   bbox = (minlon, minlat, maxlon, maxlat)  # Your AOI coordinates
   bounding_box=(minlon, minlat, maxlon, maxlat)  # For SWOT search
   ```

3. **Adjust Date Range**:
   ```python
   SWOT_DATES = ('YYYY-MM-DD', 'YYYY-MM-DD')
   SENTINEL_DATES = ('YYYY-MM-DD', 'YYYY-MM-DD')
   ```

4. **Update DEM Paths**:
   - Replace with appropriate geoid model for your region
   - Use local LiDAR or SRTM/ASTER DEM

## Troubleshooting

### Common Issues

**1. NASA Earthdata Authentication Failure**
- Verify `.netrc` file exists in home directory
- Check file permissions: `chmod 600 ~/.netrc`
- Verify credentials are correct

**2. Google Earth Engine Authentication**
- Run `ee.Authenticate()` for first-time setup
- Check service account credentials path
- Verify GEE account is activated

**3. Memory Issues with Large DEMs**
- The LiDAR DEM processing may cause kernel crashes
- Consider using smaller spatial subsets
- Process in batches with reduced point counts

**4. Missing Data**
- SWOT data may not be available for all dates/locations
- Check SWOT coverage using: https://swot.jpl.nasa.gov/
- Sentinel-2 data requires <50% cloud cover

**5. Coordinate System Mismatches**
- Ensure DEM files are in appropriate CRS
- Verify datum transformations are correct for your region

## Data Sources

- **SWOT L2 HR Pixel Cloud**: NASA/CNES (https://podaac.jpl.nasa.gov/)
- **Sentinel-2**: ESA Copernicus Program (via Google Earth Engine)
- **SWORD River Network**: https://www.swordrivers.org/
- **AUSGeoid**: Geoscience Australia (https://www.ga.gov.au/)

## Citation

If you use this workflow in your research, please cite:

```
Kumar, A. et al. (In Process). "SWOT Satellite Assessment for Monitoring the 
Extreme 2025 Floods in Australia's Inland Channel Country."
```

## References

- Durand, M., et al. (2010). "The Surface Water and Ocean Topography Mission: Observing Terrestrial Surface Water and Oceanic Submesoscale Eddies." *Proceedings of the IEEE*, 98(5), 766-779.
- Allen, G. H., & Pavelsky, T. M. (2018). "Global extent of rivers and streams." *Science*, 361(6402), 585-588.
- McFeeters, S. K. (1996). "The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features." *International Journal of Remote Sensing*, 17(7), 1425-1432.

## License

This project is available under the MIT License. See LICENSE file for details.

## Contact

For questions or issues:
- **Author**: akr706
- **Repository**: https://github.com/akr706/SWOT_CooperFlood
- **Issues**: https://github.com/akr706/SWOT_CooperFlood/issues

## Acknowledgments

- NASA/CNES SWOT Mission Team
- Google Earth Engine Platform
- Geoscience Australia
- ESA Copernicus Programme

---

**Version**: 1.0  
**Last Updated**: January 2026