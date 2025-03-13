from django.contrib import admin
from .models import ShippingAddress, Order, OrderdItem
from django.contrib.auth.models import User

# Register your models here.

# Register the model on the admin section thing 
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderdItem) 


class OrderItemInline(admin.StackedInline):
    model = OrderdItem
    extra = 1  # Optional: Defines extra empty forms in admin panel

# Extend Order Model
class OrderAdmin(admin.ModelAdmin):  # Use ModelAdmin instead of StackedInline
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "shipped", "date_shipped"]
    inlines = [OrderItemInline]

# Unregister and re-register Order model correctly
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin) 