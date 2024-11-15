from django.contrib.auth.models import User
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from belka.forms import SignUpForm, CustomAuthenticationForm, FeedbackForm
from belka.models import Place, Route


# some_path_to/virtualenv/lib/python3.11/site-packages/django/test/runner.py (probably at line 1044)
# def run_tests(self, test_labels, some=None, **kwargs):
# add any parameter like some=None
# https://docs.djangoproject.com/en/dev/topics/testing/overview/
# https://habr.com/ru/articles/122156/
# https://yourtodo.ru/ru/posts/django-testirovanie/
# https://sky.pro/media/kak-provodit-testirovanie-s-ispolzovaniem-selenium/

def create_places():
    from django.db import models
    Place.objects.create(image=models.FilePathField(), name="Место 1", short_description="Краткое описание для места 1",
                         description="Полное описание для места 1", rating=4.99, type=1, map_id=1,
                         redirect_url="places", map_x=100, map_y=350, geo_x=56.006621, geo_y=37.204354)

    Place.objects.create(image=models.FilePathField(), name="Place2", short_description="Краткое описание для места 2",
                         description="Полное описание для места 2", rating=4.5, type=2, map_id=2,
                         redirect_url="places", map_x=120, map_y=-10, geo_x=55.981894, geo_y=37.213759)

    Place.objects.create(image=models.FilePathField(), name="Место 3", short_description="Краткое описание для места 3",
                         description="Полное описание для места 3", rating=3.8, type=3, map_id=3,
                         redirect_url="places", map_x=-400, map_y=-100, geo_x=55.97926, geo_y=37.151972)

    Place.objects.create(image=models.FilePathField(), name="Место 4", short_description="Краткое описание для места 4",
                         description="Полное описание для места 4", rating=4.2, type=1, map_id=4,
                         redirect_url="places", map_x=0, map_y=30, geo_x=55.983229, geo_y=37.208158)

    Place.objects.create(image=models.FilePathField(), name="Место 5", short_description="Краткое описание для места 5",
                         description="Полное описание для места 5", rating=4.9, type=2, map_id=5,
                         redirect_url="places", map_x=350, map_y=180, geo_x=55.995364, geo_y=37.243641)

    Place.objects.create(image=models.FilePathField(), name="Место 6", short_description="Краткое описание для места 6",
                         description="Полное описание для места 6", rating=3.5, type=3, map_id=6,
                         redirect_url="places", map_x=20, map_y=480, geo_x=56.014953, geo_y=37.208202)


def create_routes():
    Route.objects.create(name="Маршрут 1", short_description="short_description", rating=5.0, votes=15, creator=0,
                         marshrut="1$2$3$4$5")
    Route.objects.create(name="Маршрут 2", short_description="short_description", rating=5.0, votes=15, creator=0,
                         marshrut="1$2$3$4$5")
    Route.objects.create(name="Маршрут 3", short_description="short_description", rating=5.0, votes=15, creator=0,
                         marshrut="1$2$3$4$5")
    Route.objects.create(name="Маршрут 4", short_description="short_description", rating=5.0, votes=15, creator=0,
                         marshrut="1$2$3$4$5")


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

    def test_place_detail(self):
        response = self.client.get('/places/Place2')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, '/places/Place2/')


class SignUpFormTest(TestCase):
    """
    Class for testing SignUpForm
    """

    def test_form_valid_basic(self):
        form_data = {'username': 'username1', 'email': 'email@nodomain.com', 'password1': 'Lqt3z8L-',
                     'password2': 'Lqt3z8L-'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_long_password(self):
        form_data = {'username': 'username1', 'email': 'email@nodomain.com',
                     'password1': 'Lqt3z8L-Lqt3z8L-Lqt3z8L-', 'password2': 'Lqt3z8L-Lqt3z8L-Lqt3z8L-'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_short_password(self):
        form_data = {'username': 'username1', 'email': 'email@nodomain.com',
                     'password1': 'Lq', 'password2': 'Lq'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_simple_password(self):
        form_data = {'username': 'username1', 'email': 'email@nodomain.com',
                     'password1': '1234567890', 'password2': '1234567890'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_mismatch_password(self):
        form_data = {'username': 'username1', 'email': 'email@nodomain.com',
                     'password1': 'Lqt3z8L-', 'password2': 'Lqt3z8L+'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_email(self):
        form_data = {'username': 'username1', 'email': 'email',
                     'password1': 'Lqt3z8L-', 'password2': 'Lqt3z8L-'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'username': 'username1', 'email': 'emailnodomain.com',
                     'password1': 'Lqt3z8L-', 'password2': 'Lqt3z8L-'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'username': 'username1', 'email': 'email@nodomaincom',
                     'password1': 'Lqt3z8L-', 'password2': 'Lqt3z8L-'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'username': 'username1', 'email': 'email@',
                     'password1': 'Lqt3z8L-', 'password2': 'Lqt3z8L-'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_excisting_username(self):
        form_data = {'username': 'username1', 'email': 'email@nodomain.com',
                     'password1': 'Lqt3z8L-', 'password2': 'Lqt3z8L-'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

        form.save()

        form_data = {'username': 'username1', 'email': 'email@domain.com',
                     'password1': 'Lqt3z8L-', 'password2': 'Lqt3z8L-'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())


class AuthenticationFormTest(TestCase):
    """
    Class for testing AuthenticationForm
    """

    def setUp(self) -> None:
        User.objects.create_user(username='username', password='Pas$w0rd')

    def test_form_login_correct(self):
        form_data = {'username': 'username', 'password': 'Pas$w0rd'}
        form = CustomAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_login_incorrect_password(self):
        form_data = {'username': 'username', 'password': 'INCORRECT_PASSWORD'}
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_login_incorrect_username(self):
        form_data = {'username': 'UsErNaMe', 'password': 'Pas$w0rd'}
        form = CustomAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())


class FeedbackFormTest(TestCase):
    """
    Class for testing FeedbackForm
    """

    def test_form_correct(self):
        form_data = {'name': 'username', 'email': 'email@nodomain.com', 'message': 'message'}
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_login_incorrect_email(self):
        form_data = {'name': 'username', 'email': 'email', 'message': 'message'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'name': 'username', 'email': '@nodomain.com', 'message': 'message'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'name': 'username', 'email': 'emailnodomain.com', 'message': 'message'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'name': 'username', 'email': '', 'message': 'message'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {'name': 'username', 'email': 'email@', 'message': 'message'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_login_incorrect_name(self):
        form_data = {'name': '', 'email': 'email@', 'message': 'message'}
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())


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

    def test_view_register(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')


class TestSelenium(StaticLiveServerTestCase):
    """
    Class for testing frontend with Selenium
    """

    def setUp(self):
        User.objects.create_user(username='username', password='Pas$w0rd')

        self.browser = webdriver.Chrome()
        create_places()
        create_routes()

    def login(self):
        self.browser.get(self.live_server_url + "/login/")

        login_field = self.browser.find_element(By.NAME, "username")
        password_field = self.browser.find_element(By.NAME, "password")
        login_button = self.browser.find_element(By.CLASS_NAME, "buttonvhod")

        login_field.send_keys('username')
        password_field.send_keys('Pas$w0rd')
        login_button.click()

    def tearDown(self):
        self.browser.quit()

    def test_correct_title(self):
        self.browser.get(self.live_server_url)
        self.assertIn("БелкаГид", self.browser.title)

    def test_route_items(self):
        self.login()
        popular_1 = self.browser.find_element(By.ID, "popular1")
        popular_1.click()

        self.assertIn("БелкаГид", self.browser.title)
        self.assertEqual("Маршрут 2", self.browser.find_element(By.ID, 'rName').text)
