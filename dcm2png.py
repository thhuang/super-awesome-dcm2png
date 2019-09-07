import pydicom as dcm
import os
from imageio import imwrite
from pathlib import Path

input_dir = "/input"
output_dir = "/output"
log_path = "log.txt"

image_path_list = []
for root, dirs, files in os.walk('/input'):
    for file in files:
        if file.endswith('.DCM') or file.endswith('.dcm'):
            image_path_list.append(os.path.join(root, file))

image_number = len(image_path_list)
with open(log_path, 'w') as out_file:
    for i, image_path in enumerate(image_path_list):
        try:
            # Get the image name
            input_image_name = image_path.split('/')[-1]
            output_image_name = input_image_name.lower().replace('.dcm', '.png')
            out_file.write('[{}/{}] {} -> {}\n'.format(i + 1, image_number, input_image_name, output_image_name))
            out_file.write('\t{}\n'.format(image_path))

            # Get the output path
            output_path = os.path.join(output_dir, output_image_name)

            # Check if the image has already been converted
            if Path(output_path).is_file():
                out_file.write('\tFile Exists!\n')
                continue

            # Read the dicom image
            dcm_image = dcm.dcmread(image_path)
            pixel_array = dcm_image.pixel_array

            # Crop the image
            height, width, _ = pixel_array.shape
            crop = int((width - height) / 2)
            croped_pixel_array = pixel_array[:, crop:-crop, :]

            # Output the image to png format
            imwrite(output_path, croped_pixel_array)
            out_file.write('\tDone!\n')

        except Exception as err:
            out_file.write(str(err))
