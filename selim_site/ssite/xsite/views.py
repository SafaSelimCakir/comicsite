from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from django.views.generic import ListView
from django.views.generic import TemplateView


class CartView(ListView):
    model = Product
    template_name = 'xsite/cart.html' 
    context_object_name = 'products' 

class HomeView(ListView):
    model = Product
    template_name = 'xsite/home.html'
    context_object_name = 'products'

class CheckoutView(ListView):
    model = Product
    template_name = 'xsite/checkout.html'
    context_object_name = 'products'

class loginView(ListView):
    model = Product
    template_name = 'xsite/login.html'
    context_object_name = 'products'
    
class bookView(ListView):
    model = Product
    template_name = 'xsite/book.html'
    context_object_name = 'products'

class registerView(ListView):
    model = Product
    template_name = 'xsite/register.html'
    context_object_name = 'products'

class informationView(ListView):
    model = Product
    template_name = 'xsite/information.html'
    context_object_name = 'products' 

class bagView(ListView):
    model = Product
    template_name = 'xsite/bag.html'
    context_object_name = 'products' 