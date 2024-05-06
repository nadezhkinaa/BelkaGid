from django.db import models


# Create your models here.

class Place(models.Model):
    name = models.TextField()
    short_description = models.TextField()
    description = models.TextField()
    rating = models.FloatField()
    image = models.FilePathField(path='static/img/places', null=1)
    # парки - 1,  музеи - 2, театры - 3, памятники - 4, церкви - 5, прочее - 6
    type = models.IntegerField(default=0)
    map_id = models.IntegerField(default=0)
    redirect_url = models.TextField(default="places")
    map_x = models.IntegerField(default=0)
    map_y = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Cafe(models.Model):
    name = models.TextField()
    short_description = models.TextField()
    rating = models.FloatField()
    image = models.FilePathField(path='static/img/cafes', null=1)
    # кафе - 1, рестораны - 2, фастфуд - 3, бары - 4, столовые - 5, прочее - 6
    type = models.IntegerField(default=0)
    map_id = models.IntegerField(default=0)
    redirect_url = models.TextField(default="cafe")
    map_x = models.IntegerField(default=0)
    map_y = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.TextField()
    cost = models.IntegerField()
    image = models.FilePathField(path='static/img/shops', null=1)
    # футболки - 1, кофты - 2, прочее - 3
    type = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserFavourites(models.Model):
    user_id = models.IntegerField()
    favourite_places = models.TextField()

    def getFavouritePlaces(self):
        return self.favourite_places.split("$")

    def saveFavouritePlaces(self, new_places):
        self.favourite_places = '$'.join(new_places)

    def __str__(self):
        return "Favourites of user " + str(self.user_id)
