from django.http.response import HttpResponse
from django.shortcuts import render

def home(request):
    context={}
    return render(request, 'xsite/home.html',context)

def cart(request):
    context={}
    return render(request, 'xsite/cart.html',context)

def checkout(request):
    context={}
    return render(request, 'xsite/checkout.html',context)
    

