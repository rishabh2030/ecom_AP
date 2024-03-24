from django.contrib import admin
from .models import OrderItem, AddressHandler
# Register your models here.
admin.site.register(OrderItem)
admin.site.register(AddressHandler)