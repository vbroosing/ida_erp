from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Excluimos is_active y los de auditoría (se llenan solos)
        fields = ['sku', 'name', 'brand', 'category', 'unit_of_measure', 'type', 'weight', 'height', 'width', 'length', 'min_stock_alert']
        
        # Le aplicamos las clases de Bootstrap a cada input
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 910-005793'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo del producto'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'unit_of_measure': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'width': forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
            'min_stock_alert': forms.NumberInput(attrs={'class': 'form-control'}),
        }