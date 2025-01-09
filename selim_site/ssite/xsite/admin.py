from django.contrib import admin
from .models import xsite, Category, Product, ProductImage, Customer, OrderItem, ShippingAddress
from .models import Product, Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)



class ProductImageInline(admin.TabularInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    
    def has_add_permission(self, request):
        if request.user.is_staff and request.user.has_perm('xsite.add_product'):
            return True
        return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_staff and request.user.has_perm('xsite.change_product'):
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(xsite)
admin.site.register(Category)
