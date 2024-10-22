from django.urls import path
from . import views
#http://127.0.0.1:8000/user             =>homepage
#http://127.0.0.1:8000/user/index        =>homepage
#http://127.0.0.1:8000/user/blogs        =>blogs
#http://127.0.0.1:8000/user/blogs/3      =>blogs-details


urlpatterns = [
<<<<<<< HEAD
    path("",views.index,name="home"),
    
    path("cart",views.cart,name="cart"),
    path("checkout",views.checkout,name="checkout"),
=======
    path("",views.index),
    path("home",views.index),
    
>>>>>>> 72c9b07376b27ddc0dedc8b07ec028fc13f8d4e9
]