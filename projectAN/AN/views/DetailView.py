from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from likeAN.models import LikeProduct

from paginator import Paginator

from priceInfo.models import PriceInfo
from django.db.models import (Prefetch, Exists, OuterRef, Case, When, Q)
from ..models import Product
from ..serializer import  idSerializer, detailSerializer, productSerializer
from silk.profiling.profiler import silk_profile
    
class DetailProductView(APIView, Paginator):
    permission_classes = [permissions.AllowAny]
    
    @silk_profile(name = "Detail Product")
    def post(self, request):
        serializer = idSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"msg": "Invalid data please check your request again"}, status=status.HTTP_400_BAD_REQUEST)
        product_id = serializer.data['product_id']
        if str(request.user) != "AnonymousUser":
            q = Q()
            q &= Q(product_id=product_id)
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            queryset = Product.objects.filter(id=product_id).annotate(
                like = Exists(subQuery)).prefetch_related(
                    Prefetch('price_relation', PriceInfo.objects.all().order_by('updated_dt'), 'prices'))
        else:
            queryset = Product.objects.filter(id=product_id).prefetch_related(Prefetch('price_relation', PriceInfo.objects.all().order_by('updated_dt'), 'prices'))
        try:
            serializer = productSerializer(queryset[0], many=False)
        except Exception as e:
            return Response("No such data", status=status.HTTP_400_BAD_REQUEST)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response
