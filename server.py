from flask import Flask, jsonify, request
from datetime import datetime
from pymodm import connect, MongoModel, fields
from LogIn import LogIn
from UserData import UserData
from UserMetrics import UserMetrics
import base64
import json
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
    """Connect to database and configure logging

    Returns:
        None
    """
    connect("mongodb+srv://dervil_dong_moavenzadeh_qi"
            ":BME54701@cluster0-dykvj.mongodb.net"
            "/test?retryWrites=true&w=majority")
    logging.basicConfig(filename="image_server.log",
                        level=logging.INFO,
                        filemode='w')


# ----------------------------Login Screen--------------------------------
def patient_exists(username):
    """Checks to see if given username already exists in the database

    Args:
        username (str): username to check in database

    Returns:
        bool: True if username already registered. False otherwise.
    """
    user = LogIn.objects.raw({"_id": username})
    if user.count() == 0:
        return False
    return True


def register_user(username):
    """Registers new username in database

    Args:
        username (str): username to register in database

    Returns:
        None
    """
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
    """POST request to login into database

    Args:
        None

    Returns:
        JSON: Str indicating login successful or bad request if username
              does not exists.
    """
    username = request.get_json()
    if patient_exists(username) is False:
        return jsonify("Bad Login Request"), 400
    return jsonify("Login Successful"), 200


@app.route("/api/new_user", methods=["POST"])
def add_new_user():
    """POST request to register new username in database

    Args:
        None

    Returns:
        JSON: Str indicating registration successful or bad request if username
              already exists in database.
    """
    username = request.get_json()
    if patient_exists(username) is True:
        return jsonify("Bad New User Request"), 400
    register_user(username)
    return jsonify("New User Registration Successful"), 200


# -----------------------------Upload tab---------------------------------
def validate_input_json(data, expected):
    """Validates json recieved from request

    Args:
        data (): json recieved from request
        expected (dict): json format expected from request

    Returns:
        bool: state of validity, True if good request
        str: reason for validity
        int: request status code
    """
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
    """Isolates image file name from path

    Args:
        filepath (str): location of image

    Returns:
        str: head filepath and image name
    """
    # Returns image name from file path
    head, tail = os.path.split(filepath)
    return head, tail


def get_db_img_name(img_name, processing):
    """Creates image name given processing type

    Args:
        img_name (str): image name
        processing (str): processing applied

    Returns:
        str: Created image name
    """
    img_name, filetype = img_name.split('.')
    return img_name + processing + "." + filetype


def img_name_from_filepath(filepath, processing):
    """Creates image name from filepath

    Args:
        filepath (str): location of image
        processing (str): Processing type to apply

    Returns:
        str: image name for storage
    """
    head, tail = isolate_image_name_from_path(filepath)
    img_name = get_db_img_name(tail, processing)  # Append original image name
    return img_name


def is_image_present(username, img_name):
    """Checks if image is present for user

    Args:
        username (str): user checking image for
        img_name (str): name of image to check

    Returns:
        bool: presence of image. True if present
    """
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
    """POST request to check which images are present for user

    Returns:
        dict: Dictionary of images present and images not
        present for user
    """
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
    """Retrieve image size from image

    Args:
        image (ndarray): image to retrieve size

    Returns:
        str: image size as COLxROWxDEP
    """
    shape = image.shape
    image_size = str(shape[1])+"x"+str(shape[0])+"x"+str(shape[2])
    return image_size


def pixel_histogram(image):
    """Creates histogram of pixel intensities

    Args:
        image (ndarray): image file

    Returns:
        dict: Dictionary of color component pixel histograms
    """
    red_hist = skimage.exposure.histogram(image[:, :, 0])
    green_hist = skimage.exposure.histogram(image[:, :, 1])
    blue_hist = skimage.exposure.histogram(image[:, :, 2])
    hist_dict = {"red": red_hist,
                 "green": green_hist,
                 "blue": blue_hist}
    return hist_dict


def is_first_upload(username):
    """Checks if user has any images stored in DB

    Args:
        username (str): user

    Returns:
        bool: state of user images. True if no image
        present for user
    """
    return not UserData.objects.raw({"_id": username}).count()


def encode_array(array):
    """Encodes array to byte64

    Args:
        array (ndarray): array

    Returns:
        byte64: encoded array
    """
    # Encoding of 3darray to save in database
    encoded_array = base64.b64encode(array)
    return encoded_array


def decode_array(array):
    """Decodes byte64 array

    Args:
        array (byte64): stored file to decode

    Returns:
        ndarray: decoded array
    """
    # Decoding of 3darray to use for processing
    decoded_array = np.frombuffer(base64.b64decode(array), np.uint8)
    return decoded_array


def encode_dict(dictionary):
    """Encodes dictinary to binary

    Args:
        dictionary (dict): dictionary to encode

    Returns:
        binary: encoded dictionary
    """
    encoded_dict = Binary(pickle.dumps(dictionary, protocol=3))
    return encoded_dict


def decode_dict(dictionary):
    """Decodes binary dictionary to native dictionary

    Args:
        dictionary (binary): storage to decode

    Returns:
        dict: decoded dictionary
    """
    decoded_dict = pickle.loads(dictionary)
    return decoded_dict


def calc_process_time(t1, t2):
    """Calculates difference between times

    Args:
        t1 (float): initial time
        t2 (float): end time

    Returns:
        str: difference in times
    """
    return str(t2 - t1)


def histogram_equalization(image):
    """Equalized each color array individual and
        returns equalized image

    Args:
        image (ndarray): image to equalize

    Returns:
        ndarray: equalized image
    """
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
    """Inverts image pixel intensities

    Args:
        image (ndarray): image to invert

    Returns:
        ndarray: Inverted image
    """
    inv_image = util.invert(image)
    return inv_image


def log_compression(img):
    """Logarithmic scaling of image

    Args:
        img (ndarray): image to scale

    Returns:
        ndarray: scaled image
    """
    # LOG COMPRESSED IMAGE PROCESSING AND ENCODING OF IMAGE
    # Apply log transform
    img_log = skimage.exposure.adjust_log(img)
    return img_log


def original_upload(username, filepath):
    """Performs encoding and uploads to database along with associated data
       metrics (upload time, processing time, histogram, size). Checks to see
       if username is already associated with a UserData document and uploads
       accordingly.

    Args:
        username (str): username to upload to in database
        filepath (str): filepath of image to be processed and encoded

    Returns:
        None
    """
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
    """Performs histogram equalization/encoding and uploads to database along
       with associated data metrics (upload time, processing time, histogram,
       size).

    Args:
        username (str): username to upload to in database
        filepath (str): filepath of image to be processed and encoded

    Returns:
        None
    """
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
    """Performs contrast stretching/encoding and uploads to database along
       with associated data metrics (upload time, processing time, histogram,
       size).

    Args:
        username (str): username to upload to in database
        filepath (str): filepath of image to be processed and encoded

    Returns:
        None
    """
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
    """Performs log compression/encoding and uploads to database along
       with associated data metrics (upload time, processing time, histogram,
       size).

    Args:
        username (str): username to upload to in database
        filepath (str): filepath of image to be processed and encoded

    Returns:
        None
    """
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
    """Performs image inversion/encoding and uploads to database along with
       associated data metrics (upload time, processing time, histogram,
       size).

    Args:
        username (str): username to upload to in database
        filepath (str): filepath of image to be processed and encoded

    Returns:
        None
    """
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
    """POST request to process and upload images to the database. Receives
       the username associated with the request, the list of images to be
       processed, and the processing type. Calls the appropriate processing
       pathways.

    Args:
        None

    Returns:
        JSON: Str indicating successful upload.
    """
    # Retrieve data sent to server
    data = request.get_json()

    # Validate Input json
    expected = {"username": (str,),
                "images": (dict,)}
    valid, message, code = validate_input_json(data, expected)
    if not valid:
        logging.warning("Attempted upload json is wrong format")
        return jsonify(message), code

    # Pull user metrics for updating
    user_entry = UserMetrics.objects.raw({"_id": data["username"]})
    user = user_entry[0]
    total_uploads = user.total_uploads
    total_hist_equal = user.total_hist_equal
    total_contrast_stretch = user.total_contrast_stretch
    total_log_comp = user.total_log_comp
    total_inv_img = user.total_inv_img

    # Begin uploading images. Handle ZIPs separately?
    new_images = data["images"]
    for filepath in new_images:
        for image_name in new_images[filepath]:
            processing_type = image_name.replace(".", "_").split("_")[-2]
            if processing_type == 'original':
                original_upload(data["username"], filepath)
                total_uploads += 1
            elif processing_type == 'histogramEqualized':
                histogram_equalized_upload(data["username"], filepath)
                total_hist_equal += 1
            elif processing_type == 'contrastStretched':
                contrast_stretched_upload(data["username"], filepath)
                total_contrast_stretch  += 1
            elif processing_type == 'logCompressed':
                log_compressed_upload(data["username"], filepath)
                total_log_comp += 1
            elif processing_type == 'invertedImage':
                inverted_image_upload(data["username"], filepath)
                total_inv_img += 1
            else:
                return jsonify("Invalid Computation Type"), 400

    # Update user metrics
    metrics = UserMetrics(username=data["username"],
                          total_uploads=total_uploads,
                          total_hist_equal=total_hist_equal,
                          total_contrast_stretch=total_contrast_stretch,
                          total_log_comp=total_log_comp,
                          total_inv_img=total_inv_img)
    metrics.save()

    return jsonify("Uploaded all images successfully")


# -----------------------------Display tab--------------------------------
def find_histo(id, name):
    """Given the user id and the image name, return the histogram value in a
       np array

    Args:
        id (str): user id in the database
        name (str): name of the file to find histogram of

    Returns:
        np.ndarray: contains histogram data
    """
    user = UserData.objects.raw({"_id": id}).first()
    names = user.image_name
    histograms = user.hist_data
    for index, item in enumerate(names):
        if item == name:
            histogram = histograms[index]
    histogram = pickle.loads(histogram)
    return histogram


def find_metrics(id, name):
    """Given the user id and the image name, return the image metrics value
       in a list

    Args:
        id (str): user id in the database
        name (str): name of the file to find metrics of

    Returns:
        list: contains image metrics data (CPU time, size of image, and upload
        timestamp)
    """
    user = UserData.objects.raw({"_id": id}).first()
    names = user.image_name
    CPU_times = user.processing_time
    sizes = user.image_size
    upload_times = user.upload_date
    histograms = user.hist_data
    for index, item in enumerate(names):
        if item == name:
            CPU_time = CPU_times[index]
            size = sizes[index]
            upload_time = upload_times[index]
    output_list = [CPU_time, size, upload_time]
    return output_list


def find_file(image_list, name):
    """Given the list of image, the list of image files and the name of the
       image, return the image file in the corresponding location

    Args:
        image_list (list): a list of list. First item is list of image names.
        Second item is list of image files.

    Returns:
        string: the image file encoded in base64
    """
    names = image_list[0]
    files = image_list[1]
    for index, item in enumerate(names):
        if item == name:
            file = files[index]
    return file


def get_all_images(id):
    """Given the user id, return the list of images the user uploaded

    Args:
        id (str): user id in the database

    Returns:
        list: list of image names and the image files
    """
    user = UserData.objects.raw({"_id": id}).first()
    name = user.image_name
    image = user.image
    list = [name, image]
    return list


@app.route("/api/histo/<id>/<name>", methods=["GET"])
def histo(id, name):
    """GET request. Given the user id and the image name, return the histogram
       data in list

    Args:
        id (str): user id in the database
        name (str): name of the file to find histogram of

    Returns:
        JSON: contains histogram data in list of list
        Status code: indicate whether request is successful
    """
    histo = find_histo(id, name)
    red = histo["red"][0].tolist()
    green = histo["green"][0].tolist()
    blue = histo["blue"][0].tolist()
    output = [red, green, blue]
    return jsonify(output), 200


@app.route("/api/get_image_metrics/<id>/<name>", methods=["GET"])
def get_image_metrics(id, name):
    """GET request. Given the user id and the image name, return the image
       metrics

    Args:
        id (str): user id in the database
        name (str): name of the file to find metrics of

    Returns:
        JSON: contains metrics data in list
        Status code: indicate whether request is successful
    """
    metrics = find_metrics(id, name)
    return jsonify(metrics), 200


@app.route("/api/fetch_image/<id>/<name>", methods=["GET"])
def fetch_image(id, name):
    """GET request. Given the user id and the image name, return the image
       file.

    Args:
        id (str): user id in the database
        name (str): name of the file to find image file of

    Returns:
        JSON: contains metrics info in list
        Status code: indicate whether request is successful
    """
    image_list = get_all_images(id)
    image_file = find_file(image_list, name)
    image_file = np.frombuffer(base64.b64decode(image_file), np.uint8)
    image_file = image_file.tolist()
    return jsonify(image_file), 200


@app.route("/api/get_all_images/<id>", methods=["GET"])
def image_list(id):
    """GET request. Given the user id, return the list of image stored for
       the user.

    Args:
        id (str): user id in the database

    Returns:
        JSON: contains image name in list
    """
    output_list = get_all_images(id)
    return jsonify(output_list[0]), 200


# ----------------------------Download tab--------------------------------
# ----------------------------User Metrics tab----------------------------
def get_metrics(username):
    """Connects to database to retrive user_metrics data for given username

    Args:
        username (str): username to check in database

    Returns:
        dict: user metrics as integers
    """
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
    """GET request to retrieve user_metrics data for given username

    Args:
        username (str): username to check in database

    Returns:
        JSON: dictionary containing user metrics as integers
    """
    metrics = get_metrics(username)
    return jsonify(metrics)


if __name__ == "__main__":
    database_connection()
    app.run(host='0.0.0.0')
