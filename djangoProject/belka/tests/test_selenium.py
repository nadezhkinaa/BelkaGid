from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from belka.models import Place, Route, Event


# python manage.py test belka.tests.test_selenium

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

    Place.objects.create(image=models.FilePathField(), name="Место 0", short_description="Краткое описание для места 0",
                         description="Полное описание для места 0", rating=3.5, type=3, map_id=0,
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


def login(browser, live_server_url, username, password):
    browser.get(live_server_url + "/login/")

    login_field = browser.find_element(By.NAME, "username")
    password_field = browser.find_element(By.NAME, "password")
    login_button = browser.find_element(By.CLASS_NAME, "buttonvhod")

    login_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()


class TestExportYaMaps(StaticLiveServerTestCase):
    """
    Class for testing export to yandex maps
    """

    def setUp(self):
        User.objects.create_superuser(username='username', password='Pas$w0rd')

        self.browser = webdriver.Chrome()
        create_places()
        create_routes()

    def test_export_yandex_maps_from_lkab(self):
        login(self.browser, self.live_server_url, 'username', 'Pas$w0rd')
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
        login(self.browser, self.live_server_url, 'username', 'Pas$w0rd')
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
        self.browser.quit()


class TestCreateOrder(StaticLiveServerTestCase):
    """
    Class for testing order creation
    """

    def setUp(self):
        User.objects.create_superuser(username='username', password='Pas$w0rd')

        self.browser = webdriver.Chrome()
        create_places()
        create_routes()

    def test_create_order(self):
        login(self.browser, self.live_server_url, 'username', 'Pas$w0rd')
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
        self.browser.quit()


class TestLogin(StaticLiveServerTestCase):
    """
    Class for testing login
    """

    def setUp(self) -> None:
        User.objects.create_superuser(username='username', password='Pas$w0rd')
        self.browser = webdriver.Chrome()

    def test_correct_login(self):
        login(self.browser, self.live_server_url, 'username', 'Pas$w0rd')
        self.assertEqual(self.browser.current_url, self.live_server_url + "/profile/routes")

    def test_wrong_login(self):
        login(self.browser, self.live_server_url, 'username', 'WRONG_PASSWORD')
        self.assertEqual(self.browser.current_url, self.live_server_url + "/login/")

    def tearDown(self) -> None:
        self.browser.quit()


class TestFilters(StaticLiveServerTestCase):
    """
    Class for testing filters
    """

    def setUp(self) -> None:
        self.browser = webdriver.Chrome()
        create_places()

    def test_places_filter_parks(self):
        self.browser.get(self.live_server_url + "/places/")
        filter_object = Select(self.browser.find_element(By.CLASS_NAME, "boxfiltr"))
        filter_object.select_by_visible_text("Парки")
        cards = self.browser.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len([card for card in cards if "display: block;" in card.get_attribute("style")]), 2)

    def test_places_filter_museums(self):
        self.browser.get(self.live_server_url + "/places/")
        filter_object = Select(self.browser.find_element(By.CLASS_NAME, "boxfiltr"))
        filter_object.select_by_visible_text("Музеи")
        cards = self.browser.find_elements(By.CLASS_NAME, "card")
        self.assertEqual(len([card for card in cards if "display: block;" in card.get_attribute("style")]), 2)

    def tearDown(self) -> None:
        self.browser.quit()


class TestRedirectEvents(StaticLiveServerTestCase):
    """
    Class for testing redirecting events on provider website
    """

    def setUp(self) -> None:
        self.browser = webdriver.Chrome()
        Event.objects.create(name="Event 1", cost=300, image="/", place="Event Hall", time="19:00",
                             date="2024-03-08 19:00:00", link="https://www.wikipedia.org/", type=0)

    def test_event(self):
        self.browser.get(self.live_server_url + "/events/")
        button_link = self.browser.find_element(By.CLASS_NAME, "buttonsob")
        button_link.click()
        WebDriverWait(self.browser, 10).until(
            EC.title_is("Wikipedia"))
        self.assertEqual(self.browser.current_url, "https://www.wikipedia.org/?")

    def tearDown(self) -> None:
        self.browser.quit()
