from rest_framework import serializers
from .models import LikeProduct

class LikeSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField('get_product_prefetch_related')
    
    def get_product_prefetch_related(self, product):
        data = {}
        item = product.product
        data['product_id'] = item.product_id
        data['name'] = item.name
        data['price'] = item.price
        data['category'] = item.category
        data['img_src'] = item.img_src
        data['site'] = item.site
        data['updated_dt'] = item.updated_dt
        data['id'] = item.id
        return data
    
    class Meta:
        model = LikeProduct
        exclude = ['user_id', 'id', 'product_id']
        
class AddLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeProduct
        fields = ('__all__')
        
    def create(self, validated_data):
        return LikeProduct.objects.create(**validated_data)
        