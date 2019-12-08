from flask import Flask, jsonify, request
from datetime import datetime
from pymodm import connect, MongoModel, fields
from LogIn import LogIn
from UserData import UserData
from UserMetrics import UserMetrics

app = Flask(__name__)


def database_connection():
    connect("mongodb+srv://dervil_dong_moavenzadeh_qi:BME54701@cluster0-dykvj.mongodb.net/test?retryWrites=true&w=majority")


# ----------------------------Login Screen--------------------------------
# -----------------------------Upload tab---------------------------------
# -----------------------------Display tab--------------------------------
def get_all_images(id):
    user = UserData.objects.raw({"_id": id}).first()
    name = user.image_name
    image = user.image
    list = [name, image]
    return list

@app.route("/api/get_all_images", methods=["POST"])
def image_list():
    user_id = request.get_json()
    output_list = get_all_images(user_id)
    return jsonify(output_list), 200
# ----------------------------Download tab--------------------------------
# ----------------------------User Metrics tab----------------------------


if __name__ == "__main__":
    database_connection()
    app.run()
