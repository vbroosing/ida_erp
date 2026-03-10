from django.urls import path
from .views import ProductListView, ProductCreateView, get_subcategories

urlpatterns = [
    
    # FRONTEND
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),

    # API
    path('api/subcategories/', get_subcategories, name='api_subcategories'), 

]