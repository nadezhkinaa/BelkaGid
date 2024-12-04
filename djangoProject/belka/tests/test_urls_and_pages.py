from django.contrib.auth.models import User
from django.test import TestCase


# for all
# python manage.py test belka

# python manage.py test belka.tests.test_urls_and_pages

# some_path_to/virtualenv/lib/python3.11/site-packages/django/test/runner.py (probably at line 1044)
# def run_tests(self, test_labels, some=None, **kwargs):
# add any parameter like some=None

# https://docs.djangoproject.com/en/dev/topics/testing/overview/
# https://habr.com/ru/articles/122156/
# https://yourtodo.ru/ru/posts/django-testirovanie/
# https://sky.pro/media/kak-provodit-testirovanie-s-ispolzovaniem-selenium/


class ViewTest(TestCase):
    """
    Class for testing view urls and templates
    """

    def setUp(self) -> None:
        User.objects.create_user(username='username', password='Pas$w0rd')

    def login(self):
        self.client.login(username='username', password='Pas$w0rd')

    def logout(self):
        self.client.logout()

    def test_view_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

    def test_view_login(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vhod.html')

    def test_view_about(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'onas.html')

    def test_view_places(self):
        response = self.client.get("/places/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mesta.html')

    def test_view_cafe(self):
        response = self.client.get("/cafe/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafe.html')

    def test_view_profile(self):
        self.login()
        response = self.client.get("/profile/info")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lkab.html')
        self.logout()

    def test_view_orders(self):
        self.login()
        response = self.client.get("/profile/orders")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'zakazi.html')
        self.logout()

    def test_view_routes(self):
        self.login()
        response = self.client.get("/profile/routes")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'marsruty.html')
        self.logout()

    def test_view_register(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
