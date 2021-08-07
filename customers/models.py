from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=191)
    middle_name = models.CharField(max_length=191, blank=True, null=True)
    last_name = models.CharField(max_length=191)
    phone = models.CharField(max_length=191, blank=True, null=True)
    email = models.EmailField(max_length=191)
    address = models.CharField(max_length=191, blank=True, null=True)
    city = models.CharField(max_length=191, blank=True, null=True)
    credit_limit = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} | {} | {}".format(self.first_name, self.last_name, self.phone) 
    

# Auto gen passwords
# quotations
# orders
# invoices
# payments
# set user logout
