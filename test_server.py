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
