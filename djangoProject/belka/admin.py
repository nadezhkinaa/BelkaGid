from django.contrib import admin

# Register your models here.
from belka.models import Place, Cafe, Shop

admin.site.register(Place)
admin.site.register(Cafe)
admin.site.register(Shop)
