from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product
from django.views.generic import ListView
from django.views.generic import TemplateView,DetailView
from ssite.forms import RegisterForm
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem, Product
from django.db import transaction
import stripe
import logging
from django.conf import settings
from decimal import Decimal

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

class CustomLoginView(LoginView):
    template_name = 'xsite/login.html'

class BookDetailView(DetailView):
    model = Product  
    template_name = 'xsite/book.html'  
    context_object_name = 'product' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        context['images'] = product.images.all()  
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'xsite/product_detail.html'  
    context_object_name = 'product'

class CartView(ListView):
    model = Product
    template_name = 'xsite/cart.html' 
    context_object_name = 'products' 

class HomeView(ListView):
    model = Product 
    template_name = 'xsite/home.html'
    context_object_name = 'products'


class GetQuerySetView(View):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query)  
            )
        else:
            products = Product.objects.all()  
        return render(request, 'xsite/checkout.html', {'products': products})


class CheckoutView(ListView):
    model = Product
    template_name = 'xsite/checkout.html'
    context_object_name = 'products'

    def get(self, request):
        query = request.GET.get('q')
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query)  
            )
        else:
            products = Product.objects.all()  
        return render(request, 'xsite/checkout.html', {'products': products})
    

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

class bagView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'xsite/bag.html'
    context_object_name = 'products'

    def get_queryset(self):
        user_orders = Order.objects.filter(user=self.request.user)
        products = Product.objects.filter(orderitem__order__in=user_orders).distinct()
        logger.info(f"User {self.request.user.username} library query returned {products.count()} products")
        return products
    

class OrderCheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()

            if not cart_items:
                messages.error(request, "Sepetiniz boş.")
                logger.warning(f"User {request.user.username} attempted checkout with empty cart.")
                return redirect('cart')

            # Toplam fiyatı hesapla
            total_price = sum(
                Decimal(str(item.product.discounted_price if item.product.apply_discount else item.product.price.amount))
                for item in cart_items
            )
            logger.info(f"Total price calculated: {total_price} for user {request.user.username}")

            payment_method_id = request.POST.get('payment_method_id')
            if not payment_method_id:
                messages.error(request, "Ödeme yöntemi sağlanmadı.")
                logger.error(f"No payment method provided for user {request.user.username}")
                return redirect('cart')

            # Stripe PaymentIntent oluştur
            payment_intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),  # Cent cinsinden
                currency='try',
                payment_method=payment_method_id,
                confirm=True,
                automatic_payment_methods={
                    'enabled': True,
                    'allow_redirects': 'never',
                },
            )
            logger.info(f"PaymentIntent created: {payment_intent.id} for user {request.user.username}")

            # Ödeme başarılıysa veritabanı işlemlerini gerçekleştir
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    total_price=total_price,
                )
                logger.info(f"Order created: {order.id} for user {request.user.username}")

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=Decimal(str(item.product.discounted_price if item.product.apply_discount else item.product.price.amount))
                    )
                    logger.info(f"OrderItem created for product {item.product.name} in order {order.id}")

                # Sepeti temizle
                cart_items.delete()
                logger.info(f"Cart cleared for user {request.user.username}")

            messages.success(request, "Ödeme başarılı! Ürünler kütüphanenize eklendi.")
            return redirect('bag')

        except stripe.error.StripeError as e:
            messages.error(request, f"Ödeme hatası: {str(e)}")
            logger.error(f"Stripe error for user {request.user.username}: {str(e)}")
            return redirect('cart')
        except Exception as e:
            messages.error(request, f"Bir hata oluştu: {str(e)}")
            logger.error(f"General error for user {request.user.username}: {str(e)}")
            return redirect('cart')
        

class PaymentReturnView(View):
    def get(self, request):
        payment_intent_id = request.GET.get('payment_intent')
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if payment_intent.status == 'succeeded':
                # Ödeme başarılı, siparişi tamamla
                cart = Cart.objects.get(user=request.user)
                total_price = sum(
                    item.product.discounted_price if item.product.apply_discount else item.product.price.amount
                    for item in cart.items.all()
                )

                with transaction.atomic():
                    order = Order.objects.create(
                        user=request.user,
                        total_price=total_price,
                    )
                    for item in cart.items.all():
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            quantity=item.quantity,
                            price=item.product.discounted_price if item.product.apply_discount else item.product.price.amount
                        )
                    cart.items.all().delete()

                messages.success(request, "Ödeme başarılı! Ürünler kütüphanenize eklendi.")
                return redirect('bag')
            else:
                messages.error(request, "Ödeme tamamlanamadı.")
                return redirect('cart')
        except stripe.error.StripeError as e:
            messages.error(request, f"Ödeme hatası: {str(e)}")
            return redirect('cart')