from django.contrib import admin
from .models import Carrier, DeliveryLine, DeliveryOrder

# Register your models here.
admin.site.register(Carrier)
admin.site.register(DeliveryLine)
admin.site.register(DeliveryOrder)
