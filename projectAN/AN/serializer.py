from rest_framework import serializers
from .models import Product

    
class productSerializer(serializers.ModelSerializer):
    like = serializers.BooleanField(required=False)
    class Meta:
        fields = ('__all__')
        model = Product

class idSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    
class priceInfoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Product
        fields = ['price', 'updated_dt']

class detailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['price', 'updated_dt', 'id']