from django.db import models
from django.conf import settings # Para referenciar al usuario

# MODELO BASE ABSTRACTO: es para no repetir valores de trazabilidad.
class AuditModel(models.Model):
    """
    Modelo base que incluye campos de auditoría y estado.
    No crea una tabla en la BD, solo sirve para heredar.
    """
    is_active = models.BooleanField(default=True, verbose_name="Es activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha actualización")
    
    # Opcional: Si ya tienes configurado Auth, descomenta esto
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name="%(class)s_created",
        verbose_name="Creado por"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name="%(class)s_updated",
        verbose_name="Actualizado por"
    )

    class Meta:
        abstract = True

# MODELOS DEL CATÁLOGO
# Unidad de medida
class UnitOfMeasure(AuditModel):
    name = models.CharField(max_length=50, verbose_name="Nombre Unidad")

    class Meta:
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"

    def __str__(self):
        return self.name

# Marca
class Brand(AuditModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre Marca")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.name

# Categoría
class Category(AuditModel):
    # Relación recursiva ('self')
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, blank=True, 
        related_name='subcategories',
        verbose_name="Categoría Padre"
    )
    name = models.CharField(max_length=100, verbose_name="Nombre Categoría")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        # Muestra la jerarquía en el admin (ej: "Ropa > Hombres > Camisas")
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

# Producto
class Product(AuditModel):
    # Enum para el tipo de producto
    class ProductType(models.TextChoices):
        STOCKABLE = 'stockable', 'Almacenable'
        SERVICE = 'service', 'Servicio'
        CONSUMABLE = 'consumable', 'Consumible'

    # Relaciones
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products', verbose_name="Marca")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name="Categoría")
    unit_of_measure = models.ForeignKey(UnitOfMeasure, on_delete=models.PROTECT, verbose_name="Unidad de Medida")
    
    # Identificación
    sku = models.CharField(max_length=50, unique=True, verbose_name="SKU")
    upc = models.CharField(max_length=50, null=True, blank=True, verbose_name="Código de Barras (UPC)")
    name = models.CharField(max_length=255, verbose_name="Nombre Producto")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")
    
    # Tipo
    type = models.CharField(
        max_length=20, 
        choices=ProductType.choices, 
        default=ProductType.STOCKABLE,
        verbose_name="Tipo de Producto"
    )

    # Dimensiones (Importantes para Logística)
    weight = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Peso")
    height = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Altura")
    width = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Ancho")
    length = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Largo")
    
    # Control
    min_stock_alert = models.IntegerField(default=0, verbose_name="Alerta Stock Mínimo")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"[{self.sku}] {self.name}"

# Imagenes de productos
class ProductImage(AuditModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    name = models.CharField(max_length=255, verbose_name="Título Imagen")
    
    # Usamos URLField ya que dijiste que no guardarías archivos físicos en el server
    # Si cambias de opinión, usa models.ImageField(upload_to='products/')
    url = models.URLField(max_length=500, verbose_name="URL Imagen")
    
    is_main = models.BooleanField(default=False, verbose_name="Es Portada")

    class Meta:
        verbose_name = "Imagen de Producto"
        verbose_name_plural = "Imágenes de Productos"

    def save(self, *args, **kwargs):
        # Lógica extra: Si esta es main, quitar main a las otras del mismo producto
        if self.is_main:
            ProductImage.objects.filter(product=self.product).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name