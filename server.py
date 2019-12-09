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


def img_name_from_filepath(filepath, processing):
    # COULD BE MORE MODULAR IF ACCEPT SINGLE FILE PATH AND PROCESSING TYPE AND RETURNS NAME
    head, tail = isolate_image_name_from_path(filepath)
    img_name = get_db_img_name(tail, processing)  # Append original image name
    return img_name


def is_image_present(username, img_name):
    # Check if image is present
    count = UserData.objects.raw(
        {"_id": username,
         "image_name": img_name}).count()
    if count == 1:
        return True
    elif count == 0:
        return False
    else:
        logging.warning("Error in finding files")
        return "Error in finding files"


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

    # Unload ZIP files and add to filepaths?

    # Store all filepaths with corresponding image name versions from processing type
    all_images_dict = {}
    for filepath in data["filepaths"]:
        all_images_dict[filepath].append(img_name_from_filepath(filepath, data["processing"]))
        all_images_dict[filepath].append(img_name_from_filepath(filepath, '_original'))

    # Retrieve images present and not present with processing type
    for filepath in all_images_dict:
        # Loop through image names from db corresponding to each filepath
        for img_name in filepath:
            # Check if image_name present MAKE FUNCTION
            if is_image_present(data["username"], img_name):
                old_images[]
            else:
                new_images[]

    # Return dictionary of images present and not present

# -----------------------------Display tab--------------------------------
# ----------------------------Download tab--------------------------------
# ----------------------------User Metrics tab----------------------------


if __name__ == "__main__":
    database_connection()
    app.run()
