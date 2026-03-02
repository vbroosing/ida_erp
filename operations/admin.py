from django.contrib import admin
from .models.catalog_models import UnitOfMeasure, Brand, Category, Product, ProductImage

# 1. MODELOS BASE (Marcas y Unidades)
@admin.register(UnitOfMeasure)
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active',)

# 2. CATEGORÍAS
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

# 3. IMÁGENES (Configuración Inline y Standalone)
# Este "Inline" permite agregar imágenes directamente DENTRO de la vista del Producto
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Muestra 1 fila vacía por defecto para agregar rápido
    fields = ('name', 'url', 'is_main', 'is_active')

# También lo registramos solo, por si quieres ver la lista completa de todas las imágenes del sistema
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('name', 'product', 'url', 'is_main', 'is_active')
    list_filter = ('is_main', 'is_active')
    search_fields = ('name', 'product__name', 'product__sku') # Permite buscar por el nombre o SKU del producto

# 4. PRODUCTOS
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'brand', 'category', 'type', 'is_active')
    list_filter = ('brand', 'category', 'type', 'is_active')
    search_fields = ('sku', 'name', 'upc')
    
    # Inyectamos el Inline de imágenes aquí
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Identificación', {
            'fields': ('sku', 'upc', 'name', 'description')
        }),
        ('Clasificación', {
            'fields': ('brand', 'category', 'unit_of_measure', 'type')
        }),
        ('Dimensiones y Logística', {
            'fields': ('weight', 'height', 'width', 'length', 'min_stock_alert')
        }),
        ('Estado y Auditoría', {
            'fields': ('is_active',),
            'classes': ('collapse',) # Esto hace que esta sección aparezca colapsada por defecto para no hacer bulto
        }),
    )