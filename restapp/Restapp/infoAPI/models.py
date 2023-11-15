from django.db import models


class Userdb(models.Model):
    name = models.CharField(max_length=30, default="Zaw Hein")
    email = models.CharField(max_length=50, default="example@gmail.com")
    phno = models.CharField(max_length=11, default="09260000000")
    degree = models.CharField(max_length=50, default="BE-Electronics")
