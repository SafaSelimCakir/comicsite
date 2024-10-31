from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Product

def cart(request):
    products = Product.objects.all()  # Tüm ürünleri al
    context = {'products': products}
    return render(request, 'xsite/cart.html', context)

def home(request):
    context = {}
    return render(request, 'xsite/home.html', context)

def checkout(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'xsite/checkout.html', context)
