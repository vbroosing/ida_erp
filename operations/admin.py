from django.contrib import admin
from .models.catalog_models import UnitOfMeasure, Brand, Category, Product, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'brand', 'category', 'type', 'is_active')
    list_filter = ('brand', 'category', 'type', 'is_active')
    search_fields = ('sku', 'name', 'upc')
    # Esto organiza los campos en secciones dentro del formulario
    fieldsets = (
        ('Identificación', {'fields': ('sku', 'upc', 'name', 'description')}),
        ('Clasificación', {'fields': ('brand', 'category', 'unit_of_measure', 'type')}),
        ('Dimensiones y Logística', {'fields': ('weight', 'height', 'width', 'length', 'min_stock_alert')}),
    )

# admin.site.register(UnitOfMeasure)
# admin.site.register(Brand)
# admin.site.register(ProductImage)