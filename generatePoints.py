# generatePoints.py allows to generate a list of n x,y coordinates in the bounding of a given geotiff
import rasterio
import numpy as np
import pandas as pd
import argparse

# --- Default Configuration ---
# Define default paths which can be overridden by command-line arguments
DEFAULT_GEOTIFF_PATH = "/geodata/altimetrie/mnt/DTM_50cm_FULL_clipped.tif"
DEFAULT_COORDS_PATH = "points.csv"
DEFAULT_NUM_POINTS = 100000

# --- Argument Parsing ---
# Set up the argument parser to read file paths from the command line.
# The 'default' parameter makes the arguments optional.
parser = argparse.ArgumentParser(description="Allows to generate a list of n x,y coordinates in the bounding of a given geotiff.")
parser.add_argument('--geotiff', default=DEFAULT_GEOTIFF_PATH, help=f'Path to the input GeoTIFF file. (default: {DEFAULT_GEOTIFF_PATH})')
parser.add_argument('--num_points', default=DEFAULT_NUM_POINTS, help=f'Number of points . (default: {DEFAULT_NUM_POINTS})')
parser.add_argument('--coords', default=DEFAULT_COORDS_PATH, help=f'Path to the output CSV file with x, y coordinates. (default: {DEFAULT_COORDS_PATH})')

args = parser.parse_args()

# --- Configuration ---
# Use the arguments passed from the command line, or the defaults if not provided
geotiff_path = args.geotiff
coords_csv_path = args.coords
number_of_points = args.num_points


def generate_random_points_df(n, x_min, x_max, y_min, y_max, filename="points.csv"):
    x = np.random.uniform(x_min, x_max, n)
    y = np.random.uniform(y_min, y_max, n)
    df_points = pd.DataFrame({"x": x, "y": y})
    df_points.to_csv(filename, index=False)
    return df_points

print(f"Generating {number_of_points} random points...")
print(f"in the bounds of geotiff_path={geotiff_path}...")
try:
    with rasterio.open(geotiff_path) as src:
        print(f"geotiff width: {src.width}")
        print(f"geotiff height: {src.height}")
        print(f"geotiff bounds : {src.bounds}")
        df = generate_random_points_df(number_of_points, src.bounds.left, src.bounds.right, src.bouns.bottom, src.bounds.top, coords_csv_path)
        print(f"generated {number_of_points} points in file '{coords_csv_path}', df.describe:\n{df.describe()}")
except FileNotFoundError:
    print(f"Error: The file was not found at {geotiff_path}")
except Exception as e:
    print(f"An error occurred: {e}")
