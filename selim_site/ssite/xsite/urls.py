from django.urls import path
from . import views
from xsite import views
from django.conf.urls.static import static
from django.conf import settings
from .views import CartView, HomeView, CheckoutView,informationView,bagView,loginView,BookDetailView,ProductDetailView,GetQuerySetView
from .views import RegisterView, CustomLoginView
from django.views.generic.base import RedirectView


urlpatterns = [
    path('information/', informationView.as_view(), name='information'),
    path('cart/', CartView.as_view(), name='cart'),
    path('home/', RedirectView.as_view(url='/', permanent=False)),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('bag/', bagView.as_view(), name='bag'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_view'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('checkout/get_queryset/', GetQuerySetView.as_view(), name='get_queryset'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    