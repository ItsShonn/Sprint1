from django.db import models


class PerevalImages(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    img = models.BinaryField(Null=False)