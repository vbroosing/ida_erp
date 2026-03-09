from django.contrib import admin
from .models import UnitOfMeasure, Brand, Category, Product, ProductImage

admin.site.register(UnitOfMeasure)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)