from django.db import models


class PerevalAdded(models.Model):
    pass


class Images(models.Model):
    img = models.BinaryField(Null=False)


class PerevalImages(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    pereval_id = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Images, on_delete=models.CASCADE)


