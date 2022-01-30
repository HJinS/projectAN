from rest_framework import serializers
from socialUser.serializer import UserSerializer
from models import LikeProduct


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeProduct
        fields = '__all__'