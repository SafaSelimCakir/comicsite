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
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from .views import register
from .views import profile_view, api_add_to_cart, remove_from_cart,categorized_products_view
from django.contrib.auth.views import LogoutView
from .views import cart_detail,update_cart_item,update_profile,ordercheckout,product_detail
from xsite.models import Rating


urlpatterns = [
    path("acconts/",include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('', include('xsite.urls')),
    path('cart/', views.cart, name='cart'),
    path('information/', views.information, name='information'),
    path('checkout/', views.checkout, name='checkout'), 
    path('ordercheckout/', views.ordercheckout, name='ordercheckout'),
    path('bag/', views.bag, name='bag'),
    path('book/', views.book_view, name='book_view'),
    path('login/', views.login, name='login'),
    path('register/', register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('profile/', profile_view, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('checkout/', views.categorized_products_view, name='checkout'), 
    path('profile/edit/', update_profile, name='edit_profile'),
    path('api/update_cart_item/<int:item_id>/', update_cart_item, name='update_cart_item'),
    path('api/add-to-cart/<int:product_id>/', views.api_add_to_cart, name='api_add_to_cart'),
    path('cartd/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
