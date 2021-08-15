from django.contrib import admin
from .models import Quotations, QuotationItems

# Register your models here.
admin.site.register(Quotations)
admin.site.register(QuotationItems)
