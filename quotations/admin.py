from django.contrib import admin
from .models import Quotation, QuotationItems

# Register your models here.
admin.site.register(Quotation)
admin.site.register(QuotationItems)
