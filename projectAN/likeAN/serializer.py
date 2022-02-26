from ast import Return
from rest_framework import serializers

from AN.models import Product
from .models import LikeProduct

class LikeSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField('get_product_prefetch_related')
    price = serializers.SerializerMethodField('get_price_prefetch')
    
    def get_product_prefetch_related(self, product):
        data = {}
        item = product.product
        if item == None:
            return None
        data['product_id'] = item.id
        data['name'] = item.name
        data['category'] = item.category
        data['img_src'] = item.img_src
        data['site'] = item.site
        data['updated_dt'] = item.updated_dt
        return data
    
    def get_price_prefetch(self, product):
        data_list = []
        if product.product == None:
            return None
        priceList = product.product.prices
        for price_item in priceList:
            data = {'price': price_item.price, 'date': price_item.updated_dt}    
            data_list.append(data)
        return data_list
    
    class Meta:
        model = LikeProduct
        exclude = ['user_id', 'id', 'product_id']
    
class AddLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeProduct
        fields = ('__all__')
        
    def create(self, validated_data):
        return LikeProduct.objects.create(**validated_data)

class LikefilterSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField('get_price_prefetch')
    class Meta:
        model = Product
        fields = ('__all__')
    
    def get_price_prefetch(self, productObj):
        data_list = []
        prices = productObj.prices
        for price_item in prices:
            data = {'price': price_item.price, 'date': price_item.updated_dt}    
            data_list.append(data)
        return data_list