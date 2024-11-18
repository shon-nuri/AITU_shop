from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    description = models.TextField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="products/")

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return '/static/images/default.jpg'  # Fallback to a default image if none is set


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="product_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f'{self.product.name} - Image'


class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=10)
    stock = models.PositiveIntegerField(default=0)

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=False, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        return any(item.product.digital == False for item in self.orderitem_set.all())

    @property
    def get_cart_total(self):
        return sum(item.get_total for item in self.orderitem_set.all())

    @property
    def get_cart_items(self):
        return sum(item.quantity for item in self.orderitem_set.all())

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=False, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    zip_code = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.address

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name