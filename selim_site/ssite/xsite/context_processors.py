from django.shortcuts import render
from xsite.models import Product
from django.conf import settings

def user_owned_products(request):
    if request.user.is_authenticated:
        owned_products = Product.objects.filter(orderitem__order__user=request.user).distinct()
        return {'owned_products': owned_products}
    return {'owned_products': []}


def base_view(request):
    latest_products = Product.objects.order_by('-id')[:5]  
    return {'latest_products': latest_products}

def stripe_keys(request):
    return {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }