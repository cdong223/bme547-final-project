from flask import Flask, jsonify, request
from datetime import datetime
from pymodm import connect, MongoModel, fields
from LogIn import LogIn
from UserData import UserData
from UserMetrics import UserMetrics

app = Flask(__name__)


def database_connection():
    connect("mongodb+srv://dervil_dong_moavenzadeh_qi:BME54701@cluster0-"
            "dykvj.mongodb.net/test?retryWrites=true&w=majority")


# ----------------------------Login Screen--------------------------------
def patient_exists(username):
    user = LogIn.objects.raw({"_id": username})
    if(user.count() == 0):
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
# -----------------------------Display tab--------------------------------
# ----------------------------Download tab--------------------------------
# ----------------------------User Metrics tab----------------------------


if __name__ == "__main__":
    database_connection()
    app.run()
