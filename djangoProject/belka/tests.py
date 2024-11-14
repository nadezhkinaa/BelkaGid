from django.contrib.auth.models import User
from django.test import TestCase
from belka.models import Place
from django.test.client import Client


# some_path_to/virtualenv/lib/python3.11/site-packages/django/test/runner.py (probably at line 1044)
# def run_tests(self, test_labels, some=None, **kwargs):
# add any parameter like some=None
# https://docs.djangoproject.com/en/dev/topics/testing/overview/
# https://habr.com/ru/articles/122156/
def create_places():
    Place.objects.create(name="Место 1", short_description="Краткое описание для места 1", image=None,
                         description="Полное описание для места 1", rating=4.99, type=1, map_id=2,
                         redirect_url="redir_url", map_x=12, map_y=21, geo_x=120, geo_y=123)
    Place.objects.create(name="Место 2", short_description="Краткое описание для места 2", image=None,
                         description="Полное описание для места 2", rating=4.5, type=2, map_id=3,
                         redirect_url="redir_url_2", map_x=15, map_y=25, geo_x=125, geo_y=128)

    Place.objects.create(name="Место 3", short_description="Краткое описание для места 3", image=None,
                         description="Полное описание для места 3", rating=3.8, type=3, map_id=4,
                         redirect_url="redir_url_3", map_x=18, map_y=30, geo_x=130, geo_y=133)

    Place.objects.create(name="Место 4", short_description="Краткое описание для места 4", image=None,
                         description="Полное описание для места 4", rating=4.2, type=1, map_id=5,
                         redirect_url="redir_url_4", map_x=21, map_y=35, geo_x=135, geo_y=138)

    Place.objects.create(name="Место 5", short_description="Краткое описание для места 5", image=None,
                         description="Полное описание для места 5", rating=4.9, type=2, map_id=6,
                         redirect_url="redir_url_5", map_x=24, map_y=40, geo_x=140, geo_y=143)

    Place.objects.create(name="Место 6", short_description="Краткое описание для места 6", image=None,
                         description="Полное описание для места 6", rating=3.5, type=3, map_id=7,
                         redirect_url="redir_url_6", map_x=27, map_y=45, geo_x=145, geo_y=148)


class PlaceTestCase(TestCase):

    def setUp(self):
        create_places()

    def test_correct_added_places(self):
        places = Place.objects.all()
        self.assertEqual(len(places), 6)

    def test_check_user(self):
        self.assertEqual(self.client.get('/login/').status_code, 200)
        response = self.client.get('/profile/orders')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/profile/orders')

        User.objects.create_user(username='username', password='Pas$w0rd')
        self.assertTrue(self.client.login(username='username', password='Pas$w0rd'))

        self.assertEqual(self.client.get('/login/').status_code, 200)
        self.assertEqual(self.client.get('/profile/orders').status_code, 200)
