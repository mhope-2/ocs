from django.db import models
from customers.model import Customer

# Create your models here.
class Receipt(models.Model):
    receipt_no = models.CharField(max_digits=255)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_first_name = models.CharField(max_length=255)
    customer_middle_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at =  models.DateTimeField(blank=True, null=True)
