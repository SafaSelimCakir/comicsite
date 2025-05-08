from django.shortcuts import render
from xsite.models import Product
from django.conf import settings

def base_view(request):
    latest_products = Product.objects.order_by('-id')[:5]  
    return {'latest_products': latest_products}

def stripe_keys(request):
    return {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }