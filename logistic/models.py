from django.db import models
from core.models import AuditModel
from catalog.models import Product

# Transporte
class Carrier(AuditModel):
    name = models.CharField(max_length=150, verbose_name="Nombre del Transportista")
    # Aquí a futuro podrías agregar RUT, teléfono de contacto, email, etc.

    class Meta:
        verbose_name = "Transportista"
        verbose_name_plural = "Transportistas"

    def __str__(self):
        return self.name

# Órden de transporte
class DeliveryOrder(AuditModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        IN_TRANSIT = 'in_transit', 'En Tránsito'
        DELIVERED = 'delivered', 'Entregada'
        CANCELLED = 'cancelled', 'Cancelada'

    carrier = models.ForeignKey(Carrier, on_delete=models.PROTECT, related_name='delivery_orders', verbose_name="Transportista")
    tracking_number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Número de Seguimiento")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name="Estado")
    
    # Fechas importantes para la logística
    shipped_date = models.DateField(null=True, blank=True, verbose_name="Fecha de Envío")
    estimated_delivery = models.DateField(null=True, blank=True, verbose_name="Fecha Estimada de Entrega")
    actual_delivery = models.DateField(null=True, blank=True, verbose_name="Fecha Real de Entrega")

    class Meta:
        verbose_name = "Orden de Despacho"
        verbose_name_plural = "Órdenes de Despacho"

    def __str__(self):
        return f"OD-{self.id} | {self.carrier.name} ({self.get_status_display()})"

# Linea de despacho
class DeliveryLine(AuditModel):
    delivery_order = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE, related_name='lines', verbose_name="Orden de Despacho")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    quantity = models.DecimalField(max_digits=15, decimal_places=4, verbose_name="Cantidad a despachar")

    class Meta:
        verbose_name = "Línea de Despacho"
        verbose_name_plural = "Líneas de Despacho"

    def __str__(self):
        return f"{self.product.sku} x {self.quantity} (OD-{self.delivery_order.id})"