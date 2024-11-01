from django.contrib import admin
from .models import xsite, Category
from .models import *
from .models import ImageCard

admin.site.register(ImageCard)

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


admin.site.register(xsite)
admin.site.register(Category)
