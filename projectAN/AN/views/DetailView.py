from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from django.db.models import (Prefetch, Exists, OuterRef, Case, When, Q)

from projectAN.paginator import Paginator

from ..models import Product
from likeAN.models import LikeProduct
from ..serializer import productSerializer, idSerializer, detailSerializer
    
class DetailProductView(APIView, Paginator):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = idSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"msg": "Invalid data please check your request again"}, status=status.HTTP_400_BAD_REQUEST)
        product_id = serializer.data['product_id']
        serializer = detailSerializer(queryset2, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response
