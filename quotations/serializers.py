from rest_framework import serializers
from .models import Quotations, QuotationItems

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotations
        fields = '__all__'



class QuotationItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuotationItems
        fields = '__all__'
