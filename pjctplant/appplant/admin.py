from django.contrib import admin
from .models import Product,User,WishlistItem

admin.site.register(User)
# Register your models here.
admin.site.register(Product)
# Register your models here.
admin.site.register(WishlistItem)
