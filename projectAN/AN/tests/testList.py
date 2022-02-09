from rest_framework.test import APIClient, APITestCase
from unittest.mock import patch, MagicMock
import json
from AN.tests.productFactory import ProductFactory
from socialUser.tests.userFactory import UserFactory
from priceInfo.tests.priceFactory import PriceFactory


class ListViewTest(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super(ListViewTest, cls).setUpClass()
        cls.client = APIClient()
        
    def test_list_amazon_with_login(self):
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
        
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/list/amazon')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
        
    def test_list_newegg_with_login(self):
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
        
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/list/newegg')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
        
    def test_list_amazon_without_login(self):
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)

        response = self.client.get('/product/list/amazon')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)

        
    def test_list_newegg_without_login(self):
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
        
        response = self.client.get('/product/list/newegg')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
