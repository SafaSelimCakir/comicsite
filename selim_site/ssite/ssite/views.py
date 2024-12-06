from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login
from .forms import RegisterForm
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from xsite.models import Product,Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserForm, ProfileForm
from xsite.models import Product, Cart, CartItem
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from xsite.models import CartItem
from .forms import UserProfileUpdateForm

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
        data = json.loads(request.body)
        quantity = data.get('quantity')

        if quantity is None or quantity < 1:
            return JsonResponse({'success': False, 'message': 'Invalid quantity'}, status=400)

        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'success': True})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found'}, status=404)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

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
    

