from django.db import models


# Create your models here.
class Place(models.Model):
    name = models.TextField()
    short_description = models.TextField()
    description = models.TextField()
    rating = models.FloatField()
    image = models.FilePathField(path='static/img/places', null=1)

    def __str__(self):
        return self.name


class Cafe(models.Model):
    name = models.TextField()
    short_description = models.TextField()
    rating = models.FloatField()
    image = models.FilePathField(path='static/img/cafes', null=1)
    address = models.TextField()

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.TextField()
    short_description = models.TextField()
    cost = models.IntegerField()
    image = models.FilePathField(path='static/img/shops', null=1)

    def __str__(self):
        return self.name
