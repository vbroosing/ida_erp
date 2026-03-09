from django.contrib import admin
from .models import Supplier, PurchaseOrder, PurchaseOrderLine

# Register your models here.
admin.site.register(Supplier)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderLine)
