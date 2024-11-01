from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from .models import ImageCard


def image_card_list(request):
    cards = ImageCard.objects.all()
    return render(request, 'xsite/checkout.html', {'cards': cards})




def cart(request):
    products = Product.objects.all()  # Tüm ürünleri al
    context = {'products': products}
    return render(request, 'xsite/cart.html', context)

def home(request):
    context = {}
    return render(request, 'xsite/home.html', context)

def checkout(request):
    products = Product.objects.all()  # Tüm ürünleri al
    context = {'products': products}
    return render(request, 'xsite/checkout.html', context)
