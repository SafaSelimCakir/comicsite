from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Kullanıcıyı otomatik olarak giriş yap
            return redirect('home')  # Giriş sonrası yönlendirme
    else:
        form = RegisterForm()
    return render(request, 'xsite/register.html', {'form': form})

def home(request):
    context={}
    return render(request, 'xsite/home.html',context)

def information(request):
    context={}
    return render(request, 'xsite/information.html',context)

def bag(request):
    context={}
    return render(request, 'xsite/bag.html',context)

def book(request):
    context={}
    return render(request, 'xsite/book.html',context)

def login(request):
    return render(request,"xsite/login.html")
  
  
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
    

