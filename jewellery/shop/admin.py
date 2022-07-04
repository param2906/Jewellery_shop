from django.contrib import admin

# Register your models here.
from .models import product, Customer, Category, cart, Appointment, Feedback, Order


# @admin.register(product)
# class productModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'product_name', 'category', 'price', 'desc']

admin.site.register(product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Feedback)
admin.site.register(Appointment)
@admin.register(cart)
class cartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'product', 'quantity']


