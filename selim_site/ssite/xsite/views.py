from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from .models import Product
def product_list(request):
    products = Product.objects.all()
    return render(request, 'xsite/index.html', {'products': products})
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'xsite/index2.html', {'product': product})
from django.http import HttpResponse
def home(request):
    return HttpResponse('Hello, World!')



def home(request):

    context={}
    return render(request, 'xsite/home.html',context)

def cart(request):
    context={}
    return render(request, 'xsite/cart.html',context)

def checkout(request):
    context={}
    return render(request, 'xsite/checkout.html',context)

