from django.test import TestCase

from belka.models import UserFavourites


# python manage.py test belka.tests.test_model

class TestUserFavourites(TestCase):
    """
    Class for testing UserFavourites model
    """

    def setUp(self):
        self.model = UserFavourites()

    def test_save_get_FavouritePlaces(self):
        places_ids = ["1", "2", "3"]
        self.model.saveFavouritePlaces(["1", "2", "3"])
        self.assertEqual(places_ids, self.model.getFavouritePlaces())

    def tearDown(self):
        pass
