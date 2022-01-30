from rest_framework import serializers
from .models import Product

    
class productSerializer(serializers.ModelSerializer):
    like = serializers.BooleanField(required=False)
    class Meta:
        fields = ('__all__')
        model = Product
