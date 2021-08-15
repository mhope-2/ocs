from rest_framework import serializers
from .models import Invoices, InvoiceItems

class Invoiceserializer(serializers.ModelSerializer):
    class Meta:
        model = Invoices
        fields = '__all__'



class InvoiceItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItems
        fields = '__all__'
