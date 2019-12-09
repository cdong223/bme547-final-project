from flask import Flask, jsonify, request
from datetime import datetime
from pymodm import connect, MongoModel, fields
from PIL import Image
from LogIn import LogIn
from UserData import UserData
from UserMetrics import UserMetrics
from skimage import exposure, io, color
import skimage
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import logging
import os
import base64
import io
import time

app = Flask(__name__)


def database_connection():
    connect("mongodb+srv://dervil_dong_moavenzadeh_qi"
            ":BME54701@cluster0-dykvj.mongodb.net"
            "/test?retryWrites=true&w=majority")
    logging.basicConfig(filename="image_server.log",
                        level=logging.INFO,
                        filemode='w')


# ----------------------------Login Screen--------------------------------
# -----------------------------Upload tab---------------------------------
def validate_input_json(data, expected):
    # Validates input json is as expected
    # Initialize response assuming all correct
    valid = True
    message = "Input json is valid."
    code = 200  # OK

    # Ensure type data is dict
    if type(data) != dict:
        valid = False
        message = "Data entry is not in dictionary format."
        code = 400  # Bad Request
        return valid, message, code

    # Ensure keys in data are same as expected
    for key in data:
        if key not in expected:
            valid = False
            message = "Dictionary keys are not in correct format."
            code = 400  # Bad Request
            return valid, message, code
    for key in expected:
        if key not in data:
            valid = False
            message = "Dictionary does not have enough " \
                      "information. Missing keys."
            code = 400  # Bad Request
            return valid, message, code

    # Ensure value types in data are same as expected
    for key in expected:
        if type(data[key]) not in expected[key]:
            valid = False
            message = "Dictionary values are not correct. Invalid data types."
            code = 400  # Bad Request
            return valid, message, code

    return valid, message, code


def isolate_image_name_from_path(filepath):
    # Returns image name from file path
    head, tail = os.path.split(filepath)
    return head, tail


def get_db_img_name(img_name, processing):
    img_name, filetype = img_name.split('.')
    return img_name + processing + "." + filetype


def img_name_from_filepath(filepath, processing):
    # COULD BE MORE MODULAR IF ACCEPT SINGLE FILE PATH AND PROCESSING TYPE AND RETURNS NAME
    head, tail = isolate_image_name_from_path(filepath)
    img_name = get_db_img_name(tail, processing)  # Append original image name
    return img_name


def is_image_present(username, img_name):
    # Check if image is present
    users = UserData.objects.raw({"_id": username})
    count = 0
    for user in users:
        for stored_images in user.image_name:
            if img_name == stored_images:
                count += 1
    if count == 1:
        return True
    elif count == 0:
        return False
    else:
        logging.warning("Error in finding files")
        return "Error in finding files"


@app.route("/api/validate_images", methods=["POST"])
def validate_images():
    # Retrieve data sent to server
    data = request.get_json()  # Returns native dictionary

    # Validate Input json
    expected = {"username": (str,),
                "filepaths": (list,),
                "processing": (str,)}
    valid, message, code = validate_input_json(data, expected)
    if not valid:
        logging.warning("Attempted upload json is wrong format")
        return jsonify(message), code

    # Unload ZIP files and add to filepaths?

    # Store all filepaths with corresponding image name versions from processing type
    all_images_dict = {}
    for filepath in data["filepaths"]:
        all_images_dict[filepath][img_name_from_filepath(filepath, '_original')] = '_original'
        all_images_dict[filepath][img_name_from_filepath(filepath, data["processing"])] = data["processing"]

    # Retrieve images present and not present with processing type
    old_images = {}
    new_images = {}
    for filepath in all_images_dict:
        # Loop through image names from db corresponding to each filepath
        for img_name in all_images_dict[filepath]:
            # Check if image is present with processing type
            if is_image_present(data["username"], img_name):
                # If is present, store in return dict not to process
                old_images[filepath].append(all_images_dict[filepath][img_name])
            else:
                # If is not present, store in return dict to process
                new_images[filepath].append(all_images_dict[filepath][img_name])

    # Return dictionary of images present and not present
    out_dict = {"present": old_images,
                "not present": new_images}
    return jsonify(out_dict)


def get_num_pixels(filepath):
    width, height = Image.open(filepath).size
    image_size = str(width)+"x"+str(height)
    return image_size


def pixel_histogram(filepath):
    image = skimage.io.imread(filepath)
    red_hist = skimage.exposure.histogram(image[:, :, 0])
    green_hist = skimage.exposure.histogram(image[:, :, 1])
    blue_hist = skimage.exposure.histogram(image[:, :, 2])
    hist_dict = {"red": red_hist,
                 "green": green_hist,
                 "blue": blue_hist}
    return hist_dict


def original_upload(username, filepath):
    # Upload original image in filepath
    # Create image name
    image_name = img_name_from_filepath(filepath, "_original")

    # Calc image size
    image_size = get_num_pixels(filepath)

    # Store upload date
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")

    # Calc histogram data
    hist_data = pixel_histogram(filepath)
    with open(filepath, "rb") as image_file:
        start_time = time.time()  # Better way may be to use timeit.timeit(function)
        coded = base64.b64encode(image_file.read())
        end_time = time.time()

        # Calc CPU processing time
        processing_time = str(end_time - start_time)
        UserData.objects.raw(
            {"_id": username}).update(
            {"$push": {"image_name": image_name,
                       "image": coded,
                       "processing_time": processing_time,
                       "image_size": image_size,
                       "hist_data": hist_data,
                       "upload_date": upload_date}})
    return


def histogram_equalized_upload(username, filepath):
    # Upload histogram equalized image from filepath
    return


def contrast_stretched_upload(username, filepath):
    # Upload contrast stretched image from filepath
    return


def log_compressed_upload(username, filepath):
    # Upload log compressed image from filepath
    return


def inverted_image_upload(username, filepath):
    # Upload inverted image from filepath
    return


@app.route("/api/upload_images", methods=["POST"])
def upload_images():
    # Retrieve data sent to server
    data = request.json()

    # Validate Input json
    expected = {"username": (str,),
                "images": (dict,)}
    valid, message, code = validate_input_json(data, expected)
    if not valid:
        logging.warning("Attempted upload json is wrong format")
        return jsonify(message), code

    # Check if user already has UserData collection.
    # If not, need to create one with first file entry being the first of new_images knowing it will be _original.

    # Begin uploading images. Handle ZIPs separately?
    new_images = data["images"]
    for filepath in new_images:
        if new_images[filepath] == '_original':
            original_upload(username, filepath)
        elif new_images[filepath] == '_histogramEqualized':
            histogram_equalized_upload(username, filepath)
        elif new_images[filepath] == '_contrastStretched':
            contrast_stretched_upload(username, filepath)
        elif new_images[filepath] == '_logCompressed':
            log_compressed_upload(username, filepath)
        elif new_images[filepath] == '_invertedImage':
            inverted_image_upload(username, filepath)
        else:
            return "Invalid Computation Type", 400

    return "Uploaded all images successfully"
# -----------------------------Display tab--------------------------------
# ----------------------------Download tab--------------------------------
# ----------------------------User Metrics tab----------------------------


if __name__ == "__main__":
    database_connection()
    app.run()
