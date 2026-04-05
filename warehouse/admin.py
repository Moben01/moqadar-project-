from django.contrib import admin

from warehouse.models import warehouse_info,inventrories,tranfer_products

admin.site.register(warehouse_info)
admin.site.register(inventrories)
admin.site.register(tranfer_products)