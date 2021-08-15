from django.contrib import admin
from .models import Invoices, InvoiceItems
# Register your models here.

admin.site.register(Invoices)
admin.site.register(InvoiceItems)