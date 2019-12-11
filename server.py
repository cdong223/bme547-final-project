from flask import Flask, jsonify, request
from datetime import datetime
from pymodm import connect, MongoModel, fields
from LogIn import LogIn
from UserData import UserData
from UserMetrics import UserMetrics
from skimage import util, exposure, io, color
from bson.binary import Binary
import pickle
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
def patient_exists(username):
    user = LogIn.objects.raw({"_id": username})
    if user.count() == 0:
        return False
    return True


def register_user(username):
    user = LogIn(username=username).save()
    metrics = UserMetrics(username=username,
                          total_uploads=0,
                          total_hist_equal=0,
                          total_contrast_stretch=0,
                          total_log_comp=0,
                          total_inv_img=0)
    metrics.save()


@app.route("/api/login", methods=["POST"])
def login_patient():
    username = request.get_json()
    if patient_exists(username) is False:
        return jsonify("Bad Login Request"), 400
    return jsonify("Login Successful"), 200


@app.route("/api/new_user", methods=["POST"])
def add_new_user():
    username = request.get_json()
    if patient_exists(username) is True:
        return jsonify("Bad New User Request"), 400
    register_user(username)
    return jsonify("New User Registration Successful"), 200


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

    # Store all filepaths with corres. image name versions from processing type
    all_images_dict = {}
    for filepath in data["filepaths"]:
        all_images_dict[filepath] = {}
        all_images_dict[filepath][img_name_from_filepath(filepath,
                                                         '_original')] \
            = '_original'
        all_images_dict[filepath][img_name_from_filepath(filepath,
                                                         data["processing"])]\
            = data["processing"]

    # Retrieve images present and not present with processing type
    old_images = {}
    new_images = {}
    for filepath in all_images_dict:
        # Loop through image names from db corresponding to each filepath
        old_images[filepath] = []
        new_images[filepath] = []
        for img_name in all_images_dict[filepath]:
            # Check if image is present with processing type
            if is_image_present(data["username"], img_name):
                # If is present, store in return dict not to process
                old_images[filepath].append(img_name)
            else:
                # If is not present, store in return dict to process
                new_images[filepath].append(img_name)

    # Return dictionary of images present and not present
    out_dict = {"present": old_images,
                "not present": new_images}
    return jsonify(out_dict)


def get_num_pixels(image):
    shape = image.shape
    image_size = str(shape[1])+"x"+str(shape[0])+"x"+str(shape[2])
    return image_size


def pixel_histogram(image):
    red_hist = skimage.exposure.histogram(image[:, :, 0])
    green_hist = skimage.exposure.histogram(image[:, :, 1])
    blue_hist = skimage.exposure.histogram(image[:, :, 2])
    hist_dict = {"red": red_hist,
                 "green": green_hist,
                 "blue": blue_hist}
    return hist_dict


def is_first_upload(username):
    return not UserData.objects.raw({"_id": username}).count()


def encode_array(array):
    # Encoding of 3darray to save in database
    encoded_array = base64.b64encode(array)
    return encoded_array


def decode_array(array):
    # Decoding of 3darray to use for processing
    decoded_array = base64.b64encode(array)
    return decoded_array


def encode_dict(dictionary):
    encoded_dict = Binary(pickle.dumps(dictionary, protocol=3))
    return encoded_dict


def decode_dict(dictionary):
    decoded_dict = pickle.loads(dictionary)
    return decoded_dict


def calc_process_time(t1, t2):
    return str(t2 - t1)


def histogram_equalization(image):
    r = image[:, :, 0]
    g = image[:, :, 1]
    b = image[:, :, 2]
    r_hist = skimage.exposure.equalize_hist(r)
    g_hist = skimage.exposure.equalize_hist(g)
    b_hist = skimage.exposure.equalize_hist(b)
    hist_image = np.dstack((r_hist, g_hist, b_hist))
    hist_image = np.uint8(hist_image*255)
    return hist_image


def invert(image):
    inv_image = util.invert(image)
    return inv_image


def log_compression(img):
    # LOG COMPRESSED IMAGE PROCESSING AND ENCODING OF IMAGE
    # Apply log transform
    img_log = (np.log(img + 1) / (np.log(1 + np.max(img)))) * 255
    # Specify the data type
    img_log = np.array(img_log, dtype=np.uint8)
    return img_log


def original_upload(username, filepath):
    # Read original image from filepath
    image = skimage.io.imread(filepath)

    # Process image and encode it.
    start_time = time.time()
    image_encode = encode_array(image)
    processing_time = str(time.time() - start_time)

    # Create image name
    image_name = img_name_from_filepath(filepath, "_original")

    # Calc image size
    image_size = get_num_pixels(image)

    # Get date and time
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")

    # Calc histogram data. Produces {"red": ndarray, "green....}
    # Use each color spectrum for analysis via processing, then
    # concatenate back together with img = np.dstack(red, green, blue)
    hist_data = pixel_histogram(image)
    hist_encode = encode_dict(hist_data)

    # Check if previous images exist
    if is_first_upload(username):
        # If first upload, create document
        user = UserData(username=username,
                        image_name=[image_name],
                        image=[image_encode],
                        processing_time=[processing_time],
                        image_size=[image_size],
                        hist_data=[hist_encode],
                        upload_date=[upload_date])
        user.save()
    else:
        # Save image to database
        UserData.objects.raw(
            {"_id": username}).update(
            {"$push": {"image_name": image_name,
                       "image": image_encode,
                       "processing_time": processing_time,
                       "image_size": image_size,
                       "hist_data": hist_encode,
                       "upload_date": upload_date}})
    return


def histogram_equalized_upload(username, filepath):
    # Read original image from filepath
    image = skimage.io.imread(filepath)

    # Process image and encode it.
    start_time = time.time()
    hist_equalized_image = histogram_equalization(image)
    image_encode = encode_array(hist_equalized_image)
    processing_time = str(time.time() - start_time)

    # Create image name
    image_name = img_name_from_filepath(filepath, "_histogramEqualized")

    # Calc image size
    image_size = get_num_pixels(image)

    # Get date and time
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")

    # Calc histogram data. Produces {"red": ndarray, "green....}
    # Use each color spectrum for analysis via processing, then
    # concatenate back together with img = np.dstack(red, green, blue)
    hist_data = pixel_histogram(image)
    hist_encode = encode_dict(hist_data)

    # Save image to database
    UserData.objects.raw(
        {"_id": username}).update(
        {"$push": {"image_name": image_name,
                   "image": image_encode,
                   "processing_time": processing_time,
                   "image_size": image_size,
                   "hist_data": hist_encode,
                   "upload_date": upload_date}})
    return


def contrast_stretched_upload(username, filepath):
    # Read original image from filepath
    image = skimage.io.imread(filepath)

    # Process image and encode it.
    start_time = time.time()
    p2, p98 = np.percentile(image, (2, 98))
    img_rescale = exposure.rescale_intensity(image, in_range=(p2, p98))
    image_encode = encode_array(img_rescale)
    processing_time = str(time.time() - start_time)

    # Create image name
    image_name = img_name_from_filepath(filepath, "_contrastStretched")

    # Calc image size
    image_size = get_num_pixels(image)

    # Get date and time
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")

    # Calc histogram data. Produces {"red": ndarray, "green....}
    # Use each color spectrum for analysis via processing, then
    # concatenate back together with img = np.dstack(red, green, blue)
    hist_data = pixel_histogram(image)
    hist_encode = encode_dict(hist_data)

    # Save image to database
    UserData.objects.raw(
        {"_id": username}).update(
        {"$push": {"image_name": image_name,
                   "image": image_encode,
                   "processing_time": processing_time,
                   "image_size": image_size,
                   "hist_data": hist_encode,
                   "upload_date": upload_date}})
    return


def log_compressed_upload(username, filepath):
    # Read original image from filepath
    image = skimage.io.imread(filepath)

    # Process image and encode it.
    start_time = time.time()
    image = log_compression(image)
    image_encode = encode_array(image)
    processing_time = str(time.time() - start_time)

    # Create image name
    image_name = img_name_from_filepath(filepath, "_logCompressed")

    # Calc image size
    image_size = get_num_pixels(image)

    # Get date and time
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")

    # Calc histogram data. Produces {"red": ndarray, "green....}
    # Use each color spectrum for analysis via processing, then
    # concatenate back together with img = np.dstack(red, green, blue)
    hist_data = pixel_histogram(image)
    hist_encode = encode_dict(hist_data)

    # Save image to database
    UserData.objects.raw(
        {"_id": username}).update(
        {"$push": {"image_name": image_name,
                   "image": image_encode,
                   "processing_time": processing_time,
                   "image_size": image_size,
                   "hist_data": hist_encode,
                   "upload_date": upload_date}})
    return


def inverted_image_upload(username, filepath):
    # Read original image from filepath
    image = skimage.io.imread(filepath)

    # Process image and encode it.
    start_time = time.time()
    inv_image = invert(image)
    inv_encoded = encode_array(inv_image)
    end_time = time.time()
    processing_time = calc_process_time(start_time, end_time)

    # Create image name
    inv_name = img_name_from_filepath(filepath, "_invertedImage")

    # Calc image size
    inv_size = get_num_pixels(inv_image)

    # Calc histogram data. Produces {"red": ndarray, "green....}
    # Use each color spectrum for analysis via processing, then
    # concatenate back together with img = np.dstack(red, green, blue)
    inv_hist = pixel_histogram(inv_image)
    hist_encoded = encode_dict(inv_hist)

    # Get date and time
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")

    # Save image to database
    UserData.objects.raw(
        {"_id": username}).update(
        {"$push": {"image_name": inv_name,
                   "image": inv_encoded,
                   "processing_time": processing_time,
                   "image_size": inv_size,
                   "hist_data": hist_encoded,
                   "upload_date": upload_date}})
    return


@app.route("/api/upload_images", methods=["POST"])
def upload_images():
    # Retrieve data sent to server
    data = request.get_json()

    # Validate Input json
    expected = {"username": (str,),
                "images": (dict,)}
    valid, message, code = validate_input_json(data, expected)
    if not valid:
        logging.warning("Attempted upload json is wrong format")
        return jsonify(message), code

    # Begin uploading images. Handle ZIPs separately?
    new_images = data["images"]
    for filepath in new_images:
        for image_name in new_images[filepath]:
            processing_type = image_name.replace(".", "_").split("_")[-2]
            if processing_type == 'original':
                original_upload(data["username"], filepath)
            elif processing_type == 'histogramEqualized':
                histogram_equalized_upload(data["username"], filepath)
            elif processing_type == 'contrastStretched':
                contrast_stretched_upload(data["username"], filepath)
            elif processing_type == 'logCompressed':
                log_compressed_upload(data["username"], filepath)
            elif processing_type == 'invertedImage':
                inverted_image_upload(data["username"], filepath)
            else:
                return jsonify("Invalid Computation Type"), 400

    return jsonify("Uploaded all images successfully")
# -----------------------------Display tab--------------------------------
# ----------------------------Download tab--------------------------------


# ----------------------------User Metrics tab----------------------------
def get_metrics(username):
        user_entry = UserMetrics.objects.raw({"_id": username})
        user = user_entry[0]
        metrics = {
                   "total_uploads": user.total_uploads,
                   "total_hist_equal": user.total_hist_equal,
                   "total_contrast_stretch": user.total_contrast_stretch,
                   "total_log_comp": user.total_log_comp,
                   "total_inv_img": user.total_inv_img
                   }
        return metrics


@app.route("/api/user_metrics/<username>", methods=["GET"])
def get_user_metrics(username):
    metrics = get_metrics(username)
    return metrics


if __name__ == "__main__":
    database_connection()
    app.run(host='0.0.0.0')
