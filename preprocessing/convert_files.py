import os
import pyvips


input_path = '../example_images/'
output_path = '../tiff_images/'

# Create output directory if not exists
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Obtain png files
png_files = [f for f in os.listdir(input_path) if f.endswith('.png')]

# Convert PNG to TIFF
for file in png_files:
    png_path = os.path.join(input_path, file)
    tiff_name = file.replace('.png', '.tiff')
    tiff_path = os.path.join(output_path, tiff_name)
    image = pyvips.Image.new_from_file(png_path, access='sequential')
    image.tiffsave(tiff_path)

print('completed')