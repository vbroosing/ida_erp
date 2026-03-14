from django.urls import path
from . import views as _v

urlpatterns = [
    
    # FRONTEND
    path('products/', _v.ProductListView.as_view(), name='product_list'),    
    path('products/create/', _v.ProductCreateView.as_view(), name='product_create'),
    
    path('brands/', _v.BrandListView.as_view(), name='brand_list'),
    path('brands/create/', _v.BrandCreateView.as_view(), name='brand_create'),
    
    path('units/', _v.UnitListView.as_view(), name='unit_list'),
    path('units/create/', _v.UnitCreateView.as_view(), name='unit_create'),
    
    path('categories/', _v.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', _v.CategoryCreateView.as_view(), name='category_create'),
    
    
    # API
    path('api/subcategories/', _v.get_subcategories, name='api_subcategories'), 
    
]

