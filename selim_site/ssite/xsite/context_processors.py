from django.shortcuts import render
from xsite.models import Product

def base_view(request):
    latest_products = Product.objects.order_by('-id')[:5]  
    return {'latest_products': latest_products}
