from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from django.db.models import (Prefetch, Exists, OuterRef, Case, When, Q)

from projectAN.paginator import Paginator

from AN.models import Product
from priceInfo.models import PriceInfo
from .models import LikeProduct
from .serializer import LikeSerializer, AddLikeSerializer

class MainLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = LikeProduct.objects.filter(user_id=request.user).prefetch_related(
            Prefetch('product_id', queryset=Product.objects.all().order_by('-updated_dt').prefetch_related(
                Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), to_attr='prices')), to_attr='product'))[:10]
        serializer = LikeSerializer(queryset, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response

class ListLikeView(APIView, Paginator):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = LikeProduct.objects.filter(user_id=request.user).prefetch_related(
            Prefetch('product_id', queryset=Product.objects.all().order_by('-updated_dt').prefetch_related(
                Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), to_attr='prices')), to_attr='product'))
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = LikeSerializer(paginated_queryset, many=True)        
        response = self.get_paginated_response(data=serializer.data)
        return response

class LikeAddView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        userId = request.user.id
        data = request.data.copy()
        data.update({'user_id': userId})
        
        serializer = AddLikeSerializer(data=data)
        if not serializer.is_valid():
            return Response({"msg": "invalid data. Please check your request"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"successfully saved"}, status=status.HTTP_201_CREATED)
    
class LikeDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        data = request.data
        
        try:
            like = LikeProduct.objects.get(user_id=request.user, product_id=data['product_id'])
            like.delete()
            return Response({"successfully deleted"}, status=status.HTTP_202_ACCEPTED)
        except LikeProduct.DoesNotExist:
            return Response({"no objects"}, status=status.HTTP_400_BAD_REQUEST)
        
            