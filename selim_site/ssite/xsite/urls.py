from django.urls import path
from . import views
from xsite import views

#http://127.0.0.1:8000/user             =>homepage
#http://127.0.0.1:8000/user/index        =>homepage
#http://127.0.0.1:8000/user/blogs        =>blogs
#http://127.0.0.1:8000/user/blogs/3      =>blogs-details


urlpatterns = [

    path("home",views.home,name="home"),
    
    path("cart",views.cart,name="cart"),
    path("checkout",views.checkout,name="checkout"),
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),

]