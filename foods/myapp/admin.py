# myapp/admin.py
from django.contrib import admin
from .models import Dessert, MainCourse, Starter, Cart, CartItem, User, UserAuth

admin.site.register(Dessert)
admin.site.register(MainCourse)
admin.site.register(Starter)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(User)
admin.site.register(UserAuth)