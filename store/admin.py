from django.contrib import admin
from .models import Customer, Product, Order, OrderItem, ShippingAddress, ProductImage, ProductSize, Category

# Register standalone models
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Category)

# ProductImage Inline Configuration
class ProductImageInline(admin.TabularInline):  # Or use admin.StackedInline for a vertical layout
    model = ProductImage
    extra = 1  # Allows adding one extra blank image entry in the admin form
    fields = ['image']  # Only show the image field in the inline admin

# ProductSize Inline Configuration
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1  # Allows adding one extra blank size entry in the admin form
    fields = ['size', 'stock']  # Only show size and stock fields in the inline admin

# Register Product Model with Inlines
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')  # Fields displayed in the Product list view
    search_fields = ('name',)  # Add a search bar to filter by name
    list_filter = ('category',)  # Add a filter sidebar for categories
    inlines = [ProductImageInline, ProductSizeInline]  # Add related images and sizes inline
