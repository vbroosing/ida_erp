from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.models import AuditModel
from catalog.models import Product

# Bodega
class Warehouse(AuditModel):
    code = models.CharField(max_length=50, unique=True, verbose_name="Código de Bodega")
    name = models.CharField(max_length=150, verbose_name="Nombre de Bodega")
    address = models.TextField(null=True, blank=True, verbose_name="Dirección")

    class Meta:
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"

    def __str__(self):
        return f"[{self.code}] {self.name}"

# Ubicación
class Location(AuditModel):
    class LocationType(models.TextChoices):
        AISLE = 'aisle', 'Pasillo'
        RACK = 'rack', 'Estante'
        SHELF = 'shelf', 'Repisa'
        BIN = 'bin', 'Contenedor'

    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='locations', verbose_name="Bodega")
    code = models.CharField(max_length=50, verbose_name="Código de Ubicación")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")
    location_type = models.CharField(
        max_length=20, 
        choices=LocationType.choices, 
        verbose_name="Tipo de Ubicación"
    )

    class Meta:
        verbose_name = "Ubicación"
        verbose_name_plural = "Ubicaciones"
        # Una ubicación debe ser única dentro de una bodega
        unique_together = ('warehouse', 'code')

    def __str__(self):
        return f"{self.warehouse.code} - {self.code}"

# Stock: tabla intermedia
class Stock(AuditModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='stock_records', verbose_name="Producto")
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='stock_records', verbose_name="Ubicación")
    quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0, verbose_name="Cantidad Disponible")
    reserved_quantity = models.DecimalField(max_digits=15, decimal_places=4, default=0, verbose_name="Cantidad Reservada")
    last_counted_at = models.DateTimeField(null=True, blank=True, verbose_name="Último conteo físico")

    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        # No podemos tener dos registros del mismo producto en la misma ubicación exacta
        unique_together = ('product', 'location')

    def __str__(self):
        return f"{self.product.sku} en {self.location.code}: {self.quantity}"

# ajuste de stock
class StockAdjustment(AuditModel):
    class AdjustmentType(models.TextChoices):
        INCREASE = 'increase', 'Aumento'
        DECREASE = 'decrease', 'Disminución'

    class AdjustmentStatus(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        APPLIED = 'applied', 'Aplicado'
        REJECTED = 'rejected', 'Rechazado'

    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Producto")
    location = models.ForeignKey(Location, on_delete=models.PROTECT, verbose_name="Ubicación")
    quantity = models.DecimalField(max_digits=15, decimal_places=4, verbose_name="Cantidad")
    reason = models.CharField(max_length=255, verbose_name="Motivo")
    adjustment_type = models.CharField(max_length=20, choices=AdjustmentType.choices, verbose_name="Tipo de Ajuste")
    status = models.CharField(max_length=20, choices=AdjustmentStatus.choices, default=AdjustmentStatus.PENDING, verbose_name="Estado")

    class Meta:
        verbose_name = "Ajuste de Stock"
        verbose_name_plural = "Ajustes de Stock"

    def __str__(self):
        return f"Ajuste {self.id} - {self.product.sku} ({self.adjustment_type})"

# kardex
class Kardex(AuditModel):
    class MovementType(models.TextChoices):
        IN = 'in', 'Entrada'
        OUT = 'out', 'Salida'
        TRANSFER = 'transfer', 'Transferencia'

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='kardex_movements', verbose_name="Producto")
    location = models.ForeignKey(Location, on_delete=models.PROTECT, verbose_name="Ubicación")
    quantity = models.DecimalField(max_digits=15, decimal_places=4, verbose_name="Cantidad Movida")
    balance_after = models.DecimalField(max_digits=15, decimal_places=4, verbose_name="Saldo Posterior")
    movement_type = models.CharField(max_length=20, choices=MovementType.choices, verbose_name="Tipo de Movimiento")
    notes = models.TextField(null=True, blank=True, verbose_name="Notas")

    # Campos para Relación Polimórfica (Generic relation en Django)
    # Esto permite que el origen sea una Orden de Compra, una Entrega, o un Ajuste
    source_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, verbose_name="Tipo de Documento Origen")
    source_id = models.PositiveIntegerField(verbose_name="ID Documento Origen")
    source_object = GenericForeignKey('source_type', 'source_id')

    class Meta:
        verbose_name = "Movimiento de Kardex"
        verbose_name_plural = "Movimientos de Kardex"
        indexes = [
            models.Index(fields=['product', 'location']),
            models.Index(fields=['source_type', 'source_id']),
        ]

    def __str__(self):
        return f"{self.movement_type.upper()} | {self.product.sku} | Cant: {self.quantity} | Saldo: {self.balance_after}"