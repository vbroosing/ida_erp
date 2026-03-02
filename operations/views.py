from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Product

class CatalogListView(ListView):
    model = Product
    template_name = 'operations/catalog.html'
    context_object_name = 'products'
    paginate_by = 1
    
    def get_queryset(self):
        # 1. Consulta base (lo que ya tenías)
        queryset = Product.objects.filter(is_active=True).select_related('brand', 'category')
        
        # 2. Capturamos lo que viene en la URL por el método GET (ej: ?q=arduino)
        query = self.request.GET.get('q')
        
        # 3. Si el usuario escribió algo, aplicamos el filtro
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(sku__icontains=query)
            )
            
        return queryset

class ProductDetailView(DetailView):
    model = Product
    template_name = 'operations/product_detail.html'
    context_object_name = 'product'