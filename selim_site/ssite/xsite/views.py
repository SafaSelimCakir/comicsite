from django.http.response import HttpResponse
from django.shortcuts import render

def home(request):
<<<<<<< HEAD
    context={}
    return render(request, 'xsite/home.html',context)

def cart(request):
    context={}
    return render(request, 'xsite/cart.html',context)

def checkout(request):
    context={}
    return render(request, 'xsite/checkout.html',context)
=======
    return render(request, 'home.html')
>>>>>>> 72c9b07376b27ddc0dedc8b07ec028fc13f8d4e9
