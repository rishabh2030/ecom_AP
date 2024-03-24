from django.db import models
from helper.models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
Users = get_user_model()

class Category(BaseModel):
    name = models.CharField(max_length=255,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.name}"

class Product(BaseModel):
    name = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(max_length=255,null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ImageField(upload_to='products/images')

    def __str__(self):
        return f"{self.product.name}"
    
class Rating(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],null=True,blank=True)
    review = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.name} - {self.product.name}: {self.rating}'


class Cart(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    items = models.ManyToManyField('Product', through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.name}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,null=True,blank=True)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"

