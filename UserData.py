from pymodm import MongoModel, fields
from LogIn import LogIn


class UserData(MongoModel):
    username = fields.ReferenceField(LogIn)
    image_name = fields.CharField(primary_key=True)
    image = fields.ImageField()
    upload_time = fields.DateTimeField()
    processing_time = fields.FloatField(min_value=0.0)
    image_size = fields.ListField()


if __name__ == "__main__":
    print("In UserData.py Module Main")
