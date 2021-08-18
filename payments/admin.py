from django.contrib import admin
from .models import Tax, PaymentMethod, Payment
# Register your models here.

admin.site.register(Taxes)
admin.site.register(Payments)
admin.site.register(PaymentMethods)

