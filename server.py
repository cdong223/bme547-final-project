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
# -----------------------------Upload tab---------------------------------
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
    app.run()
