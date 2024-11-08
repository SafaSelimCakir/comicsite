from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

def home(request):
    context={}
    return render(request, 'xsite/home.html',context)

def information(request):
    context={}
    return render(request, 'xsite/information.html',context)

def bag(request):
    context={}
    return render(request, 'xsite/bag.html',context)

def login(request):
    context={}
    return render(request, 'xsite/login.html',context)

def register(request):
    form=UserCreationForm()
    context={'form':form}
    return render(request, 'xsite/register.html',context)

def cart(request):
    context={}
    return render(request, 'xsite/cart.html',context)

def checkout(request):
    context={}
    return render(request, 'xsite/checkout.html',context)
    

