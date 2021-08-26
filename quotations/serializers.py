from rest_framework import serializers
from .models import Quotation, QuotationItems

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = '__all__'



class QuotationItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItems
        fields = '__all__'
