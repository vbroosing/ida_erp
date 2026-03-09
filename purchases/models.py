from django.db import models
from core.models import AuditModel
from catalog.models import Product
from inventory.models import Warehouse

# proveedor
class Supplier(AuditModel):
    name = models.CharField(max_length=255, verbose_name="Nombre del Proveedor")
    contact_email = models.EmailField(null=True, blank=True, verbose_name="Correo de Contacto")
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Teléfono")

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.name

# orden de compra
class PurchaseOrder(AuditModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Borrador'
        CONFIRMED = 'confirmed', 'Confirmada'
        RECEIVED = 'received', 'Recibida'
        CANCELLED = 'cancelled', 'Cancelada'

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders', verbose_name="Proveedor")
    # Relación "delivers_to" del diagrama
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='expected_purchases', verbose_name="Bodega de Destino")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name="Estado")
    expected_date = models.DateField(null=True, blank=True, verbose_name="Fecha Esperada de Entrega")

    class Meta:
        verbose_name = "Orden de Compra"
        verbose_name_plural = "Órdenes de Compra"

    def __str__(self):
        return f"OC-{self.id} | {self.supplier.name}"

# registro de ordenes de compra
class PurchaseOrderLine(AuditModel):
    # Relación "detail_of" del diagrama
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='lines', verbose_name="Orden de Compra")
    # Relación "refers_to" del diagrama
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    quantity = models.DecimalField(max_digits=15, decimal_places=4, verbose_name="Cantidad")
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Precio Unitario")

    class Meta:
        verbose_name = "Línea de Orden de Compra"
        verbose_name_plural = "Líneas de Órdenes de Compra"

    def __str__(self):
        return f"{self.product.sku} x {self.quantity}"