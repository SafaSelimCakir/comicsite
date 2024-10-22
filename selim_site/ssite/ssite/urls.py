"""
URL configuration for ssite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views  # Görünümlerinizi içe aktarın

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Ana sayfa için görünüm
<<<<<<< HEAD
    path('cart/', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
=======
    
>>>>>>> 72c9b07376b27ddc0dedc8b07ec028fc13f8d4e9
]