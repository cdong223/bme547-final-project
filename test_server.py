import pytest
import pymongo
from UserData import UserData
from LogIn import LogIn


def test_database_connection():
    from server import database_connection
    try:
        database_connection()
        flag = True
    except pymongo.errors.ConfigurationError:
        flag = False
    assert flag


@pytest.mark.parametrize("in_dict, ex_dict, expected", [
    ({"username": "sm642",
      "filepaths": ["filepath1", "filepath2"],
      "processing": "_histogramEqualized"},
     {"username": (str,),
      "filepaths": (list,),
      "processing": (str,)},
     "Input json is valid."),
    (["username", "sm642",
      "filepaths", ["filepath1", "filepath2"],
      "processing", "_histogramEqualized"],
     {"username": (str,),
      "filepaths": (list,),
      "processing": (str,)},
     "Data entry is not in dictionary format."),
    ({"unexpected_key": "sm642",
      "filepaths": ["filepath1", "filepath2"],
      "processing": "_histogramEqualized"},
     {"username": (str,),
      "filepaths": (list,),
      "processing": (str,)},
     "Dictionary keys are not in correct format."),
    ({"username": "sm642",
      "filepaths": ["filepath1", "filepath2"],
      "processing": "_histogramEqualized"},
     {"missing_dict_key": (str,),
      "username": (str,),
      "filepaths": (list,),
      "processing": (str,)},
     "Dictionary does not have enough information. Missing keys."),
    ({"username": "sm642",
      "filepaths": "filepath1",
      "processing": "_histogramEqualized"},
     {"username": (str,),
      "filepaths": (list,),
      "processing": (str,)},
     "Dictionary values are not correct. Invalid data types.")
])
def test_validate_input_json(in_dict, ex_dict, expected):
    from server import validate_input_json
    valid, message, code = validate_input_json(in_dict, ex_dict)
    assert expected == message


@pytest.mark.parametrize("filepath, expected", [
    ('C:/Users/moave/Pictures/Saved Pictures/Aviary Stock Photo 1.png',
     'Aviary Stock Photo 1.png'),
    ('moave/Pictures/Saved Pictures/Aviary Stock Photo 1.png',
     'Aviary Stock Photo 1.png'),
    ('Aviary Stock Photo 1.png',
     'Aviary Stock Photo 1.png')
])
def test_isolate_image_name_from_path(filepath, expected):
    from server import isolate_image_name_from_path
    head, img_name = isolate_image_name_from_path(filepath)
    assert expected == img_name


@pytest.mark.parametrize("img_name, processing, expected", [
    ('Aviary Stock Photo 1.png',
     '_original',
     'Aviary Stock Photo 1_original.png')
])
def test_get_db_img_name(img_name, processing, expected):
    from server import get_db_img_name
    img_name = get_db_img_name(img_name, processing)
    assert expected == img_name


@pytest.mark.parametrize("filepath, processing, expected", [
    ('C:/Users/moave/Pictures/Saved Pictures/Aviary Stock Photo 1.png',
     '_original',
     'Aviary Stock Photo 1_original.png')
])
def test_img_name_from_filepath(filepath, processing, expected):
    from server import img_name_from_filepath
    img_name = img_name_from_filepath(filepath, processing)
    assert expected == img_name


@pytest.mark.parametrize("stored_username, stored_img_name, username, img_name, expected", [
    ('...',
     'Aviary_original.png',
     '...',
     'Aviary_original.png',
     True),
    ('...',
     'Aviary_original.png',
     'unstored_username',
     'Aviary_original.png',
     False),
    ('...',
     'Aviary_original.png',
     '...',
     'Aviary_unstored.png',
     False),
])
def test_is_image_present(stored_username, stored_img_name, username, img_name, expected):
    from server import is_image_present
    user = LogIn(username=stored_username)
    user.save()
    user_data = UserData(username=user,
                         image_name=[stored_img_name])
    user_data.save()
    value = is_image_present(username, img_name)
    assert expected == value
    UserData.objects.raw({"_id": stored_username}).delete()
    LogIn.objects.raw({"_id": stored_username}).delete()


if __name__ == "__main__":
    test_database_connection()
    print("test_server.py Main")
