import pytest
import pymongo
from UserData import UserData


def test_database_connection():
    from server import database_connection
    try:
        database_connection()
        flag = True
    except pymongo.errors.ConfigurationError:
        flag = False
    assert flag


@pytest.mark.parametrize("", [(),()])
def test_validate_input_json():
