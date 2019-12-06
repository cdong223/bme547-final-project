from pymodm import MongoModel, fields


class LogIn(MongoModel):
    username = fields.CharField(primary_key=True)


if __name__ == "__main__":
    print("In LogIn.py Module Main")
