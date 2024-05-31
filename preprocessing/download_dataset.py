import os
import pandas as pd
import subprocess
import pyvips
import shutil
import zipfile
from tqdm import tqdm

# Base directory path
base_path = '/vast/qtim/datasets/public/UBC-OCEAN'

# Paths to CSV file and output directory
csv_path = os.path.join(base_path, 'train.csv')
output_dir = os.path.join(base_path, 'train_images')

# Path to the Kaggle CLI executable
kaggle_path = '/vast/qtim/projects/brcrp/anaconda3/envs/vips/bin/kaggle'

# Temporary directory for downloads
temp_download_dir = os.path.join(base_path, 'temp_downloads')

# Create output and temporary directories if they do not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(temp_download_dir):
    os.makedirs(temp_download_dir)

# Read the CSV
df = pd.read_csv(csv_path)


# Function to download an image using Kaggle CLI
def download_image(image_id):
    file_name = f'train_images/{image_id}.png'
    subprocess.run([kaggle_path, 'competitions', 'download', '-c', 'UBC-OCEAN', '-f', file_name])
    # Move the downloaded file to the temporary directory
    shutil.move(f'{image_id}.png.zip', os.path.join(temp_download_dir, f'{image_id}.png.zip'))


# Function to extract the image
def extract_image(image_id):
    with zipfile.ZipFile(os.path.join(temp_download_dir, f'{image_id}.png.zip'), 'r') as zip_ref:
        zip_ref.extractall(temp_download_dir)


# Function to convert a PNG image to TIFF and remove the original PNG
def convert_to_tiff_and_remove_png(image_id):
    image_path = os.path.join(temp_download_dir, f'{image_id}.png')
    tiff_path = os.path.join(output_dir, f'{image_id}.tiff')
    image = pyvips.Image.new_from_file(image_path, access='sequential')
    image.tiffsave(tiff_path)
    os.remove(image_path)  # remove the PNG image
    os.remove(os.path.join(temp_download_dir, f'{image_id}.png.zip'))  # remove the ZIP file


# Iterate over each row in the DataFrame
for index, row in tqdm(df.iterrows()):
    image_id = row['image_id']

    # Download the image if the PNG.ZIP file does not exist
    if not os.path.exists(os.path.join(temp_download_dir, f'{image_id}.png.zip')):
        print(f'Downloading image {image_id}...')
        download_image(image_id)

    # If downloaded ZIP file exists then extract PNG image and convert it to TIFF
    if os.path.exists(os.path.join(temp_download_dir, f'{image_id}.png.zip')):
        print(f'Extracting and converting image {image_id}...')
        extract_image(image_id)
        convert_to_tiff_and_remove_png(image_id)
    else:
        print(f'Image {image_id}.png.zip not found in the downloads folder. Verify if the download was successful.')

print('Process completed.')
