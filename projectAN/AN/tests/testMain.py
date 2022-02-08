from urllib import request
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from unittest.mock import patch, MagicMock

from .productFactory import ProductFactory
from socialUser.tests.userFactory import UserFactory
from priceInfo.tests.priceFactory import PriceFactory


class MainViewTest(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = APIClient()
        
        
    def test_main_view(self):
        for i in range(1000):    
            PriceFactory.create_batch(5)
        
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/main/amazon', content_type='applications/json')
        self.assertEqual(response.status_code, 200)
        