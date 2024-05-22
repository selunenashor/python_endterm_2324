from django.db import models


class CustomUser(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    username = models.TextField(max_length=100, unique=True)
    password = models.TextField(max_length=100)
    email = models.EmailField()
    phone = models.TextField(max_length=20, blank=True)

    def __init__(self, username=None, password=None, email=None, phone="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone

    def getID(self):
        return self.id
