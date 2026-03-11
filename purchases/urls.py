from django.urls import path
from .views import PurchaseOrderListView, PurchaseOrderCreateView, receive_purchase_order

urlpatterns = [
    path('orders/', PurchaseOrderListView.as_view(), name='po_list'),
    path('orders/create/', PurchaseOrderCreateView.as_view(), name='po_create'),
    path('orders/<int:pk>/receive/', receive_purchase_order, name='po_receive'),
]