from django.http.response import HttpResponse
from django.shortcuts import render
from .models import *


def home(request):
    products = Product.objects.all()
    context={'products':products}
    return render(request, 'xsite/home.html',context)

def cart(request):
    context={}
    return render(request, 'xsite/cart.html',context)

def checkout(request):
    context={}
    return render(request, 'xsite/checkout.html',context)

