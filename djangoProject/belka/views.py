from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import SignUpForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView


# Create your views here.
def index_page(request):
    return render(request, 'web1.html')


def about_page(request):
    return render(request, 'information.html')


def places_page(request):
    return render(request, 'mesta.html')


def cafe_page(request):
    return render(request, 'cafe.html')


def shop_page(request):
    return render(request, 'magazin.html')


def login_page(request):
    return render(request, 'lkab.html')


@login_required
def profile_page(request):
    return render(request, 'lichnkabinet.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/profile/')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


def login(request):
    return MyLoginView.as_view(template_name='login.html')(request)


def log_out(request):
    logout(request)
    return redirect("/")


class MyLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
