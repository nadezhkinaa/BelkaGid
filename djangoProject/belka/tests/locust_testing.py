# locust -f '.\belka\tests\locust_testing.py'


from locust import HttpUser, task, between

TEST_LOGIN = ""
TEST_PASSWORD = ""


class BelkaUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("")

    @task
    def about(self):
        self.client.get("/about")

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
