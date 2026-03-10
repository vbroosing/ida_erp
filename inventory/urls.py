from django.urls import path
from .views import StockListView, StockAdjustmentCreateView

urlpatterns = [
    path('stock/', StockListView.as_view(), name='stock_list'),
    path('stock/adjust/', StockAdjustmentCreateView.as_view(), name='stock_adjust'),
    
]