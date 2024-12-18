from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from xsite.models import Product,Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from xsite.models import Product, Cart, CartItem,Order,OrderItem, Rating
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserProfileUpdateForm,RatingForm,UserForm, ProfileForm,RegisterForm
from decimal import Decimal
from django.db.models import Avg
from django.db import models

def add_rating(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        user = request.user  # Giriş yapmış kullanıcı
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Daha önce değerlendirme yapılmışsa güncelle
        existing_rating = Rating.objects.filter(user=user, product=product).first()
        if existing_rating:
            existing_rating.rating = rating
            existing_rating.comment = comment
            existing_rating.save()
            return JsonResponse({'success': True, 'message': 'Değerlendirmeniz başarıyla güncellendi!'})

        # Yeni değerlendirme oluştur
        new_rating = Rating.objects.create(
            product=product,
            user=user,
            rating=rating,
            comment=comment
        )
        return JsonResponse({'success': True, 'message': 'Değerlendirmeniz başarıyla kaydedildi!'})

    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})


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

            # Değerlendirme oluştur
            Rating.objects.create(
                product=product,
                user=request.user,  # Kullanıcıyı buraya bağlayabilirsiniz
                rating=rating_value,
                comment=comment
            )

            return JsonResponse({'success': True, 'message': 'Değerlendirme başarıyla kaydedildi.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Hata: {str(e)}'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Geçersiz istek.'}, status=405)
 


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            # User verilerini güncelle
            request.user.email = form.cleaned_data.get('email')
            request.user.username = form.cleaned_data.get('username')
            request.user.save()
            profile.save()
            messages.success(request, "Profiliniz başarıyla güncellendi!")
            return redirect('edit_profile')
        else:
            messages.error(request, "Formda hata var. Lütfen düzeltin: {}".format(form.errors))
    else:
        form = UserProfileUpdateForm(user=request.user)

    return render(request, 'xsite/profile.html', {'form': form})


@csrf_exempt
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity', 0)
            cart_item = CartItem.objects.get(id=item_id)

            if quantity <= 0:
                # Remove the item if quantity is 0
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
        # Ürün formu burada oluşturulabilir
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
def profile_update(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if user_form.is_valid() and profile_form.is_valid():
            if current_password and new_password:
                if not request.user.check_password(current_password):
                    messages.error(request, 'Mevcut şifreniz yanlış.')
                elif new_password != confirm_password:
                    messages.error(request, 'Yeni şifreler eşleşmiyor.')
                else:
                    request.user.set_password(new_password)
                    update_session_auth_hash(request, request.user)  # Kullanıcıyı oturumdan atmaz
                    messages.success(request, 'Şifre başarıyla güncellendi.')

            user_form.save()
            profile_form.save()
            messages.success(request, 'Profil başarıyla güncellendi.')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Kayıt sonrası yönlendirme
    else:
        form = RegisterForm()  # GET isteğinde boş form oluştur
    return render(request, 'xsite/register.html', {'form': form})

@login_required
def ordercheckout(request):
    # Get the user's cart
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('cart')  # Redirect to cart page if no cart exists

    # Initialize total_price as a Decimal
    total_price = Decimal('0.00')

    # Calculate total price
    for item in cart.items.all():
        price = Decimal(item.product.discounted_price if item.product.apply_discount else item.product.price)
        total_price += price * item.quantity

    # Create an Order
    order = Order.objects.create(user=request.user, total_price=total_price)

    # Create OrderItems from CartItems
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=Decimal(item.product.discounted_price if item.product.apply_discount else item.product.price)
        )

    # Clear the cart
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
    context={}
    return render(request, 'xsite/bag.html',context)

def book_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # product_id'ye göre ürünü al
    images = product.images.all()  # Ürüne ait resimleri al
    return render(request, 'xsite/book.html', {'product': product, 'images': images})

def login(request):
    return render(request,"xsite/login.html")
  

def cart(request):
    context={}
    return render(request, 'xsite/cart.html',context)

def checkout(request):
    context={}
    return render(request, 'xsite/checkout.html',context)
    

