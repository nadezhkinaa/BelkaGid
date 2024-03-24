import time

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import SignUpForm, CustomAuthenticationForm, FeedbackForm
from django.contrib.auth.views import LoginView
import telegram
import asyncio

bot_token = ''
chat_id = ''


async def sendToBot(message, bot_id, chat_id):
    bot = telegram.Bot(token=bot_id)
    chat_id = chat_id
    try:
        await bot.sendMessage(chat_id=chat_id, text=message)
        time.sleep(5)
    except Exception as Err:
        print("Error, bot_id : " + bot_id + " channel_id : " + chat_id)
        print(Err)


# Create your views here.
def index_page(request):
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

    else:
        form = FeedbackForm()

    return render(request, 'web1.html', {'form': form})


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
