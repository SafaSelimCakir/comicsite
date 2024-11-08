from django.urls import path
from . import views
from xsite import views
from django.conf.urls.static import static
from django.conf import settings
from .views import CartView, HomeView, CheckoutView,informationView,bagView,loginView,registerView


urlpatterns = [
    path('information/', informationView.as_view(), name='information'),
    path('cart/', CartView.as_view(), name='cart'),
    path('home/', HomeView.as_view(), name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('bag/', bagView.as_view(), name='bag'),
    path('login/', loginView.as_view(), name='login'),
    path('register/', registerView.as_view(), name='register'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)