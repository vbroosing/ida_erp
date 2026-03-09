from django.views.generic import ListView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        # Solo traemos los productos activos, optimizando la consulta
        return Product.objects.filter(is_active=True).select_related('brand', 'category')