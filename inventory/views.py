from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from .models import Stock, StockAdjustment, Kardex
from .forms import StockAdjustmentForm


class StockListView(ListView):
    model = Stock
    template_name = 'inventory/stock_list.html'
    context_object_name = 'stocks'
    
    def get_queryset(self):
        # select_related es crucial aquí para no saturar la BD pidiendo la bodega de cada producto
        return Stock.objects.select_related('product', 'location__warehouse').filter(is_active=True)

class StockAdjustmentCreateView(CreateView):
    model = StockAdjustment
    form_class = StockAdjustmentForm
    template_name = 'inventory/adjustment_form.html'
    success_url = reverse_lazy('stock_list')

    def form_valid(self, form):
        # ¡INICIO DE LA TRANSACCIÓN ATÓMICA!
        with transaction.atomic():
            # 1. Guardamos el documento de ajuste (Aún en estado 'Pendiente')
            adjustment = form.save(commit=False)
            adjustment.status = StockAdjustment.AdjustmentStatus.APPLIED
            adjustment.save()

            # 2. Buscamos el registro de Stock. Si no existe en ese pasillo/repisa, lo creamos en 0.
            stock, created = Stock.objects.get_or_create(
                product=adjustment.product,
                location=adjustment.location,
                defaults={'quantity': 0}
            )

            # 3. Matemática básica de inventario
            if adjustment.adjustment_type == 'increase':
                stock.quantity += adjustment.quantity
                mov_type = Kardex.MovementType.IN
            else:
                stock.quantity -= adjustment.quantity
                mov_type = Kardex.MovementType.OUT
            
            stock.save() # Actualizamos la tabla Stock

            # 4. Escribimos la huella inmutable en el Kardex
            Kardex.objects.create(
                product=adjustment.product,
                location=adjustment.location,
                quantity=adjustment.quantity,
                balance_after=stock.quantity,
                movement_type=mov_type,
                notes=adjustment.reason,
                # El Polimorfismo en acción: Enlazamos el Kardex directamente con este Ajuste
                source_type=ContentType.objects.get_for_model(StockAdjustment),
                source_id=adjustment.id
            )

        # Si llegamos aquí sin errores, PostgreSQL hace el COMMIT final.
        return super().form_valid(form)