from django import forms
from django.forms import inlineformset_factory
from .models import PurchaseOrder, PurchaseOrderLine

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['supplier', 'warehouse', 'expected_date']
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select'}),
            'warehouse': forms.Select(attrs={'class': 'form-select'}),
            'expected_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# ¡La magia de los Formsets! 
# Esto crea un generador de formularios para las líneas enlazadas a la orden principal
PurchaseOrderLineFormSet = inlineformset_factory(
    PurchaseOrder, # Modelo Padre
    PurchaseOrderLine, # Modelo Hijo
    fields=['product', 'quantity', 'unit_price'],
    extra=1, # Muestra 1 línea vacía por defecto
    can_delete=True,
    widgets={
        'product': forms.Select(attrs={'class': 'form-select'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
    }
)