from django.contrib import admin
from .models import Taxes, PaymentMethods
# Register your models here.

admin.site.register(Taxes)
admin.site.register(PaymentMethods)
