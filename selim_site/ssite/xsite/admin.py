from django.contrib import admin
from .models import xsite, Category, Product, ProductImage, Customer, OrderItem, ShippingAddress

class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    
    def has_add_permission(self, request):
        # Sadece staff status ve ilgili izni olan kullanıcılar ekleyebilir
        if request.user.is_staff and request.user.has_perm('xsite.add_product'):
            return True
        return False
    
    def has_change_permission(self, request, obj=None):
        # Sadece admin veya staff statüsünde ilgili izinlere sahip kullanıcılar düzenleyebilir
        if request.user.is_staff and request.user.has_perm('xsite.change_product'):
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Staff kullanıcıların silme yetkisi yok
        return False

# Register the models  
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(xsite)
admin.site.register(Category)
