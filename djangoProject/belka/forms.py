from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email

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
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['username'].widget.attrs.update({'class': 'text-field__input', 'placeholder': 'Логин'})
        self.fields['password'].widget.attrs.update({'class': 'text-field__input', 'placeholder': 'Пароль'})


class FeedbackForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "inputname"}), max_length=100)
    email = forms.EmailField(widget=forms.TextInput(attrs={"class": "inputemail"}))
    message = forms.CharField(widget=forms.Textarea(attrs={"class": "inputmessage"}))

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['email'].label = ""
        self.fields['message'].label = ""

        self.fields['name'].widget.attrs['placeholder'] = " Имя"
        self.fields['email'].widget.attrs['placeholder'] = " Электронная почта"
        self.fields['message'].widget.attrs['placeholder'] = " Сообщение"
