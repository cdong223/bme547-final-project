import pytest
from pymodm import connect, MongoModel, fields
import dns

from LogIn import LogIn
from UserData import UserData
from UserMetrics import UserMetrics

connect("mongodb+srv://"
        "dervil_dong_moavenzadeh_qi:BME54701@cluster0-dykvj.mongodb.net/"
        "test?retryWrites=true&w=majority")


@pytest.mark.parametrize("input, expected1, expected2",
                         [('1', ["a.png", "b.png"], ["imageA", "imageB"]),
                          ('2', ["a.jpg", "a_hist.jpg"], ["imageA", "histA"])])
def test_get_all_images(input, expected1, expected2):
    from server import get_all_images
    p = LogIn(username='1')
    p.save()
    p = UserData(username='1', image_name=["a.png", "b.png"],
                 image=["imageA", "imageB"], processing_time=["0.5s", "0.2s"],
                 image_size=["400x200, 300x300"],
                 hist_data=["histA", "histB"],
                 upload_dat=["2019/12/8", "2019/12/9"])
    p.save()
    p = LogIn(username='2')
    p.save()
    p = UserData(username='2', image_name=["a.jpg", "a_hist.jpg"],
                 image=["imageA", "histA"], processing_time=["0.3s", "0.4s"],
                 image_size=["400x100, 200x200"],
                 hist_data=["histA", "histhistA"],
                 upload_dat=["2019/12/1", "2019/12/2"])
    p.save()
    result = get_all_images(input)
    assert result[0] == expected1
    assert result[1] == expected2
    UserData.objects.raw({"_id": "1"}).delete()
    UserData.objects.raw({"_id": "2"}).delete()
    LogIn.objects.raw({"_id": "1"}).delete()
    LogIn.objects.raw({"_id": "2"}).delete()
