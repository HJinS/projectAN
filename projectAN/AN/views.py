from django.forms import BooleanField
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from django.db.models import (Prefetch, Exists, OuterRef, Case, When, Q)

from .models import Product
from likeAN.models import LikeProduct
from .serializer import productSerializer


class MainAmazonView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        querySet = None
        if request.auth is not None:
            q = Q()
            q &= Q(product_id=OuterRef('id'))
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            querySet = Product.objects.filter(site=0).annotate(
                like = Exists(subQuery)).order_by('updated_dt')[:10]
        else:
            querySet = Product.objects.filter(site=0).order_by('updated_dt')[:10]
        serializer = productSerializer(querySet, many=True)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response
            
            
class MainNeweggView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        querySet = None
        if request.auth is not None:
            q = Q()
            q &= Q(product_id=OuterRef('id'))
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            querySet = Product.objects.filter(site=1).annotate(
                like = Exists(subQuery)).order_by('updated_dt')[:10]
        else:
            querySet = Product.objects.filter(site=1).order_by('updated_dt')[:10]
        serializer = productSerializer(querySet, many=True)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response