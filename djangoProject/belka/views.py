from django.shortcuts import render


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


def profile_page(request):
    return render(request, 'lichnkabinet.html')
