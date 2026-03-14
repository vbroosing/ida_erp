from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductImage, Brand, Category, UnitOfMeasure

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

# Generador de formularios para múltiples imágenes
ProductImageFormSet = inlineformset_factory(
    Product, 
    ProductImage, 
    fields=['url', 'name', 'is_main'],
    extra=1, # Muestra 1 fila vacía por defecto
    can_delete=True,
    widgets={
        'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://ejemplo.com/imagen.jpg'}),
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Vista frontal'}),
        'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
    }
)


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la marca'})}

class UnitOfMeasureForm(forms.ModelForm):
    class Meta:
        model = UnitOfMeasure
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Unidad, Kg, Litro'})}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'parent': forms.Select(attrs={'class': 'form-select'})
        }