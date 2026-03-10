from django.urls import path
from .views import PurchaseOrderListView, PurchaseOrderCreateView

urlpatterns = [
    path('orders/', PurchaseOrderListView.as_view(), name='po_list'),
    path('orders/create/', PurchaseOrderCreateView.as_view(), name='po_create'),
]