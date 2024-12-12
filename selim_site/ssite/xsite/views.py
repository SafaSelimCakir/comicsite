from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product
from django.views.generic import ListView
from django.views.generic import TemplateView,DetailView
from ssite.forms import RegisterForm
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'xsite/login.html'

class BookDetailView(DetailView):
    model = Product  # Hangi modelin detayını göstereceğimizi belirtiyoruz
    template_name = 'xsite/book.html'  # Kullanılacak şablon dosyasının adı
    context_object_name = 'product'  # Şablonda kullanılacak nesne adı (varsayılan 'object' yerine 'product' olarak kullanacağız)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        context['images'] = product.images.all()  # Ürün resimlerini de ekliyoruz
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'xsite/product_detail.html'  # Oluşturacağınız HTML şablon
    context_object_name = 'product'

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

class RegisterView(FormView):
    template_name = 'xsite/register.html'
    form_class = RegisterForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()  # Kullanıcıyı kaydet
        return super().form_valid(form)

class informationView(ListView):
    model = Product
    template_name = 'xsite/information.html'
    context_object_name = 'products' 

class bagView(ListView):
    model = Product
    template_name = 'xsite/bag.html'
    context_object_name = 'products' 