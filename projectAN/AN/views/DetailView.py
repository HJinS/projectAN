from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from projectAN.paginator import Paginator

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
        priceQueryset = Product.objects.filter(product_id=product_id)
        infoSerializer = detailSerializer(priceQueryset[0], many=False)
        priceSerializer = priceInfoSerializer(priceQueryset.only('price', 'updated_dt'), many=True)
        priceData = priceSerializer.data
        infoData = infoSerializer.data
        infoData['priceInfo'] = priceData
        
        response = Response(infoData, status=status.HTTP_200_OK)
        return response
