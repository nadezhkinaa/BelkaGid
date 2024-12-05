# locust -f '.\belka\tests\locust_testing.py'


from locust import HttpUser, task, between

TEST_LOGIN = ""
TEST_PASSWORD = ""
WAIT_FROM = 0.5
WAIT_TO = 2


class BelkaLoads(HttpUser):
    wait_time = between(WAIT_FROM, WAIT_TO)

    @task
    def index(self):
        self.client.get("")

    @task
    def about(self):
        self.client.get("/about")

    @task
    def admin(self):
        self.client.get("/admin")

    @task
    def places_page(self):
        self.client.get("/places")

    @task
    def cafe_page(self):
        self.client.get("/cafe")

    @task
    def shop_page(self):
        self.client.get("/shop")

    @task
    def profile_redirect_page(self):
        self.client.get("/profile")

    @task
    def profile_page(self):
        self.client.get("/profile/info")

    @task
    def profile_routes_page(self):
        self.client.get("/profile/routes")

    @task
    def profile_orders_page(self):
        self.client.get("/profile/orders")

    @task
    def create_order_page(self):
        self.client.get("/profile/orders/create")

    @task
    def login(self):
        self.client.get("/login")

    @task
    def log_out(self):
        self.client.get("/logout")

    @task
    def signup(self):
        self.client.get("/register")

    @task
    def message_sent(self):
        self.client.get("/message_sent")

    @task
    def events(self):
        self.client.get("/events")


class BelkaForms(HttpUser):
    wait_time = between(WAIT_FROM, WAIT_TO)

    @task
    def login(self):
        URL = "http://127.0.0.1:8000/login/"
        client = self.client
        client.get(URL)
        if 'csrftoken' in client.cookies:
            # Django 1.6 and up
            csrftoken = client.cookies['csrftoken']
        else:
            # older versions
            csrftoken = client.cookies['csrf']

        client.post(URL, data={'csrfmiddlewaretoken': csrftoken,
                               'username': TEST_LOGIN,
                               'password': TEST_PASSWORD})

    @task
    def send_message(self):
        URL = "http://127.0.0.1:8000/about/"
        client = self.client
        client.get(URL)
        if 'csrftoken' in client.cookies:
            # Django 1.6 and up
            csrftoken = client.cookies['csrftoken']
        else:
            # older versions
            csrftoken = client.cookies['csrf']

        client.post(URL, data={'csrfmiddlewaretoken': csrftoken,
                               'name': "testlogin",
                               'email': "testmail@mail.ru",
                               'message': "test message"})
