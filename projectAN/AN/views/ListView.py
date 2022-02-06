from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from django.db.models import (Prefetch, Exists, OuterRef, Case, When, Q)

from projectAN.paginator import Paginator

from ..models import Product
from likeAN.models import LikeProduct
from ..serializer import productSerializer
from priceInfo.models import PriceInfo

class ListAmazonView(APIView, Paginator):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        if request.auth is not None:
            q = Q()
            q &= Q(product_id=OuterRef('id'))
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            queryset = Product.objects.filter(site=0).annotate(
                like = Exists(subQuery)).order_by('updated_dt').prefetch_related(
                    'price').order_by('-updated_dt')
        else:
            queryset = Product.objects.filter(site=0).order_by('updated_dt')
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = productSerializer(paginated_queryset, many=True)
        response = self.get_paginated_response(data=serializer.data)
        return response
    
class ListNeweggView(APIView, Paginator):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        if request.auth is not None:
            q = Q()
            q &= Q(product_id=OuterRef('id'))
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            queryset = Product.objects.filter(site=1).annotate(
                like = Exists(subQuery)).order_by('updated_dt').prefetch_related(
                    'price').order_by('-updated_dt')
        else:
            queryset = Product.objects.filter(site=1).order_by('updated_dt')
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = productSerializer(paginated_queryset, many=True)
        response = self.get_paginated_response(data=serializer.data)
        return response