from flask import Flask, jsonify, request
from datetime import datetime
from pymodm import connect, MongoModel, fields
from LogIn import LogIn
from UserData import UserData
from UserMetrics import UserMetrics
import pickle
import base64
import json
import numpy as np

app = Flask(__name__)


def database_connection():
    connect("mongodb+srv://"
            "dervil_dong_moavenzadeh_qi:BME54701@cluster0-dykvj.mongodb.net/"
            "test?retryWrites=true&w=majority")


# ----------------------------Login Screen--------------------------------
# -----------------------------Upload tab---------------------------------
# -----------------------------Display tab--------------------------------
def find_histo(id, name):
    user = UserData.objects.raw({"_id": id}).first()
    names = user.image_name
    histograms = user.hist_data
    for index, item in enumerate(names):
        if item == name:
            histogram = histograms[index]
    histogram = pickle.loads(histogram)
    return histogram


def find_metrics(id, name):
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
    names = image_list[0]
    files = image_list[1]
    for index, item in enumerate(names):
        if item == name:
            file = files[index]
    return file


def get_all_images(id):
    user = UserData.objects.raw({"_id": id}).first()
    name = user.image_name
    image = user.image
    list = [name, image]
    return list

@app.route("/api/histo/<id>/<name>", methods=["GET"])
def histo(id, name):
    histo = find_histo(id, name)
    print(type(histo))
    red = histo["red"][0].tolist()
    green = histo["green"][0].tolist()
    blue = histo["blue"][0].tolist()
    output = [red, green, blue]
    return jsonify(output), 200

@app.route("/api/get_image_metrics/<id>/<name>", methods=["GET"])
def get_image_metrics(id, name):
    metrics = find_metrics(id, name)
    return jsonify(metrics), 200


@app.route("/api/fetch_image/<id>/<name>", methods=["GET"])
def fetch_image(id, name):
    image_list = get_all_images(id)
    image_file = find_file(image_list, name)
    image_file = np.frombuffer(base64.b64decode(image_file), np.uint8)
    image_file = image_file.tolist()
    return jsonify(image_file), 200


@app.route("/api/get_all_images/<id>", methods=["GET"])
def image_list(id):
    output_list = get_all_images(id)
    return jsonify(output_list[0]), 200
# ----------------------------Download tab--------------------------------
# ----------------------------User Metrics tab----------------------------


if __name__ == "__main__":
    database_connection()
    app.run()
