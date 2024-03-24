from django.db import models
from django.shortcuts import render
from helper.models import BaseModel
from products.models import Product
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
Users = get_user_model()

class OrderItem(BaseModel):
    PAYMENT_CHOICES = (
        ('COD', 'Cash on Delivery'),
        ('CASH', 'Cash'),
    )

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1,null=True,blank=True)
    orginal_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    payment_method = models.CharField(max_length=4, choices=PAYMENT_CHOICES,default='COD', verbose_name="Payment Method for Cash on Delivery")
    
    def __str__(self) :
        return f"{self.user.name}"

class AddressHandler(BaseModel):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone_regex = RegexValidator(
        regex=r'^\+91[6-9]\d{9}$',
        message="Phone number must be entered in the format: '+91xxxxxxxxxx'."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=14, blank=True,null=True)

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}, {self.postal_code}"