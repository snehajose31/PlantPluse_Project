from django.contrib import admin
from .models import User,Category2,Subcategory2,Product2,AddToCart3,WishlistItem3

admin.site.register(User)
# Register your models here.
admin.site.register(Product2)
# Register your models here.

admin.site.register(Subcategory2)
admin.site.register(Category2)
admin.site.register(AddToCart3)
admin.site.register(WishlistItem3)

