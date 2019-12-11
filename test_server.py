import pytest
from LogIn import LogIn
from UserMetrics import UserMetrics
from pymodm import connect


def connect_db():
    connect("mongodb+srv://dervil_dong_moavenzadeh_qi:BME54701@cluster0-"
            "dykvj.mongodb.net/test?retryWrites=true&w=majority")


@pytest.mark.parametrize("username, expected", [
                ("unit_test_get_metrics",
                 {
                    "total_uploads": 8,
                    "total_hist_equal": 3,
                    "total_contrast_stretch": 4,
                    "total_log_comp": 1,
                    "total_inv_img": 0
                    })
])
def test_get_metrics(username, expected):
    from server import get_metrics
    connect_db()
    username = "unit_test_get_metrics"
    user = LogIn(username=username).save()
    metrics = UserMetrics(username=username,
                          total_uploads=8,
                          total_hist_equal=3,
                          total_contrast_stretch=4,
                          total_log_comp=1,
                          total_inv_img=0)
    metrics.save()
    result = get_metrics(username)
    assert result == expected
    UserMetrics.objects.raw({"_id": "unit_test_get_metrics"}).delete()


@pytest.mark.parametrize("username, expected", [
                                ("unit_test_patient_exists", True),
                                ("other", False)
])
def test_patient_exists(username, expected):
    from server import patient_exists
    connect_db()
    user = LogIn(username="unit_test_patient_exists").save()
    result = patient_exists(username)
    assert result == expected
    LogIn.objects.raw({"_id": "unit_test_patient_exists"}).delete()


@pytest.mark.parametrize("username, expected", [
                                ("unit_test_register_user",
                                 ["unit_test_register_user",
                                  0, 0, 0, 0, 0])
])
def test_register_user(username, expected):
    from server import register_user
    connect_db()
    register_user(username)

    login_user_entry = LogIn.objects.raw({"_id": username})
    login_user = login_user_entry[0]
    login_username = login_user.username
    metrics_user_entry = UserMetrics.objects.raw({"_id": username})
    metrics_user = metrics_user_entry[0]
    total_uploads = metrics_user.total_uploads
    total_hist_equal = metrics_user.total_hist_equal
    total_contrast_stretch = metrics_user.total_contrast_stretch
    total_log_comp = metrics_user.total_log_comp
    total_inv_img = metrics_user.total_inv_img

    result = [login_username, total_uploads, total_hist_equal,
              total_contrast_stretch, total_log_comp, total_inv_img]

    assert result == expected
    LogIn.objects.raw({"_id": username}).delete()
    UserMetrics.objects.raw({"_id": username}).delete()