from django.contrib.auth.models import User
from django.test import TestCase

from belka.forms import SignUpForm, CustomAuthenticationForm, FeedbackForm


# python manage.py test belka.tests.test_forms

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
    """TestCase
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
