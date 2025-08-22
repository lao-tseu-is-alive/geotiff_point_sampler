# GeoTIFF Altitude Query Tool

A fast and efficient Python command-line tool to extract altitude values from a GeoTIFF raster file for a large number of point coordinates. It uses the highly optimized `rasterio` and `pandas` libraries for high performance.

## Features

* **Fast**: Optimized for querying hundreds of thousands of points in seconds.
* **Flexible**: Reads input and output file paths from command-line arguments.
* **Easy to Use**: Sensible defaults allow for quick execution with no arguments if files are named `points.csv` and `DTM_50cm_FULL_clipped.tif`.
* **Robust**: Handles points outside the raster's bounds gracefully.

## Requirements

* Python 3.13+
* [`uv`](https://docs.astral.sh/uv/) An extremely fast Python package and project manager, written in Rust.
* Dependencies listed in `pyproject.toml` (`rasterio`, `pandas`)

## Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/lao-tseu-is-alive/geotiff_point_sampler.git](https://github.com/lao-tseu-is-alive/geotiff_point_sampler.git)
    cd geotiff_point_sampler
    ```

2.   Create a virtual environment and install dependencies using `uv`:
     

```bash
    # Create a virtual environment
    uv venv

    # Activate the virtual environment (on macOS/Linux)
    source .venv/bin/activate
    # On Windows, use: .venv\Scripts\activate

    # Install the project and its dependencies from pyproject.toml
    uv pip install .
```
    

## Usage

The script is run from the command line, specifying the paths to the GeoTIFF, the input coordinates CSV, and the desired output file.
```bash
python getMntFromGeoTif.py --geotiff <path_to_raster.tif> --coords <path_to_points.csv> --output <path_to_results.csv>
```

### Example run 

**less than 7 seconds** to query 100 000 x,y points on a local geotiff file  

```bash
time python getMntValue.py --geotiff /geodata/altimetrie/mnt/DTM_50cm_FULL_clipped.tif --coords points.csv  --output points_with_altitudes.csv 
🚀 Loading coordinates from points.csv...
🚀 Loading geotiff from /geodata/altimetrie/mnt/DTM_50cm_FULL_clipped.tif...
 📏 geotiff width, height : 36000, 26000
 📐 geotiff bounds: BoundingBox(left=2528000.0, bottom=1149000.0, right=2546000.0, top=1162000.0)
 ⏳ Querying 100000 points in /geodata/altimetrie/mnt/DTM_50cm_FULL_clipped.tif...
✅ Success! Results saved to points_with_altitudes.csv

real	0m6.858s
user	0m8.087s
sys	0m1.889s


```