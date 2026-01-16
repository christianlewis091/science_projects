import os
import shutil

source_dir = r" I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3585"
dest_dir = r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\png_folder"

os.makedirs(dest_dir, exist_ok=True)

for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith(".png"):
            src_path = os.path.join(root, file)
            dst_path = os.path.join(dest_dir, file)

            # if same file name already exists, rename with a number
            base, ext = os.path.splitext(file)
            counter = 1
            while os.path.exists(dst_path):
                dst_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
                counter += 1

            shutil.copy2(src_path, dst_path)