from django.contrib import admin
from .models import xsite, Category
from .models import *
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
     # Yeni ürün oluştururken varsayılan olarak kaç resim alanı gösterileceği

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'rating', 'comment']
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(xsite)
admin.site.register(Category)
