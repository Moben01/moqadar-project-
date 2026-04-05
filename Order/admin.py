from django.contrib import admin

from Order.models import Order, Order_Item,sale_item_part

# Register your models here.
admin.site.register(Order)
admin.site.register(Order_Item)
admin.site.register(sale_item_part)