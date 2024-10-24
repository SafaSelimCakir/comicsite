from django.contrib import admin
from .models import xsite, Category
from .models import Product
admin.site.register(Product)


admin.site.register(xsite)
admin.site.register(Category)
