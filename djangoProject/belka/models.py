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
    geo_x = models.FloatField(default=0)
    geo_y = models.FloatField(default=0)

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
    favourite_places = models.TextField(default="")

    def getFavouritePlaces(self):
        return self.favourite_places.split("$")[:-1]

    def saveFavouritePlaces(self, new_places):
        self.favourite_places = '$'.join(new_places) + "$"

    def addId(self, new_id):
        temp_places = self.getFavouritePlaces()
        if new_id not in temp_places:
            self.favourite_places += new_id + "$"
            self.save()
        else:
            self.favourite_places = self.favourite_places.replace(str(new_id) + "$", "", 1)
            self.save()

    def __str__(self):
        return "Favourites of user " + str(self.user_id)


class Route(models.Model):
    name = models.TextField()
    short_description = models.TextField()
    rating = models.FloatField()
    votes = models.IntegerField()
    creator = models.IntegerField()
    marshrut = models.TextField()

    def getRoute(self):
        return self.marshrut.split("$")[:-1]

    def refreshRating(self, new_rate):
        prev_sum = self.rating * self.votes
        self.votes += 1
        self.rating = (prev_sum + new_rate) / self.votes

    def __str__(self):
        return str(self.name)


class Event(models.Model):
    name = models.TextField()
    cost = models.IntegerField()
    image = models.FilePathField(path='static/img/events', null=1)
    place = models.TextField()
    time = models.TimeField()
    date = models.DateTimeField()
    link = models.TextField()
    type = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    date = models.DateField()
    persons = models.IntegerField()
    gid = models.IntegerField(default=-1)
    comments = models.TextField(default="")
    ordered_user = models.IntegerField(default=0)
    name = models.TextField(default="Заказ")

    def __str__(self):
        return "Заказ на " + str(self.date)
