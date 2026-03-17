# SWOT Satellite–Based Water Depth Analysis of the Australian Channel Country Rivers

This repository contains Jupyter notebooks for analysing SWOT (Surface Water and Ocean Topography) Pixel Cloud data to quantify floodwater depth  in inland Australia, with a primary focus on the Cooper Creek–Thomson River system within the Channel Country.

## Overview

In April 2025, the Channel Country river system experienced one of the most severe flood events on record. This workflow demonstrates the derivation of floodwater depth from SWOT Pixel Cloud (PIXC) observations, integrated with LiDAR-derived Digital Elevation Model (DEM) data and complementary optical satellite imagery.

## Study Area

- **River**: Thomson River, Cooper Creek
- **Region**: Channel Country, Queensland, Australia  
- **SWOT Reach ID**: 56829100071
- **Coordinates**: ~143.2°E to 143.3°E, -24.4°S to -24.3°S

## Key Features

- **SWOT L2 HR Pixel Cloud data** automated retrieval from NASA Earthdata
- **Sentinel-2 optical imagery** water extent mapping using MNDWI
- **Quality assurance** filtering (water fraction, classification, false detection rate)
- **Tidal and atmospheric corrections** (pole tide, load tide, solid earth tide)
- **Coordinate transformations** WGS84 → GDA94 → MGA54 (Australian datums)
- **Accurate depth calculation** water surface (SWOT - AUSGeoid) - riverbed (LiDAR DEM)
- **Statistical outlier removal** using KDTree spatial analysis
- **Visualization and export** to Shapefile, GeoPackage, CSV, and KML formats

## Requirements

### System Requirements
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab
- Minimum 8GB RAM (16GB+ recommended for large LiDAR files)
- Internet connection for satellite data download

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
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/akr706/SWOT_CooperFlood.git
cd SWOT_CooperFlood
```

### 2. Install Dependencies

The notebook includes an automatic installation in the first cell, or install manually:

```bash
pip install numpy pandas geopandas shapely xarray rasterio earthengine-api geemap earthaccess pyproj matplotlib scipy netCDF4
```

## Data Files

This repository includes:
- **SWOT_Water_Depth_Analysis.ipynb** - Main analysis notebook
- **au_ga_AUSGeoid09_V1.01.tif** - AUSGeoid09 geoid model for datum correction
- **CooperLiDAR_DEM_25m.tif** - LiDAR DEM (25m resolution) for riverbed elevation

**Note**: The LiDAR DEM file is large (~250MB). For other study areas, replace with your own DEM.

## Authentication Setup

### NASA Earthdata Login

Required for downloading SWOT data:

1. Create a free account at https://urs.earthdata.nasa.gov/
2. Create a `.netrc` file in your home directory:

```bash
# On Linux/Mac
nano ~/.netrc
```

Add the following:

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

Required for Sentinel-2 imagery:

1. Sign up at https://earthengine.google.com/
2. **Option A - Service Account** (recommended for automation):
   - Create a Google Cloud project
   - Create a service account and download JSON credentials
   - Update `credentials_path` in notebook cell 7
   
3. **Option B - Interactive Authentication**:
   - Run `ee.Authenticate()` when prompted in the notebook


## Running the Notebook

### 1. Open Jupyter Notebook

```bash
jupyter notebook SWOT_Water_Depth_Analysis.ipynb
```

### 2. Configure Parameters

In notebook cell 7, update these parameters for your study area:

```python
# Study Area Parameters
SELECTED_REACH_ID = 56829100071  # SWORD reach identifier
SELECTED_NODE_ID = 56829100070271  # Node within reach

# Data Download Parameters
SWOT_DATES = ('2025-03-30', '2025-03-30')  # SWOT observation dates
SENTINEL_DATES = ('2025-03-29', '2025-04-01')  # Sentinel-2 date range

# Output directory
OUTPUT_BASE_DIR = f'/path/to/output/{SELECTED_REACH_ID}'
```

### 3. Execute Cells Sequentially

Run all cells in order (cells 1-32). **Important**: Do not skip cells as later cells depend on variables created in earlier ones.

## Workflow Overview

### Data Acquisition
1. **Sentinel-2 Imagery** - MNDWI water mask creation via Google Earth Engine
2. **SWOT Data** - Download L2 HR PIXC NetCDF files from NASA Earthdata
3. **KML Export** - Generate KML file of water extent

### Data Processing
4. **Spatial Filtering** - Filter SWOT points to study area bounding box
5. **Quality Filtering** - Apply classification, water fraction, and false detection filters
6. **Tidal Corrections** - Remove pole tide, load tide, and solid earth tide effects

### Depth Calculation
7. **Coordinate Transformation** - WGS84 → GDA94 → MGA54
8. **Datum Correction** - Subtract AUSGeoid to convert ellipsoidal height to AHD
9. **Riverbed Subtraction** - Subtract LiDAR DEM to get actual water depth
   ```
   depth = (SWOT_height - AUSGeoid) - LiDAR_DEM
   ```

### Quality Control & Export
10. **Outlier Removal** - KDTree-based statistical filtering
11. **Visualization** - Scatter plots, histograms, statistics
12. **Export** - Save to Shapefile, GeoPackage, and CSV

## Output Files

Results are saved to `OUTPUT_BASE_DIR/<reach_id>/`:

- **SWOT NetCDF**: `<date>/SWOT_L2_HR_PIXC_*.nc`
- **Sentinel-2 Water Mask**: `kml/sentinel2_water_mask.tif`, `kml/Sentinel2_water_extent_*.kml`
- **Processed Depth Data**: 
  - `swot_depth_processed.shp` (Shapefile)
  - `swot_depth_processed.gpkg` (GeoPackage)
  - `swot_depth_processed.csv` (CSV with lat, lon, depth_m)

## Methodology

### Depth Calculation Formula

The water depth above riverbed is calculated in two steps:

**Step 1: Datum Correction**
```
water_surface_AHD = SWOT_ellipsoidal_height - AUSGeoid_separation
```
- Converts WGS84 ellipsoidal height to Australian Height Datum (AHD)
- AUSGeoid09 provides the geoid-ellipsoid separation

**Step 2: Depth Calculation**
```
water_depth = water_surface_AHD - LiDAR_riverbed_elevation_AHD
```
- Subtracts riverbed elevation from water surface elevation
- Both in AHD reference frame

### Coordinate Systems

- **WGS84 (EPSG:4326)** - SWOT raw data
- **GDA94 (EPSG:4283)** - Australian geodetic datum (lat/lon)
- **MGA54 (EPSG:28354)** - Map Grid of Australia Zone 54 (projected, meters)
- **AHD** - Australian Height Datum (vertical reference)

The LiDAR DEM is in MGA54 projected coordinates, so SWOT points are transformed: WGS84 → GDA94 → MGA54 for DEM sampling.


## Customization for Other Study Areas

### 1. Find Your River Reach

Use the SWORD (Surface Water and Ocean Topography Reference) database:
- Browse: https://www.swordrivers.org/
- Find your river's reach_id and node_id
- Update in notebook cell 7

### 2. Provide Your Own DEMs

Replace these files with DEMs covering your study area:
- **Geoid model** (for datum correction) - replace `au_ga_AUSGeoid09_V1.01.tif`
- **LiDAR/SRTM DEM** (for riverbed elevation) - replace `CooperLiDAR_DEM_25m.tif`

Ensure DEMs have:
- Proper CRS metadata
- NoData values defined
- Coverage overlapping your SWOT observations

### 3. Update Date Ranges

```python
SWOT_DATES = ('YYYY-MM-DD', 'YYYY-MM-DD')
SENTINEL_DATES = ('YYYY-MM-DD', 'YYYY-MM-DD')
```

Check SWOT coverage: https://swot.jpl.nasa.gov/

## Troubleshooting

### Common Issues

**1. NASA Earthdata Authentication Failed**
```bash
# Verify .netrc file exists and has correct permissions
ls -la ~/.netrc
chmod 600 ~/.netrc
```

**2. Google Earth Engine Not Authenticated**
```python
# In notebook, run:
ee.Authenticate()
```

**3. Kernel Crashes with Large DEMs**
- The notebook uses windowed reading to prevent memory issues
- If problems persist, reduce batch_size in cell 25 (default: 10000)

**4. No SWOT Data Found**
- Check if SWOT has coverage for your dates/location
- SWOT has 21-day repeat cycle with limited spatial coverage
- Visit: https://swot.jpl.nasa.gov/mission/coverage/

**5. All Depth Values are NaN**
- Check coordinate system match between SWOT data and LiDAR DEM
- Verify DEM coverage overlaps SWOT observation area
- Check DEM nodata values

**6. Negative Depth Values**
- Can occur due to measurement uncertainties
- Use outlier removal (cell 27) to filter anomalies
- Adjust `OUTLIER_STD_MULT` parameter if needed

## Data Sources & References

### Data
- **SWOT Mission**: NASA/CNES - https://swot.jpl.nasa.gov/
- **SWOT L2 PIXC Data**: NASA Earthdata - https://podaac.jpl.nasa.gov/
- **SWORD River Database**: Allen & Pavelsky (2018) - https://www.swordrivers.org/
- **Sentinel-2**: ESA Copernicus - https://sentinel.esa.int/
- **AUSGeoid09**: Geoscience Australia - https://www.ga.gov.au/
- **Google Earth Engine**: https://earthengine.google.com/

## Citation

If you use this workflow in your research, please cite:

```
"SWOT satellite assessment for monitoring the extreme 2025 floods in Australia’s inland Channel Country" by Rai et al
DOI 10.1088/1748-9326/ae530f
url: https://iopscience.iop.org/article/10.1088/1748-9326/ae530f
```

## License

This project is available under the MIT License.

## Contact

- **Author**: Atul Kumar Rai [ akr706@uowmail.edu.au]
- **Repository**: https://github.com/akr706/SWOT_CooperFlood
- **Issues**: https://github.com/akr706/SWOT_CooperFlood/issues

## Acknowledgments

- NASA/CNES SWOT Mission Team
- Google Earth Engine Platform
- Geoscience Australia
- ESA Copernicus Programme

---

**Last Updated**: January 2026
