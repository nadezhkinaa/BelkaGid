import asyncio

import telegram
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.shortcuts import render, redirect

from .forms import SignUpForm, CustomAuthenticationForm, FeedbackForm
from .models import Shop, Place, Cafe, UserFavourites

bot_token = ''
chat_id = ''


async def sendToBot(message, bot_id, chat_id):
    bot = telegram.Bot(token=bot_id)
    chat_id = chat_id
    try:
        await bot.sendMessage(chat_id=chat_id, text=message)
    except Exception as Err:
        print("Error, bot_id : " + bot_id + " channel_id : " + chat_id)
        print(Err)


# Create your views here.
def index_page(request):
    places = Place.objects.all()
    cafes = Cafe.objects.all()
    shops = Shop.objects.all()

    for place in places:
        place.image = place.image.replace("static/", "")

    for cafe in cafes:
        cafe.image = cafe.image.replace("static/", "")

    for shop in shops:
        shop.image = shop.image.replace("static/", "")

    places = serializers.serialize("json", Place.objects.all())
    cafes = serializers.serialize("json", Cafe.objects.all())
    shops = serializers.serialize("json", Shop.objects.all())

    context = {
        'places': places,
        'cafes': cafes,
        'shops': shops,
    }
    return render(request, 'main.html', context)


def about_page(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Обработка данных формы
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            formmessage = form.cleaned_data['message']

            # Дополнительная логика сохранения данных или отправки уведомлений
            # Текст сообщения для отправки
            message = "Новое сообщение!\n\nОтправитель: " + name + "\nПочта: " + email + "\n\nТекст сообщения:\n" + formmessage
            asyncio.run(sendToBot(message, bot_token, chat_id))
            form = FeedbackForm()
            return redirect('/message_sent/')
    else:
        form = FeedbackForm()

    return render(request, 'onas.html', {'form': form})


def places_page(request):
    items = Place.objects.all()
    for item in items:
        item.image = item.image.replace("static/", "")
    context = {
        'items': items,
    }
    return render(request, 'mesta.html', context)


def cafe_page(request):
    items = Cafe.objects.all()
    for item in items:
        item.image = item.image.replace("static/", "")
    context = {
        'items': items,
    }
    return render(request, 'cafe.html', context)


def shop_page(request):
    items = Shop.objects.all()
    for item in items:
        item.image = item.image.replace("static/", "")
    context = {
        'items': items,
    }
    return render(request, 'magazin.html', context)


@login_required
def profile_page(request):
    return render(request, 'lkab.html')


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
    return MyLoginView.as_view(template_name='vhod.html')(request)


def log_out(request):
    logout(request)
    return redirect("/")


class MyLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


def message_sent(request):
    return render(request, 'message_sent.html')


@login_required
def profile_routes_page(request):
    return render(request, "marsruty.html")


@login_required
def profile_orders_page(request):
    return render(request, "zakazi.html")


@login_required
def profile_redirect_page(request):
    user = request.user
    if not UserFavourites.objects.filter(user_id=user.id).exists():
        UserFavourites.objects.create(user_id=user.id, favourite_places="")
    return redirect('/profile/routes')


@login_required
def create_order_page(request):
    return render(request, "zayvka.html")
