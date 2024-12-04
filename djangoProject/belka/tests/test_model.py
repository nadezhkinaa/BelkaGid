from django.test import TestCase

from belka.models import UserFavourites


# python manage.py test belka.tests.test_model

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

    def test_add_id_FavouritePlaces_new(self):
        places_ids = ["1", "2", "3"]
        self.model.saveFavouritePlaces(places_ids)
        place_id_new = "4"
        self.model.addId(place_id_new)

        self.assertEqual(["1", "2", "3", "4"], self.model.getFavouritePlaces())

    def test_add_id_FavouritePlaces_excisting(self):
        places_ids = ["1", "2", "3"]
        self.model.saveFavouritePlaces(places_ids)
        place_id_new = "2"
        self.model.addId(place_id_new)

        self.assertEqual(["1", "2", "3"], self.model.getFavouritePlaces())

    def tearDown(self):
        pass
