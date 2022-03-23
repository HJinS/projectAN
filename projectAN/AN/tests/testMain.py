from rest_framework.test import APIClient, APITestCase
import json
from AN.tests.productFactory import ProductFactory
from socialUser.tests.userFactory import UserFactory
from priceInfo.tests.priceFactory import PriceFactory


class MainViewTest(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super(MainViewTest, cls).setUpClass()
        cls.client = APIClient()
        
        
    def test_main_amazon_with_login(self):
        for i in range(10):
            product = ProductFactory.create(site=0)
            PriceFactory.create_batch(4, product_id = product)
        
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/main/amazon')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 10)
        
    def test_main_newegg_with_login(self):
        for i in range(10):
            product = ProductFactory.create(site=1)
            PriceFactory.create_batch(4, product_id = product)
        
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/main/newegg')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 10)
        
    def test_main_amazon_without_login(self):
        for i in range(10):
            product = ProductFactory.create(site=0)
            PriceFactory.create_batch(4, product_id = product)

        response = self.client.get('/product/main/amazon')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 10)

        
    def test_main_newegg_without_login(self):
        for i in range(10):
            product = ProductFactory.create(site=1)
            PriceFactory.create_batch(4, product_id = product)
        
        response = self.client.get('/product/main/newegg')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 10)
