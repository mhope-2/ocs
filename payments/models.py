from django.db import models
from customers.models import Customer
from invoices.models import Invoice
 
# Create your models here.
class Tax(models.Model):
    name = models.CharField(max_length=191)
    percentage = models.DecimalField(decimal_places=2, max_digits=10)
    description = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{} | {}".format(self.name, self.percentage)


# # Create your models here.
class PaymentMethod(models.Model):
    name = models.CharField(max_length=191)
    description = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)


class Payment(models.Model):
    payment_no = models.CharField(max_length=191)  # PAY00001 + 1
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_first_name = models.CharField(max_length=255)
    customer_middle_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=20)
    customer_last_name = models.CharField(max_length=255)
    invoice_no = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    payment_date = models.DateTimeField()
    amount_due = models.DecimalField(decimal_places=2, max_digits=10)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=10)
    balance_due = models.DecimalField(decimal_places=2, max_digits=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)



#     receipt_id = models.PositiveIntegerField()
#     journal_id = models.PositiveIntegerField()
#     branch_id = models.PositiveIntegerField()
#     created_at = models.DateTimeField(blank=True, null=True)
#     updated_at = models.DateTimeField(blank=True, null=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)
#     discount_allowed = models.FloatField(blank=True, null=True)
#     card_holder_name = models.CharField(max_length=600, blank=True, null=True)
#     card_number = models.CharField(max_length=600, blank=True, null=True)
#     card_cvv_number = models.CharField(max_length=600, blank=True, null=True)
#     card_expiry_date = models.CharField(max_length=600, blank=True, null=True)
#     description = models.TextField(blank=True, null=True)
#     vat_withholding_id = models.IntegerField(blank=True, null=True)
#     fixed_vat_withholding = models.FloatField(blank=True, null=True)
#     corp_withholding_id = models.IntegerField(blank=True, null=True)
#     fixed_corp_withholding = models.FloatField(blank=True, null=True)
#     total_corp_withholding = models.FloatField(blank=True, null=True)
#     total_vat_withholding = models.FloatField(blank=True, null=True)