from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView, View
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from django.conf import settings
from decimal import Decimal
import stripe
import logging
from .models import Product, Cart, CartItem, Order, OrderItem
from xsite.forms import RegisterForm, PaymentForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class StripeCheckoutRedirectView(LoginRequiredMixin, View):
    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()

        if not cart_items:
            messages.error(request, "Sepetiniz boş.")
            return redirect('cart')

        line_items = []
        for item in cart_items:
            price = item.product.discounted_price if item.product.apply_discount else item.product.price.amount
            line_items.append({
                'price_data': {
                    'currency': 'try',
                    'unit_amount': int(price * 100),
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })

        # Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/payment/success/'),
            cancel_url=request.build_absolute_uri('/cartd/'),
            metadata={'user_id': request.user.id}
        )

        return redirect(session.url)


logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeSuccessView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        if not cart_items:
            return redirect('home')  # önlem

        total_price = sum(
            item.product.discounted_price if item.product.apply_discount else item.product.price.amount
            for item in cart_items
        )

        with transaction.atomic():
            order = Order.objects.create(user=request.user, total_price=total_price)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.discounted_price if item.product.apply_discount else item.product.price.amount
                )
            cart_items.delete()

        messages.success(request, "Ödeme başarılı! Ürünler kütüphanenize eklendi.")
        return redirect('bag')


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
        products = Product.objects.filter(Q(name__icontains=query)) if query else Product.objects.all()
        return render(request, 'xsite/checkout.html', {'products': products})


class CheckoutView(ListView):
    model = Product
    template_name = 'xsite/checkout.html'
    context_object_name = 'products'

    def get(self, request):
        query = request.GET.get('q')
        products = Product.objects.filter(Q(name__icontains=query)) if query else Product.objects.all()
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
        form.save()
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
        return Product.objects.filter(orderitem__order__user=self.request.user).distinct()




class OrderCheckoutView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()

            if not cart_items:
                messages.error(request, "Sepetiniz boş.")
                return redirect('cart')

            total_price = sum(
                Decimal(str(item.product.discounted_price if item.product.apply_discount else item.product.price.amount))
                for item in cart_items
            )

            payment_method_id = request.POST.get('payment_method_id')
            if not payment_method_id:
                messages.error(request, "Ödeme yöntemi sağlanmadı.")
                return redirect('cart')

            # Stripe ödeme işlemi
            payment_intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),
                currency='try',
                payment_method=payment_method_id,
                confirm=True,
                automatic_payment_methods={'enabled': True, 'allow_redirects': 'never'}
            )

            # Satın alınan ürünleri listelemek için
            purchased_products = [item.product for item in cart_items]

            with transaction.atomic():
                order = Order.objects.create(user=request.user, total_price=total_price)
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=Decimal(str(item.product.discounted_price if item.product.apply_discount else item.product.price.amount))
                    )
                cart_items.delete()

            request.session['purchased_product_ids'] = [product.id for product in purchased_products]
            messages.success(request, "Ödeme başarılı! Ürünler kütüphanenize eklendi.")
            return redirect('cart')  # kullanıcı cart/ sayfasına yönlendirilir

        except stripe.error.StripeError as e:
            messages.error(request, f"Ödeme hatası: {str(e)}")
            return redirect('cart')
        except Exception as e:
            messages.error(request, f"Bir hata oluştu: {str(e)}")
            return redirect('cart')

def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()

    # Satın alınan ürünleri session’dan çek
    purchased_product_ids = request.session.pop('purchased_product_ids', [])
    purchased_products = Product.objects.filter(id__in=purchased_product_ids) if purchased_product_ids else []

    context = {
        'cart': cart,
        'purchased_products': purchased_products,
        'cart_items': cart_items,
        'form': PaymentForm(),
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'xsite/cart_detail.html', context)

class PaymentReturnView(View):
    def get(self, request):
        payment_intent_id = request.GET.get('payment_intent')
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if payment_intent.status == 'succeeded':
                cart = Cart.objects.get(user=request.user)
                total_price = sum(
                    item.product.discounted_price if item.product.apply_discount else item.product.price.amount
                    for item in cart.items.all()
                )

                with transaction.atomic():
                    order = Order.objects.create(user=request.user, total_price=total_price)
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
