import json
import glob
from tqdm import tqdm
import os
from datetime import datetime
import piexif
import shutil


base_dir = 'C:/Users/Florian/Desktop/google_images'
result_dir = 'C:/Users/Florian/Desktop/images'
icloud_dir = 'C:/Users/Florian/Pictures/iCloud Photos/Photos'


def get_name(string: str):
    return string.split('.')[0]


icloud_files = list(map(get_name, os.listdir(icloud_dir)))

json_file_paths = glob.glob(base_dir + '/*/*.json')
for json_path in tqdm(json_file_paths):
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
    img_path = json_path[:-5]

    time_parse = json_data.get('photoTakenTime')
    if time_parse is None:
        time_parse = json_data.get('creationTime')
    if time_parse is None:
        time_parse = json_data.get('photoLastModifiedTime')

    result_image_path = f'{result_dir}/{os.path.split(img_path)[-1]}'
    if get_name(os.path.split(img_path)[-1]) not in icloud_files:
        try:
            shutil.copy2(img_path, result_image_path)

            exif_dict = piexif.load(result_image_path)
            if time_parse is not None:
                time = datetime.fromtimestamp(int(time_parse.get('timestamp'))).strftime("%Y:%m:%d %H:%M:%S")
                exif_dict['0th'][piexif.ImageIFD.DateTime] = time
                exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = time
                exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = time
                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, result_image_path)
        except:
            print(img_path)


