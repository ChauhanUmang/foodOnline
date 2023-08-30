from django.contrib import admin
from orders.models import Payment, Order, OrderedProduct

# Register your models here.
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderedProduct)
