from django.db import transaction
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Product, Category, Brand,  UnitOfMeasure
from .forms import ProductForm, ProductImageFormSet, BrandForm, CategoryForm, UnitOfMeasureForm
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
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['images'] = ProductImageFormSet(self.request.POST)
        else:
            data['images'] = ProductImageFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images = context['images']
        
        with transaction.atomic():
            
            # Guardamos el producto
            self.object = form.save() 
            
            if images.is_valid():
                
                # Enlazamos las imágenes al producto
                images.instance = self.object 
                
                images.save()
                
        return super().form_valid(form)

    
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

class BrandListView(ListView):
    model = Brand
    template_name = 'catalog/brand_list.html'
    context_object_name = 'brands'
    paginate_by = 20

    def get_queryset(self):
        # 1. Solo traemos las activas (Sin select_related porque Brand no tiene llaves foráneas)
        queryset = Brand.objects.filter(is_active=True)
        
        # 2. Capturamos lo que el usuario escriba en el buscador
        query = self.request.GET.get('q')
        
        if query:
            # 3. Buscamos SOLO por el nombre (no necesitamos usar Q() porque es un solo campo)
            queryset = queryset.filter(name__icontains=query)
            
        return queryset

class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'catalog/simple_form.html'
    success_url = reverse_lazy('brand_list')
    extra_context = {'title': 'Nueva Marca', 'back_url': 'brand_list'}

# --- VISTAS DE UNIDADES ---
class UnitListView(ListView):
    model = UnitOfMeasure
    template_name = 'catalog/unit_list.html'
    context_object_name = 'units'

class UnitCreateView(CreateView):
    model = UnitOfMeasure
    form_class = UnitOfMeasureForm
    template_name = 'catalog/simple_form.html'
    success_url = reverse_lazy('unit_list')
    extra_context = {'title': 'Nueva Unidad de Medida', 'back_url': 'unit_list'}

# --- VISTAS DE CATEGORÍAS ---
class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        # select_related('parent') es vital aquí para que la tabla cargue rápido
        queryset = Category.objects.filter(is_active=True).select_related('parent')
        
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
            
        return queryset


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'catalog/category_form.html' # <--- CAMBIAR ESTA LÍNEA
    success_url = reverse_lazy('category_list')