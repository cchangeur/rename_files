# Rename Images with Date Photo Taken

# Purpose: Renames image files in a folder based on date photo taken from EXIF metadata

# Author: Matthew Renze
# Update: Clement Changeur

# Usage: python rename.py input-folder
#   - input-folder = (optional) the directory containing the image files to be renamed

# Examples: python.exe Rename.py C:\Photos
#           python.exe Rename.py

# Behavior:
#  - Given a photo named "Photo Apr 01, 5 54 17 PM.jpg"
#  - with EXIF date taken of "4/1/2018 5:54:17 PM"
#  - when you run this script on its parent folder
#  - then it will be renamed "2018-04-01 17.54.17.jpg"
#  If name is taken, renamed by "xxx-1" or "xxx-2" etc..

# Notes:
#   - For safety, please make a backup before running this script
#   - Currently only designed to work with .jpg, .jpeg, and .png files
#   - EXIF metadata must exist or an error will occur
#   - If you omit the input folder, then the current working directory will be used instead.

# Import libraries
import os
import sys
import time
from PIL import Image, ExifTags

# Set list of valid file extensions
valid_extensions = [".mp4", ".MP4", ".mov", ".MOV"]
valid_image_extensions = [".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG"]

# If folder path argument exists then use it
# Else use the current running folder
if len(sys.argv) < 1:
    folder_path = input_file_path = sys.argv[1]
else:
    print("Start      : Use current folder")
    folder_path = os.getcwd()

# Get all files from folder
file_names = os.listdir(folder_path)
print(file_names)
rename_number = 0
# For each file
for file_name in file_names:
    is_image = False
    new_file_name = ""
    new_file_name_ext = ""
    try:
        # Get the file extension
        file_ext = os.path.splitext(file_name)[1]

        # If the file does not have a valid file extension
        # then skip it
        if file_ext in valid_image_extensions:
            is_image = True
        elif file_ext in valid_extensions:
            pass
        else:
            continue

        # Get the old file path
        old_file_path = os.path.join(folder_path, file_name)

        if is_image:
            # Open the image
            try:
                print("______________________________________")
                print("Open image :", file_name)
                image = Image.open(old_file_path)
            except:
                print("Fail to open image")
                is_image = False
                continue

        if is_image:
            try:
                # Get the date taken from EXIF metadata
                date_taken = image._getexif()[36867]
                # Close the image
                image.close()
                # Reformat the date taken to "YYYY-MM-DD HH-mm-ss"
                date_time = date_taken.replace(":", "-")
                # Change time format to HH.mm.ss
                dataStrip = date_time.split(" ")
                new_file_name = dataStrip[0] + " " + dataStrip[1].replace("-", ".")
            except:
                image.close()
                print("No data in EXIF metadata, take modified date")
                new_file_name = time.strftime(
                    "%Y-%m-%d %H.%M.%S", time.localtime(os.path.getmtime(old_file_path))
                )
                print(
                    time.strftime(
                        "%Y-%m-%d %H.%M.%S",
                        time.localtime(os.path.getmtime(old_file_path)),
                    )
                )
        else:  # Video
            # Reformat the date taken to "YYYY-MM-DD HH-mm-ss"
            print("______________________________________")
            new_file_name = time.strftime(
                "%Y-%m-%d %H.%M.%S", time.localtime(os.path.getmtime(old_file_path))
            )
            print(
                "Open video :",
                time.strftime(
                    "%Y-%m-%d %H.%M.%S", time.localtime(os.path.getmtime(old_file_path))
                ),
            )

        # Combine the new file name and file extension
        new_file_name_ext = new_file_name + file_ext.lower()

        if file_name == new_file_name_ext:
            print("Already OK :", new_file_name_ext)
            continue
        # Check if image with same name not present
        i = 1
        end = True
        while end:
            if new_file_name_ext in os.listdir(folder_path):
                new_file_name_ext = new_file_name + "-" + str(i) + file_ext.lower()
                if file_name == new_file_name_ext:
                    print("Already OK :", new_file_name_ext)
                    break
                i += 1
            else:
                end = False
        print("New name   :", new_file_name_ext)
        # Create the new folder path
        new_file_path = os.path.join(folder_path, new_file_name_ext)

        # Rename the file
        os.rename(old_file_path, new_file_path)
        rename_number += 1
    except Exception as err:
        print("Error while processing : ", err)


print("______________________________________")
print("Stop       : %s files rename for %s files " % (rename_number, len(file_names)))
