from rest_framework import serializers
from .models import Product

    
class productSerializer(serializers.ModelSerializer):
    like = serializers.BooleanField(required=False)
    price = serializers.SerializerMethodField('get_price_prefetch')
    
    def get_price_prefetch(self, price):
        data_list = []
        prices = price.price.all()
        for price_item in prices:
            data = {'price': price_item.price, 'date': price_item.updated_dt}    
            data_list.append(data)
        return data_list
    
    class Meta:
        fields = ('__all__')
        model = Product

class idSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    
class priceInfoSerializer(serializers.ModelSerializer):    
    price = serializers.SerializerMethodField('get_price_prefetch')
    
    def get_price_prefetch(self, price):
        data_list = []
        prices = price.price.all()
        for price_item in prices:
            data = {'price': price_item.price, 'date': price_item.updated_dt}    
            data_list.append(data)
        return data_list
    
    class Meta:
        model = Product
        fields = ['price', 'updated_dt']

class detailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['price', 'updated_dt', 'id']