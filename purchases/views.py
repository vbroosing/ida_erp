from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.db import transaction
from .models import PurchaseOrder
from .forms import PurchaseOrderForm, PurchaseOrderLineFormSet
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

# Importando módulo inventory
from inventory.models import Stock, Location, Kardex 


def receive_purchase_order(request, pk):
    # Buscamos la orden
    po = get_object_or_404(PurchaseOrder, pk=pk)
    
    # Validamos que no se reciba dos veces
    if po.status == PurchaseOrder.Status.RECEIVED:
        messages.error(request, f"La orden OC-{po.id} ya fue recibida anteriormente.")
        return redirect('po_list')

    if request.method == 'POST':
        # Capturamos la ubicación física donde el operario dejará la mercancía
        location_id = request.POST.get('location_id')
        location = get_object_or_404(Location, pk=location_id, warehouse=po.warehouse)

        # Transacción Atómica
        with transaction.atomic():
            # 1) Actualizamos el estado de la OC
            po.status = PurchaseOrder.Status.RECEIVED
            po.save()

            # Preparamos el tipo de contenido para el Kardex polimórfico
            po_content_type = ContentType.objects.get_for_model(PurchaseOrder)

            # 2) Iteramos sobre cada producto que viene en la orden
            for line in po.lines.all():
                # Buscamos el stock actual en esa ubicación específica, si no existe comienza en 0
                stock, created = Stock.objects.get_or_create(
                    product=line.product,
                    location=location,
                    defaults={'quantity': 0}
                )
                
                # Sumamos lo que llego
                stock.quantity += line.quantity
                stock.save()

                # 3) Dejamos el rastro de auditoría en el Kardex
                Kardex.objects.create(
                    product=line.product,
                    location=location,
                    quantity=line.quantity,
                    balance_after=stock.quantity,
                    movement_type=Kardex.MovementType.IN,
                    notes=f"Recepción automática de OC-{po.id} ({po.supplier.name})",
                    source_type=po_content_type,
                    source_id=po.id
                )
        
        messages.success(request, f"¡OC-{po.id} recibida con éxito! Stock actualizado en {location.code}.")
        return redirect('po_list')

    # Si la petición es GET, buscamos las ubicaciones disponibles en la bodega destino
    locations = Location.objects.filter(warehouse=po.warehouse)
    return render(request, 'purchases/po_receive.html', {'po': po, 'locations': locations})

class PurchaseOrderListView(ListView):
    model = PurchaseOrder
    template_name = 'purchases/po_list.html'
    context_object_name = 'orders'
    
    def get_queryset(self):
        return PurchaseOrder.objects.select_related('supplier', 'warehouse').all().order_by('-created_at')

class PurchaseOrderCreateView(CreateView):
    model = PurchaseOrder
    form_class = PurchaseOrderForm
    template_name = 'purchases/po_form.html'
    success_url = reverse_lazy('po_list')

    def get_context_data(self, **kwargs):
        # Inyectamos el Formset (las líneas) en el contexto del HTML
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['lines'] = PurchaseOrderLineFormSet(self.request.POST)
        else:
            data['lines'] = PurchaseOrderLineFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        lines = context['lines']
        
        # Guardamos todo en una sola transacción
        with transaction.atomic():
            self.object = form.save() # Guarda la cabecera (PurchaseOrder)
            if lines.is_valid():
                lines.instance = self.object # Enlaza las líneas con la cabecera
                lines.save() # Guarda los productos (PurchaseOrderLine)
                
        return super().form_valid(form)