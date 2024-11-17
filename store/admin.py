from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress, ProductImage, ProductSize

# Register other models
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

# Configure Product with inlines
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of extra empty image fields

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1  # Number of extra empty size fields

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductSizeInline]
