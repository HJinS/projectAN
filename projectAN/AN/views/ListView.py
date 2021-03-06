from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from django.db.models import (Prefetch, Exists, OuterRef, Case, When, Q)

from paginator import Paginator

from ..models import Product
from likeAN.models import LikeProduct
from ..serializer import productSerializer
from priceInfo.models import PriceInfo

from silk.profiling.profiler import silk_profile

class ListAmazonView(APIView, Paginator):
    permission_classes = [permissions.AllowAny]
    
    @silk_profile(name = "List Amazon Get")
    def get(self, request):
        if str(request.user) != "AnonymousUser":
            q = Q()
            q &= Q(product_id=OuterRef('id'))
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            queryset = Product.objects.filter(site=0).annotate(
                like = Exists(subQuery)).order_by('-updated_dt').prefetch_related(
                    Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))
        else:
            queryset = Product.objects.filter(site=0).prefetch_related(Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = productSerializer(paginated_queryset, many=True)
        response = self.get_paginated_response(data=serializer.data)
        return response
    
    @silk_profile(name = "List Amazon Post")
    def post(self, request):
        filterData = request.data["filter"]
        filter_q = Q()
        for filterItem in filterData:
            filter_q |= Q(category=filterItem)
        filter_q &= Q(site = 0)
        if str(request.user) != "AnonymousUser":
            q = Q()
            q &= Q(product_id=OuterRef('id'))
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            queryset = Product.objects.filter(filter_q).annotate(
                like = Exists(subQuery)).order_by('-updated_dt').prefetch_related(
                    Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))
        else:
            queryset = Product.objects.filter(filter_q).prefetch_related(Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = productSerializer(paginated_queryset, many=True)
        response = self.get_paginated_response(data=serializer.data)
        return response
    
class ListNeweggView(APIView, Paginator):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        if str(request.user) != "AnonymousUser":
            q = Q()
            q &= Q(product_id=OuterRef('id'))
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            queryset = Product.objects.filter(site=1).annotate(
                like = Exists(subQuery)).order_by('-updated_dt').prefetch_related(
                    Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))
        else:
            queryset = Product.objects.filter(site=1).prefetch_related(Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = productSerializer(paginated_queryset, many=True)
        response = self.get_paginated_response(data=serializer.data)
        return response
    
    def post(self, request):
        filterData = request.data["filter"]
        filter_q = Q()
        for filterItem in filterData:
            filter_q |= Q(category=filterItem)
        filter_q &= Q(site = 1)
        if str(request.user) != "AnonymousUser":
            q = Q()
            q &= Q(product_id=OuterRef('id'))
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            queryset = Product.objects.filter(filter_q).annotate(
                like = Exists(subQuery)).order_by('-updated_dt').prefetch_related(
                    Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))
        else:
            queryset = Product.objects.filter(filter_q).prefetch_related(Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = productSerializer(paginated_queryset, many=True)
        response = self.get_paginated_response(data=serializer.data)
        return response
    
class ProductSearchView(APIView, Paginator):
    permission_classes = [permissions.AllowAny]
    
    @silk_profile(name = "Search Post")
    def post(self, request):
        search_keywords = list(request.data["keyword"].split(' '))
        filter_q = Q()
        for keyword in search_keywords:
            filter_q |= Q(name__contains=keyword)
        if str(request.user) != "AnonymousUser":
            q = Q()
            q &= Q(product_id=OuterRef('id'))
            q &= Q(user_id = request.user.id)
            subQuery = LikeProduct.objects.filter(q)
            queryset = Product.objects.filter(filter_q).annotate(
                like = Exists(subQuery)).order_by('-updated_dt').prefetch_related(
                    Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))
        else:
            queryset = Product.objects.filter(filter_q).prefetch_related(Prefetch('price_relation', PriceInfo.objects.all().order_by('-updated_dt'), 'prices'))
        paginated_queryset = self.paginate_queryset(queryset, request)
        serializer = productSerializer(paginated_queryset, many=True)
        response = self.get_paginated_response(data=serializer.data)
        return response