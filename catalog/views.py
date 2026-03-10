from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Product, Category
from .forms import ProductForm
from django.http import JsonResponse

def get_subcategories(request):
    """
    Endpoint para alimentar los selects en cascada mediante AJAX.
    """
    parent_id = request.GET.get('parent_id')
    
    if parent_id:
        # Si envían un padre, buscamos sus hijos directos
        categories = Category.objects.filter(parent_id=parent_id, is_active=True).values('id', 'name')
    else:
        # Si no envían padre, buscamos las categorías raíz (las que no tienen padre)
        categories = Category.objects.filter(parent__isnull=True, is_active=True).values('id', 'name')
        
    return JsonResponse(list(categories), safe=False)

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    # Cuando guarde con éxito, nos devolverá a la lista de productos
    success_url = reverse_lazy('product_list')

    
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 2  # ¡Clave para la escalabilidad! Muestra de a 20 productos.

    def get_queryset(self):
        # 1. select_related evita que Django haga 15,000 consultas extra a la BD
        queryset = Product.objects.filter(is_active=True).select_related('brand', 'category')
        
        # 2. Capturamos lo que el usuario escriba en el buscador
        query = self.request.GET.get('q')
        
        if query:
            # 3. Buscamos si el texto coincide con el nombre O el SKU (insensible a mayúsculas)
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(sku__icontains=query)
            )
            
        return queryset

