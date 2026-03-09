from django.contrib import admin
from .models import Warehouse, Location, Stock, StockAdjustment, Kardex

admin.site.register(Warehouse)
admin.site.register(Location)
admin.site.register(Stock)
admin.site.register(StockAdjustment)
admin.site.register(Kardex)