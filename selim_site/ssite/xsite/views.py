from django.http import HttpResponse
from django.shortcuts import render
from .models import Product
from django.views.generic import ListView
from django.views.generic import TemplateView

class CartView(ListView):
    model = Product
    template_name = 'xsite/cart.html' 
    context_object_name = 'products' 

class HomeView(TemplateView):
    template_name = 'xsite/home.html'

class CheckoutView(ListView):
    model = Product
    template_name = 'xsite/checkout.html'
    context_object_name = 'products'