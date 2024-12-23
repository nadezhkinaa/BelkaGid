import asyncio
import datetime

import telegram
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.sites import requests
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import SignUpForm, CustomAuthenticationForm, FeedbackForm
from .models import Shop, Place, Cafe, UserFavourites, Route, Event, Order

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
    routes = Route.objects.filter(creator=0)
    routes_for_order = Route.objects.filter(creator=request.user.id)

    for place in places:
        place.image = place.image.replace("static/", "")

    for cafe in cafes:
        cafe.image = cafe.image.replace("static/", "")

    for shop in shops:
        shop.image = shop.image.replace("static/", "")

    places = serializers.serialize("json", Place.objects.all())
    cafes = serializers.serialize("json", Cafe.objects.all())
    shops = serializers.serialize("json", Shop.objects.all())
    routes = serializers.serialize("json", routes)

    context = {
        'places': places,
        'cafes': cafes,
        'shops': shops,
        'routes': routes,
        'routes_for_order': routes_for_order

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
    if request.user.first_name != "":
        context = {
            'name': request.user.first_name,
            'surname': request.user.last_name,
            'email': User.objects.filter(id=request.user.id).values_list('email', flat=True)[0],
            'username': request.user.username,
        }
    else:
        context = {
            'name': "",
            'surname': "",
            'email': User.objects.filter(id=request.user.id).values_list('email', flat=True)[0],
            'username': request.user.username,
        }
    return render(request, 'lkab.html', context)


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
    favs = UserFavourites.objects.get_or_create(user_id=request.user.id)
    routes = serializers.serialize("json", Route.objects.all().order_by('rating').reverse())

    places = Place.objects.all()
    for place in places:
        place.image = place.image.replace("static/", "")

    places = serializers.serialize("json", Place.objects.all())

    context = {
        'routes': routes,
        'places': places,
        'personalRoutes': Route.objects.filter(creator=request.user.id)
    }
    return render(request, 'marsruty.html', context)


@login_required
def profile_orders_page(request):
    if request.user.groups.filter(name='Gids').exists():
        orders = Order.objects.filter(gid=-1)
        orders_personal = Order.objects.filter(gid=request.user.id)

        context = {
            'orders': orders,
            'orders_personal': orders_personal,
        }
        return render(request, "zakazi_gid.html", context)
    else:
        orders = Order.objects.filter(ordered_user=request.user.id)
        context = {
            'orders': orders,
        }
        return render(request, "zakazi.html", context)


@login_required
def profile_redirect_page(request):
    return redirect('/profile/routes')


@login_required
def create_order_page(request):
    routes = Route.objects.filter(creator=0)
    routes_for_order = Route.objects.filter(creator=request.user.id)
    context = {
        'routes': routes,
        'routes_for_order': routes_for_order
    }

    return render(request, "zayvka.html", context)


@csrf_exempt
@login_required
def add_favourite(request):
    if request.method == "POST":
        argument = request.POST.get('place-id')  # Получение аргумента из запроса
        favourite, created = UserFavourites.objects.get_or_create(user_id=request.user.id)
        favourite.addId(argument)
        return JsonResponse({'success': True})  # Возврат ответа в виде JSON
    else:
        return JsonResponse({'success': False})


@csrf_exempt
@login_required
def saveRoute(request):
    if request.method == "POST":
        Route.objects.create(
            name=request.POST.get("name"),
            short_description=request.POST.get("short_description"),
            rating=0.0,
            votes=0,
            creator=request.user.id,
            marshrut=request.POST.get('route'),  # Получение аргумента из запроса
        )

        return JsonResponse({'success': True})  # Возврат ответа в виде JSON
    else:
        return JsonResponse({'success': False})


@csrf_exempt
@login_required
def check_favourite(request):
    if request.method == "POST":
        argument = request.POST.get('place-id')  # Получение аргумента из запроса
        favourite = UserFavourites.objects.get(user_id=request.user.id)
        if argument not in favourite.getFavouritePlaces():
            return JsonResponse({'success': True, "color": "#333D29"})  # Возврат ответа в виде JSON
        else:
            return JsonResponse({'success': True, "color": "#ff033e"})  # Возврат ответа в виде JSON

    else:
        return JsonResponse({'success': False})


def place_detail(request, place_name):
    place = Place.objects.get(name=place_name)
    place.image = place.image.replace("static/", "")
    context = {'place': place}
    return render(request, 'place_detail.html', context)


def route_detail(request, route_id):
    places = Place.objects.all()
    userfavs = UserFavourites.objects.get(user_id=request.user.id)
    userfavs = userfavs.favourite_places.split("$")

    for place in places:
        place.image = place.image.replace("static/", "")

    routeq = Route.objects.get(id=route_id)
    routeq.marshrut = routeq.marshrut.split("$")
    arr_stops = []
    for i in range(len(routeq.marshrut) - 1):
        arr_stops.append(places[int(routeq.marshrut[i])].name)

    places_favs = []
    for i in range(len(userfavs) - 1):
        places_favs.append(places[int(userfavs[i])])

    places_list = list(places)
    places_not_favs = []
    for place in places_list:
        flag = True
        for fav_place in places_favs:
            if place.name == fav_place.name:
                flag = False
                break
        if flag:
            places_not_favs.append(place)

    context = {'route': routeq, 'stops': arr_stops, "places": serializers.serialize("json", Place.objects.all()),
               'placesFav': places_favs, "placesNonFav": places_not_favs}
    return render(request, 'marsr.html', context)


def event_page(request):
    items = Event.objects.all()
    for item in items:
        item.image = item.image.replace("static/", "")
    context = {
        'items': items,
    }
    return render(request, "sobitia.html", context)


def parseDate(date_from_form):
    dates = str(date_from_form).split("-")
    return datetime.date(int(dates[0]), int(dates[1]), int(dates[2]))


@csrf_exempt
@login_required
def saveOrder(request):
    if request.method == "POST":
        Order.objects.create(
            route=Route.objects.get(id=request.POST.get("route")),
            persons=request.POST.get("persons"),
            date=parseDate(request.POST.get('date')),  # Получение аргумента из запроса
            ordered_user=request.user.id,
            name=request.POST.get("name"),
            comments=request.POST.get("comments")
        )

        return JsonResponse({'success': True})  # Возврат ответа в виде JSON
    else:
        return JsonResponse({'success': False})


@csrf_exempt
@login_required
def deleteOrder(request):
    if request.method == "POST":
        id = request.POST.get("id")
        Order.objects.get(id=id).delete()

        return JsonResponse({'success': True})  # Возврат ответа в виде JSON
    else:
        return JsonResponse({'success': False})


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    places = Place.objects.all()

    if order.ordered_user != request.user.id and (not request.user.groups.filter(name='Gids').exists()):
        raise PermissionDenied()

    for place in places:
        place.image = place.image.replace("static/", "")
    places = serializers.serialize("json", Place.objects.all())

    routes = serializers.serialize("json", Route.objects.all())

    email = User.objects.filter(id=order.ordered_user).values_list('email', flat=True)

    if order.gid == -1:
        context = {'places': places,
                   'order': order,
                   'routes': routes,
                   'email': email[0],
                   'gid_name': "",
                   'gid_email': "",
                   'isgid': int(request.user.groups.filter(name='Gids').exists()),
                   }
    else:
        context = {'places': places,
                   'order': order,
                   'routes': routes,
                   'email': email[0],
                   'gid_name': User.objects.get(id=order.gid).first_name + " " + User.objects.get(
                       id=order.gid).last_name,
                   'gid_email': User.objects.filter(id=order.gid).values_list('email', flat=True)[0],
                   'isgid': int(request.user.groups.filter(name='Gids').exists()),
                   }

    return render(request, 'order_detail.html', context)


@login_required
@csrf_exempt
def takeOrder(request):
    if request.method == "POST":
        id = request.POST.get("id")
        q = Order.objects.get(id=id)
        q.gid = request.user.id
        q.save()

        return JsonResponse({'success': True})  # Возврат ответа в виде JSON
    else:
        return JsonResponse({'success': False})


@login_required
@csrf_exempt
def finishOrder(request):
    if request.method == "POST":
        request.session['route_finish'] = request.POST.get("route")
        request.session['date_finish'] = request.POST.get("date")
        request.session['persons_finish'] = request.POST.get("persons")

        return JsonResponse({'success': True})  # Возврат ответа в виде JSON
    else:
        return JsonResponse({'success': False})


@login_required
@csrf_exempt
def deleteSessionData(request):
    if request.method == "POST":
        request.session['route_finish'] = ""
        request.session['date_finish'] = ""
        request.session['persons_finish'] = ""
        return JsonResponse({'success': True})  # Возврат ответа в виде JSON
    else:
        return JsonResponse({'success': False})


@csrf_exempt
@login_required
def saveDataEdits(request):
    if request.method == "POST":
        u = User.objects.get(id=request.user.id)
        u.first_name = request.POST.get("name")
        u.last_name = request.POST.get("surname")
        u.username = request.POST.get("username")
        u.email = request.POST.get("email")
        if (request.POST.get("password")) != "":
            u.set_password(request.POST.get("password"))
        u.save()
        return JsonResponse({'success': True})  # Возврат ответа в виде JSON
    else:
        return JsonResponse({'success': False})


@login_required
@csrf_exempt
def editOrder(request):
    if request.method == "POST":
        order = Order.objects.get(id=request.POST.get("order"))
        order.name = request.POST.get("name")
        order.persons = request.POST.get("persons")
        order.comments = request.POST.get("comments")
        order.date = request.POST.get("date")
        order.save()
        return JsonResponse({'success': True})  # Возврат ответа в виде JSON
    else:
        return JsonResponse({'success': False})
