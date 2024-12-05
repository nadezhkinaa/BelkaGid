import datetime

from django.test import TestCase

from belka.models import UserFavourites, Route, Event, Order, Shop, Cafe, Place


# python manage.py test belka.tests.test_model

class TestPlace(TestCase):
    """
    Class for testing Place model
    """

    def setUp(self):
        self.model = Place()

    def test_str(self):
        self.model.name = "Place 1"
        self.assertEqual(str(self.model), "Place 1")

    def tearDown(self):
        pass


class TestCafe(TestCase):
    """
    Class for testing Cafe model
    """

    def setUp(self):
        self.model = Cafe()

    def test_str(self):
        self.model.name = "Cafe 1"
        self.assertEqual(str(self.model), "Cafe 1")

    def tearDown(self):
        pass


class TestShop(TestCase):
    """
    Class for testing Order model
    """

    def setUp(self):
        self.model = Shop()

    def test_str(self):
        self.model.name = "Shop 1"
        self.assertEqual(str(self.model), "Shop 1")

    def tearDown(self):
        pass


class TestUserFavourites(TestCase):
    """
    Class for testing UserFavourites model
    """

    def setUp(self):
        self.model = UserFavourites()
        self.model.user_id = 1

    def test_save_get_FavouritePlaces(self):
        places_ids = ["1", "2", "3"]
        self.model.saveFavouritePlaces(places_ids)
        self.assertEqual(places_ids, self.model.getFavouritePlaces())

    def test_add_FavouritePlace(self):
        places_ids = ["1", "2", "3"]
        self.model.saveFavouritePlaces(places_ids)
        place_id_new = "4"
        self.model.addId(place_id_new)

        self.assertEqual(["1", "2", "3", "4"], self.model.getFavouritePlaces())

    def test_remove_FavouritePlaces(self):
        places_ids = ["1", "2", "3"]
        self.model.saveFavouritePlaces(places_ids)
        place_id_new = "2"
        self.model.addId(place_id_new)

        self.assertEqual(["1", "3"], self.model.getFavouritePlaces())

    def test_str(self):
        self.assertEqual(str(self.model), "Favourites of user 1")

    def tearDown(self):
        pass


class TestRoute(TestCase):
    """
    Class for testing Route model
    """

    def setUp(self):
        self.model = Route()

    def test_get_route(self):
        self.model.marshrut = "1$2$3$"
        self.assertEqual(self.model.getRoute(), ["1", "2", "3"])

    def test_refresh_rating_one_rate(self):
        self.model.rating = 3.00
        self.model.votes = 1

        self.model.refreshRating(5.00)
        self.assertEqual(self.model.rating, 4.00)

    def test_refresh_rating_multiply_rates(self):
        self.model.rating = 3.67
        self.model.votes = 10

        self.model.refreshRating(2.87)
        self.assertEqual(self.model.rating, (3.67 * 10 + 2.87) / 11)

    def test_str(self):
        self.model.name = "Route 1"
        self.assertEqual(str(self.model), "Route 1")

    def tearDown(self):
        pass


class TestEvent(TestCase):
    """
    Class for testing Event model
    """

    def setUp(self):
        self.model = Event()

    def test_str(self):
        self.model.name = "Event 1"
        self.assertEqual(str(self.model), "Event 1")

    def tearDown(self):
        pass


class TestOrder(TestCase):
    """
    Class for testing Order model
    """

    def setUp(self):
        self.model = Order()

    def test_str(self):
        self.model.date = datetime.datetime.strptime('2024-10-15', '%Y-%m-%d').date()
        self.assertEqual(str(self.model), "Заказ на 2024-10-15")

    def tearDown(self):
        pass
