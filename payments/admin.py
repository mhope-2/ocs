from django.contrib import admin
from .models import Tax, PaymentMethod, Payment
# Register your models here.

admin.site.register(Tax)
admin.site.register(Payment)
admin.site.register(PaymentMethod)

