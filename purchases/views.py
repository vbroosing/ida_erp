from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.db import transaction
from .models import PurchaseOrder
from .forms import PurchaseOrderForm, PurchaseOrderLineFormSet

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