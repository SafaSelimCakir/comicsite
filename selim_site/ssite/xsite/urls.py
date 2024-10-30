from django.urls import path
from . import views
from xsite import views
from django.conf.urls.static import static
from django.conf import settings
#http://127.0.0.1:8000/user             =>homepage
#http://127.0.0.1:8000/user/index        =>homepage
#http://127.0.0.1:8000/user/blogs        =>blogs
#http://127.0.0.1:8000/user/blogs/3      =>blogs-details


urlpatterns = [

    path("home",views.home,name="home"),
    
    path("cart",views.cart,name="cart"),
    path("checkout",views.checkout,name="checkout"),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)