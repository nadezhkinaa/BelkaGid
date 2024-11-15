from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

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
    Route.objects.create(name="Маршрут 1", short_description="short_description", rating=5.0, votes=15, creator=1,
                         marshrut="1$2$3$4$5")
    Route.objects.create(name="Маршрут 2", short_description="short_description", rating=5.0, votes=15, creator=1,
                         marshrut="1$2$3$4$5")
    Route.objects.create(name="Маршрут 3", short_description="short_description", rating=5.0, votes=15, creator=1,
                         marshrut="1$2$3$4$5")
    Route.objects.create(name="Маршрут 4", short_description="short_description", rating=5.0, votes=15, creator=1,
                         marshrut="1$2$3$4$5")
    Route.objects.create(name="Маршрут 5", short_description="short_description", rating=5.0, votes=15, creator=1,
                         marshrut="1$2$3$4$5")
    Route.objects.create(name="Маршрут 6", short_description="short_description", rating=5.0, votes=15, creator=0,
                         marshrut="1$2$3$4$5")
    Route.objects.create(name="Маршрут 7", short_description="short_description", rating=5.0, votes=15, creator=0,
                         marshrut="1$2$3$4$5")
    Route.objects.create(name="Маршрут 8", short_description="short_description", rating=5.0, votes=15, creator=0,
                         marshrut="1$2$3$4$5")
    Route.objects.create(name="Маршрут 9", short_description="short_description", rating=5.0, votes=15, creator=0,
                         marshrut="1$2$3$4$5")


class ViewTest(TestCase):
    """
    Unit 1. Class for testing view urls and templates
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


class SignUpFormTest(TestCase):
    """
    Unit 2. Class for testing SignUpForm
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
    Unit 3. Class for testing AuthenticationForm
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
    Unit 4. Class for testing FeedbackForm
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


class TestExportYaMaps(StaticLiveServerTestCase):
    """
    Unit 5. Class for testing export to yandex maps
    """

    def setUp(self):
        User.objects.create_superuser(username='username', password='Pas$w0rd')

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

    def test_export_yandex_maps_from_lkab(self):
        self.login()
        initial_windows = self.browser.window_handles
        routes = self.browser.find_elements(By.CLASS_NAME, "export1")
        route_2 = routes[1]
        route_2.click()
        WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(len(initial_windows) + 1))
        all_windows = self.browser.window_handles
        new_window_handle = [window for window in all_windows if window not in initial_windows][0]
        self.browser.switch_to.window(new_window_handle)
        self.assertIn("yandex", self.browser.current_url)
        self.assertIn("Яндекс", self.browser.title)

    def test_export_yandex_maps_from_index(self):
        self.login()
        self.browser.get(self.live_server_url)
        routes = self.browser.find_elements(By.CLASS_NAME, "buttonexport")
        route_3 = routes[2]
        initial_windows = self.browser.window_handles
        self.browser.execute_script("arguments[0].scrollIntoView();", route_3)
        self.browser.execute_script("arguments[0].click();", route_3)
        WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(len(initial_windows) + 1))
        all_windows = self.browser.window_handles
        new_window_handle = [window for window in all_windows if window not in initial_windows][0]
        self.browser.switch_to.window(new_window_handle)
        self.assertIn("yandex", self.browser.current_url)
        self.assertIn("Яндекс", self.browser.title)

    def tearDown(self):
        self.client.login()
        self.browser.quit()


class TestCreateOrder(StaticLiveServerTestCase):
    """
    Unit 6. Class for testing order creation
    """

    def setUp(self):
        User.objects.create_superuser(username='username', password='Pas$w0rd')

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

    def test_create_order(self):
        self.login()
        self.browser.get(self.live_server_url + "/profile/orders")

        create_button = self.browser.find_element(By.CLASS_NAME, "buttoncreate")
        create_button.click()

        name_field = self.browser.find_element(By.ID, "name")
        persons_field = self.browser.find_element(By.ID, "persons-count")
        message_field = self.browser.find_element(By.ID, "messages")
        date_field = self.browser.find_element(By.CLASS_NAME, "datazayavka")

        place_add = Select(self.browser.find_element(By.ID, "place-add-select"))
        button_finish = self.browser.find_element(By.CLASS_NAME, "buttonsozdat")

        name_field.send_keys('New order for me')
        persons_field.send_keys('5')
        message_field.send_keys("Message for my order for me")
        date_field.send_keys("01.01.2032")
        place_add.select_by_visible_text('Маршрут 8')
        button_finish.click()

        self.browser.get(self.live_server_url + "/profile/orders")

        orders = self.browser.find_elements(By.CLASS_NAME, "zakaz")
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].text, "New order for me")

        orders[0].click()

        name_field_order = self.browser.find_element(By.ID, "name")
        persons_field_order = self.browser.find_element(By.ID, "persons-count")
        message_field_order = self.browser.find_element(By.ID, "messages")
        date_field_order = self.browser.find_element(By.CLASS_NAME, "datazayavkaorder")
        route_field_order = self.browser.find_element(By.ID, "name_route")

        self.assertEqual(name_field_order.get_attribute("value"), "New order for me")
        self.assertEqual(persons_field_order.get_attribute("value"), "5")
        self.assertEqual(message_field_order.get_attribute("value"), "Message for my order for me")
        self.assertEqual(date_field_order.get_attribute("value"), "2032-01-01")
        self.assertEqual(route_field_order.get_attribute("value"), "Маршрут 8")

    def tearDown(self):
        self.client.login()
        self.browser.quit()
