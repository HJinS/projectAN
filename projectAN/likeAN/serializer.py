from rest_framework import serializers
from .models import LikeProduct

class LikeSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField('get_product_prefetch_related')
    price = serializers.SerializerMethodField('get_price_prefetch')
    
    def get_product_prefetch_related(self, product):
        data = {}
        item = product.product
        data['product_id'] = item.id
        data['name'] = item.name
        data['category'] = item.category
        data['img_src'] = item.img_src
        data['site'] = item.site
        data['updated_dt'] = item.updated_dt
        return data
    
    def get_price_prefetch(self, product):
        data_list = []
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
