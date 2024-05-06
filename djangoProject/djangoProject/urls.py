"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import belka.views
from belka.views import index_page, message_sent, profile_routes_page, profile_orders_page, profile_redirect_page, \
    create_order_page
from belka.views import about_page
from belka.views import places_page
from belka.views import cafe_page
from belka.views import shop_page
from belka.views import profile_page
from belka.views import signup
from belka.views import login
from belka.views import log_out

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index_page),
    path('about/', about_page),
    path('places/', places_page),
    path('cafe/', cafe_page),
    path('shop/', shop_page),
    path('profile/', profile_redirect_page),
    path('profile/info', profile_page),
    path('profile/routes', profile_routes_page),
    path('profile/orders', profile_orders_page),
    path('profile/orders/create', create_order_page),
    path('login/', login),
    path('logout/', log_out),
    path('register/', signup),
    path('message_sent/', message_sent),

    path('add_fav/', belka.views.add_favourite, name='add_favourite'),

]
