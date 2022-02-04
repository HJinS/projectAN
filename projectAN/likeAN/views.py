from math import prod
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from django.db.models import (Prefetch, Exists, OuterRef, Case, When, Q)

from projectAN.paginator import LikePaginator

from AN.models import Product
from .models import LikeProduct
from .serializer import LikeSerializer, AddLikeSerializer
from AN.serializer import productSerializer

class MainLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        q = Q()
        q &= Q(product_id=OuterRef('id'))
        q &= Q(user_id = request.user.id)
        subQuery = LikeProduct.objects.filter(q)
        querySet1 = Product.objects.filter(site=0).annotate(
                like = Exists(subQuery)).order_by('updated_dt')[:5]
        querySet2 = Product.objects.filter(site=1).annotate(
                like = Exists(subQuery)).order_by('updated_dt')[:5]
        querySet = querySet1.union(querySet2, all=True)
        serializer = productSerializer(querySet, many=True)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response

class ListLikeView(APIView, LikePaginator):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = LikeProduct.objects.filter(user_id=request.user).prefetch_related(Prefetch('product_id', queryset=Product.objects.all(), to_attr='product'))
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
            
            
            