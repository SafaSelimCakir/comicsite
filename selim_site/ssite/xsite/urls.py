from django.urls import path
from . import views
from xsite import views
from django.conf.urls.static import static
from django.conf import settings
from .views import image_card_list


urlpatterns = [
    path("home",views.home,name="home"),
    path("cart",views.cart,name="cart"),
    path("checkout",views.checkout,name="checkout"),
    path('', image_card_list, name='image_card_list'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)