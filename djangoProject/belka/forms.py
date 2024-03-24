from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Удаляем тексты проверок пароля
        self.fields['username'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.fields['username'].label = "Логин"
        self.fields['password1'].label = "Придумайте пароль"
        self.fields['password2'].label = "Повторите пароль"

        # Удаляем проверки пароля или добавляем собственные
        del self.fields['password1'].validators[:]
        del self.fields['password2'].validators[:]

    email = forms.EmailField(max_length=254, help_text='', label="Электронный адрес")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=None, *args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)



