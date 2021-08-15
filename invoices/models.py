from django.db import models
from products.models import Product
from user.models import User

# # Create your models here.
class Invoice(models.Model):
    invoice_no = models.CharField(max_length=255)
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    customer_first_name = models.CharField(max_length=255)
    customer_middle_name = models.CharField(max_length=255, blank=True, null=True)
    customer_last_name = models.CharField(max_length=255)
    net_total = models.FloatField()
    quotation_no = models.CharField(max_length=255, blank=True, null=True)
    customer_phone = models.CharField(max_length=255)
    customer_email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


class InvoiceItems(models.Model):
    invoice_no = models.CharField(max_length=255)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    description = models.CharField(max_length=191, blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
