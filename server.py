from flask import Flask, jsonify, request
from datetime import datetime
from pymodm import connect, MongoModel, fields
from LogIn import LogIn
from UserData import UserData
from UserMetrics import UserMetrics
import logging
import os

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


def split_db_img_name(img_name):

    return img_name, processing


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

    # Unload ZIP files
    all_images = {}

    # Loop through each filepath and store image name with appended processing as found in DB
    # MAKE A FUNCTION ACCEPTING ALL FILEPATHS RETURNING ALL_IMAGES DICT
    for filepath in data["filepaths"]:
        head, tail = isolate_image_name_from_path(filepath)
        all_images[filepath] = []
        all_images[filepath].append(get_db_img_name(tail, '_original'))  # Append original image name
        all_images[filepath].append(get_db_img_name(tail, data["processing"]))  # Append image name with processing type

    # Loop through filepaths
    # MAKE A FUNCTION WHICH RETURNS DICTS
    for filepath in all_images:
        # Loop through image names from db corresponding to each filepath
        for img_name in filepath:
            # Check if image_name present
            count = UserData.objects.raw(
                {"_id": data["username"],
                "image_name": img_name}).count()
            if count == 1:
                # If present, store filepath and processing type as old_image
                old_images[]
            elif count == 0:
                # If not present, store filepath and processing type as new_image
                new_images[]
            else:
                logging.warning("Error in finding files")
                return "Error in finding files", 400


    # Return dictionary of images present and not present

# -----------------------------Display tab--------------------------------
# ----------------------------Download tab--------------------------------
# ----------------------------User Metrics tab----------------------------


if __name__ == "__main__":
    database_connection()
    app.run()
