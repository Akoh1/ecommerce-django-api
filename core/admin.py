from django.contrib import admin

# Register your models here.

from core.models.auth import User, BillingAddress, States, Countries
from core.models.cart import Products

admin.site.register(User)
admin.site.register(States)
admin.site.register(Countries)
admin.site.register(BillingAddress)
admin.site.register(Products)
