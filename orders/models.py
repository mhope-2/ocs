from django.db import models
from customers.models import Customer
from products.models import Product


class Order(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    customer_first_name = models.CharField(max_length=255)
    customer_middle_name = models.CharField(max_length=255, blank=True, null=True)
    customer_last_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255)
    customer_email = models.EmailField()
    order_no = models.CharField(max_length=255)
    net_total = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.order_no)



class OrderItems(models.Model):
    order_no = models.CharField(max_length=255)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)