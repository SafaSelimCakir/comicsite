from .forms import UserProfileUpdateForm,RatingForm,UserForm, ProfileForm,RegisterForm,UserUpdateForm, ProfileUpdateForm
from xsite.models import Product, Cart, CartItem,Order,OrderItem, Rating,Product,Profile,Category
from django.contrib.auth import authenticate, update_session_auth_hash,login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Avg
from django.db import models
from decimal import Decimal
import json


def categorized_products(request):
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'checkout.html', {'categories': categories})


def get_queryset(request):
    query = request.GET.get('q', '')
    category_ids = request.GET.getlist('category')
    print(categories)
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    if category_ids:
        products = products.filter(categories__id__in=category_ids).distinct()

    categories = Category.objects.all() 
    return render(request, 'template_name.html', {
        'products': products,
        'categories': categories  
    })



def order_items_view(request):
    order_items = OrderItem.objects.filter(order__user=request.user)
    return render(request, 'template_name.html', {'order_items': order_items})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    ratings = Rating.objects.filter(product=product)
    
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'product': product,
        'ratings': ratings,
        'average_rating': round(average_rating, 2),
    }
    return render(request, 'product_detail.html', context)


@csrf_exempt
def add_rating(request, product_id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id)
            rating_value = int(request.POST.get('rating'))
            comment = request.POST.get('comment')

            Rating.objects.create(
                product=product,
                user=request.user,
                rating=rating_value,
                comment=comment
            )

            return JsonResponse({'success': True, 'message': 'Değerlendirme başarıyla kaydedildi.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Hata: {str(e)}'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Geçersiz istek.'}, status=405)
 


@csrf_exempt
@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        data = request.POST

        try:
            current_password = data.get('current_password')
            new_password = data.get('new_password')

            if current_password and new_password:
                if not user.check_password(current_password):
                    return JsonResponse({'success': False, 'error': 'Mevcut şifre yanlış.'})

                user.set_password(new_password)

            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.profile.bio = data.get('bio', user.profile.bio)

            user.save()
            user.profile.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Geçersiz istek.'})


@csrf_exempt
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity', 0)
            cart_item = CartItem.objects.get(id=item_id)

            if quantity <= 0:
                cart_item.delete()
                return JsonResponse({'success': True, 'message': 'Item removed from cart'})

            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'success': True, 'quantity': quantity})

        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


@csrf_exempt
@login_required
def update_password(request):
    if request.method == 'POST':
        user = request.user
        data = request.POST

        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not user.check_password(current_password):
            return JsonResponse({'success': False, 'error': 'Mevcut şifre yanlış.'})

        if not new_password or len(new_password) < 8:
            return JsonResponse({'success': False, 'error': 'Yeni şifre geçerli değil.'})

        user.set_password(new_password)
        user.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Geçersiz istek.'})



@login_required
def api_add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({'message': 'Product added to cart!', 'success': True})

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'xsite/cart_detail.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_detail')


@login_required
def profile_view(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    
    
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return redirect('profile')
        else:
            user_form = UserForm(instance=request.user)
            profile_form = ProfileForm(instance=request.user.profile)

        return render(request, 'xsite/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
        })
    
    return render(request, 'xsite/profile.html', {'user': request.user})


@login_required
@user_passes_test(lambda u: u.profile.is_authorized)
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        Product.objects.create(name=name, description=description, price=price, owner=request.user)
        return redirect('profile')
    return render(request, 'add_product.html')

@login_required
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id, owner=request.user)
    product.delete()
    return redirect('profile')


@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            bio = request.POST.get('bio')
            profile_picture = request.FILES.get('profile_picture')

            user = request.user
            user.username = username
            user.email = email
            user.save()

            profile = user.profile
            profile.bio = bio
            if profile_picture:
                profile.profile_picture = profile_picture
            profile.save()

            return JsonResponse({'success': True})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'success': False, 'message': 'Bir hata oluştu.'})

    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'xsite/register.html', {'form': form})

@login_required
def ordercheckout(request):
   
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('cart')  


    total_price = Decimal('0.00')

    for item in cart.items.all():
        price = Decimal(item.product.discounted_price if item.product.apply_discount else item.product.price)
        total_price += price * item.quantity

    order = Order.objects.create(user=request.user, total_price=total_price)

   
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=Decimal(item.product.discounted_price if item.product.apply_discount else item.product.price)
        )

    
    cart.items.all().delete()

    return render(request, 'xsite/order_confirmation.html', {'order': order})

def home(request):
    digital_products = Product.objects.filter(digital=True)
    context = {
        'digital_products': digital_products,
    }
    return render(request, 'xsite/home.html',context)

def information(request):
    context={}
    return render(request, 'xsite/information.html',context)

def bag(request):
    purchased_items = OrderItem.objects.filter(order__user=request.user).select_related('product')

    context = {
        'products': [item.product for item in purchased_items],
    }
    return render(request, 'xsite/bag.html',context)

def book_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)  
    images = product.images.all() 
    return render(request, 'xsite/book.html', {'product': product, 'images': images})

def login(request):
    return render(request,"xsite/login.html")
  

def cart(request):
    context={}
    return render(request, 'xsite/cart.html',context)

def checkout(request):
    context={}
    return render(request, 'xsite/checkout.html',context)
    

