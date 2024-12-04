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
    context={}
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
    

