from pymodm import MongoModel, fields
from LogIn import LogIn


class UserData(MongoModel):
    username = fields.ReferenceField(LogIn, primary_key=True)
    image_name = fields.ListField()
    image = fields.ListField()
    processing_time = fields.ListField()
    image_size = fields.ListField()
    hist_data = fields.ListField()
    upload_date = fields.ListField()


if __name__ == "__main__":
    print("In UserData.py Module Main")
