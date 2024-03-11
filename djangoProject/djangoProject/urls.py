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
from belka.views import index_page
from belka.views import about_page
from belka.views import places_page
from belka.views import cafe_page
from belka.views import shop_page
from belka.views import profile_page
from belka.views import login_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index_page),
    path('about/', about_page),
    path('places/', places_page),
    path('cafe/', cafe_page),
    path('shop/', shop_page),
    path('profile/', profile_page),
    path('login/', login_page)

]
