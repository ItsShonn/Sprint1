from django.db import models


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


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
    otherTitles = models.CharField(null=True, blank=True)
    connect = models.CharField(null=True, blank=True)
    add_time = models.CharField() # IN JSON DATA
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    spring = models.CharField(null=True, blank=True)
    summer = models.CharField(null=True, blank=True)
    autumn = models.CharField(null=True, blank=True)
    winter = models.CharField(null=True, blank=True)

    coords_id = models.ForeignKey(Coords, on_delete=models.CASCADE)

    status = models.CharField(choices=(('n', 'new'),
                                       ('p', 'pending'),
                                       ('a', 'accepted'),
                                       ('r', 'rejected')),
                              default='n')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Images(models.Model):
    img = models.BinaryField(default=False, editable=True, null=False)
    title = models.CharField(default='')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class PerevalImages(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    pereval_id = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
    image_id = models.ForeignKey(Images, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class PerevalAreas(models.Model):
    id_parent = models.ForeignKey(PerevalAdded, on_delete=models.CASCADE)
    title = models.CharField(null=True)


class SprActivitiesTypes(models.Model):
    title = models.CharField(null=True)