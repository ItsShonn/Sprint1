from django.db import models


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class User(models.Model):
    email = models.EmailField(primary_key=True)
    fam = models.CharField()
    name = models.CharField()
    otc = models.CharField()
    phone = models.CharField()


class PerevalAdded(models.Model):
    time_added = models.DateTimeField(auto_now=True) # OF PEREVAL ADDED OBJECT

    beautyTitle = models.CharField()
    title = models.CharField()
    otherTitles = models.CharField()
    connect = models.CharField()
    add_time = models.CharField() # IN JSON DATA
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    spring = models.CharField(null=True)
    summer = models.CharField(null=True)
    autumn = models.CharField(null=True)
    winter = models.CharField(null=True)

    coords_id = models.ForeignKey(Coords, on_delete=models.CASCADE)

    status = models.CharField(choices=(('n', 'new'),
                                       ('p', 'pending'),
                                       ('a', 'accepted'),
                                       ('r', 'rejected')),
                              default='n')


class Images(models.Model):
    img = models.BinaryField(Null=False)


class PerevalImages(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    pereval_id = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Images, on_delete=models.CASCADE)


class PerevalAreas(models.Model):
    id_parent = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
    title = models.CharField(null=True)


class SprActivitiesTypes(models.Model):
    title = models.CharField(null=True)