from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from projectAN.paginator import Paginator

from priceInfo.models import PriceInfo
from ..models import Product
from ..serializer import priceInfoSerializer, idSerializer, detailSerializer
    
class DetailProductView(APIView, Paginator):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        print(request.data)
        serializer = idSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"msg": "Invalid data please check your request again"}, status=status.HTTP_400_BAD_REQUEST)
        product_id = serializer.data['product_id']
        queryset = PriceInfo.objects.filter(product_id=product_id).prefetch_related('price').order_by('-updated_dt')
        serializer = priceInfoSerializer(queryset, many=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        return response
