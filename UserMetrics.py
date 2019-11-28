from pymodm import MongoModel, fields
from LogIn import LogIn


class UserMetrics(MongoModel):
    username = fields.ReferenceField(LogIn, primary_key=True)
    total_uploads = fields.IntegerField(min_value=0)
    total_hist_equal = fields.IntegerField(min_value=0)
    total_contrast_stretch = fields.IntegerField(min_value=0)
    total_log_comp = fields.IntegerField(min_value=0)
    total_inv_img = fields.IntegerField(min_value=0)


if __name__ == "__main__":
    print("In UserMetrics.py Module Main")
