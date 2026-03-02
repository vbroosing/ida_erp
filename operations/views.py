from django.views.generic import ListView, DetailView
from .models import Product

class CatalogListView(ListView):
    model = Product
    template_name = 'operations/catalog.html'
    context_object_name = 'products' # Así llamaremos a la lista en el HTML
    
    def get_queryset(self):
        # Traemos solo los productos activos e incluimos las relaciones para optimizar la BD
        return Product.objects.filter(is_active=True).select_related('brand', 'category')
    

class CatalogListView(ListView):
    model = Product
    template_name = 'operations/catalog.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('brand', 'category')

# NUEVA VISTA:
class ProductDetailView(DetailView):
    model = Product
    template_name = 'operations/product_detail.html'
    context_object_name = 'product'
    # Django automáticamente buscará el producto por su ID (pk) en la URL