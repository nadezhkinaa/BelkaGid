from django.contrib import admin

# Register your models here.
from belka.models import Place, Cafe, Shop, UserFavourites

admin.site.register(Place)
admin.site.register(Cafe)
admin.site.register(Shop)
admin.site.register(UserFavourites)
