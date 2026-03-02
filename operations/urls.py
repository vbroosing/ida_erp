from django.urls import path
from .views import CatalogListView, ProductDetailView

app_name = 'operations'

urlpatterns = [
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    
    # NUEVA RUTA: Recibe un número entero que representa el ID del producto
    path('producto/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    
]