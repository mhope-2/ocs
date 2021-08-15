from django.db import models
# from customers.models import Customer
# from invoices.models import Invoice
 
# Create your models here.
# class Taxes(models.Model):
#     name = models.CharField(max_length=191)
#     percentage = models.DecimalField(decimal_places=2, max_digits=10)
#     description = models.CharField(max_length=191, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now_add=True)
#     deleted_at = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return "{} | {}".format(self.name, self.percentage)


# # Create your models here.
class PaymentMethods(models.Model):
    name = models.CharField(max_length=191)
    description = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "{}".format(self.name)


# class Payments(models.Model):
#     payment_no = models.CharField(max_length=191)  # PAY00001 + 1
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     invoice = models.PositiveIntegerField()
#     payment_method = models.ForeignKey(Invoice, on_delete=models.CASCADE)
#     payment_date = models.DateField()
#     cheque_no = models.CharField(max_length=191, blank=True, null=True)
#     amount_due = models.DecimalField(decimal_places=2, max_digits=10)
#     amount_paid = models.DecimalField(decimal_places=2, max_digits=10)
#     balance_due = models.DecimalField(decimal_places=2, max_digits=10)



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