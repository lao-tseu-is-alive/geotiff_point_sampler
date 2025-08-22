# getMntValue.py allows to extract a list geotiff Values (like MNT value) from a list of x,y coordinates
# using Rasterio to access to geospatial raster data
# https://rasterio.readthedocs.io/en/stable/index.html
import rasterio
import pandas as pd
import argparse

# --- Default Configuration ---
# Define default paths which can be overridden by command-line arguments
DEFAULT_GEOTIFF_PATH = "/geodata/altimetrie/mnt/DTM_50cm_FULL_clipped.tif"
DEFAULT_COORDS_PATH = "points.csv"
DEFAULT_OUTPUT_PATH = "output_with_altitudes.csv"

# --- Argument Parsing ---
# Set up the argument parser to read file paths from the command line.
# The 'default' parameter makes the arguments optional.
parser = argparse.ArgumentParser(description="Extracts altitude values from a GeoTIFF for a given list of coordinates.")
parser.add_argument('--geotiff', default=DEFAULT_GEOTIFF_PATH, help=f'Path to the input GeoTIFF file. (default: {DEFAULT_GEOTIFF_PATH})')
parser.add_argument('--coords', default=DEFAULT_COORDS_PATH, help=f'Path to the input CSV file with x, y coordinates. (default: {DEFAULT_COORDS_PATH})')
parser.add_argument('--output', default=DEFAULT_OUTPUT_PATH, help=f'Path for the output CSV file with altitudes. (default: {DEFAULT_OUTPUT_PATH})')

args = parser.parse_args()

# --- Configuration ---
# Use the arguments passed from the command line, or the defaults if not provided
geotiff_path = args.geotiff
coords_csv_path = args.coords
output_csv_path = args.output


# 1. Load  X, Y coordinates from the given CSV file
print(f"🚀 Loading coordinates from {coords_csv_path}...")
df = pd.read_csv(coords_csv_path)
# Ensure column names are 'x' and 'y'
coords = list(zip(df['x'], df['y']))
print(f"🚀 Loading geotiff from {geotiff_path}...")
# 2. Open the GeoTIFF and sample the points in one go
try:
    with rasterio.open(geotiff_path) as src:
        print(f" 📏 geotiff width, height : {src.width}, {src.height}")
        print(f" 📐 geotiff bounds: {src.bounds}")
        print(f" ⏳ Querying {len(coords)} points in {geotiff_path}...")
        # The 'sample' method is highly optimized for this task.
        # It returns a generator, so we convert it to a list.
        # Each item in the list is a NumPy array with the value from the first band.
        altitude_generator = src.sample(coords)

        # Extract the first band value for each point.
        # The NoData value from the file is handled automatically.
        # you can see it doing a :  gdalinfo your_geotiff.tif
        # If a point is outside the raster, rasterio returns also the nodata value (usually -32768.0).
        altitudes = [alt[0] for alt in altitude_generator]

    # 3. Add the new altitude data to the DataFrame and save it
    df['altitude'] = altitudes
    df.to_csv(output_csv_path, index=False)

    print(f"✅ Success! Results saved to {output_csv_path}")

except FileNotFoundError as e:
    print(f"💥 Error: The file was not found at {geotiff_path}, please check the path and try again.")
    print(e)
except Exception as e:
    print(f"💥 An error occurred: {e}")

