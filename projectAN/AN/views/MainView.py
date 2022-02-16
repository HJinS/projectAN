from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from django.db.models import (Prefetch, Exists, OuterRef, Case, When, Q)

from priceInfo.models import PriceInfo

from ..models import Product
from likeAN.models import LikeProduct
from ..serializer import productSerializer

from silk.profiling.profiler import silk_profile


class MainAmazonView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @silk_profile(name = "Main Amazon")
    def get(self, request):
        querySet = None
        
        if str(request.user) != "AnonymousUser":
            q = Q()
            q &= Q(product_id=OuterRef('id'))
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            querySet = Product.objects.filter(site=0).annotate(
                like = Exists(subQuery)).order_by('-updated_dt').prefetch_related(
                    Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))[:10]
        else:
            querySet = Product.objects.filter(site=0).prefetch_related(Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))[:10]
        serializer = productSerializer(querySet, many=True)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response
            
            
class MainNeweggView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @silk_profile(name = "Main Newegg")
    def get(self, request):
        querySet = None
        if str(request.user) != "AnonymousUser":
            q = Q()
            q &= Q(product_id=OuterRef('id'))
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            querySet = Product.objects.filter(site=1).annotate(
                like = Exists(subQuery)).order_by('-updated_dt').prefetch_related(
                    Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))[:10]
        else:
            querySet = Product.objects.filter(site=1).prefetch_related(Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))[:10]
        serializer = productSerializer(querySet, many=True)
        response = Response(data=serializer.data, status=status.HTTP_200_OK)
        return response