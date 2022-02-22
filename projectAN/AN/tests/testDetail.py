from rest_framework.test import APIClient, APITestCase
import json
from AN.tests.productFactory import ProductFactory
from socialUser.tests.userFactory import UserFactory
from priceInfo.tests.priceFactory import PriceFactory


class DetailViewTest(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super(DetailViewTest, cls).setUpClass()
        cls.client = APIClient()
        
    def test_detail_with_login(self):
        product = ProductFactory.create()
        PriceFactory.create_batch(4, product_id = product)
        
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/detail', {'product_id': product.id})
        self.assertEqual(response.status_code, 200)
        
    def test_detail_without_login(self):
        product = ProductFactory.create()
        PriceFactory.create_batch(4, product_id = product)
            
        response = self.client.post('/product/detail', {'product_id': product.id})
        self.assertEqual(response.status_code, 200)
    
    def test_detail_fail(self):
        product = ProductFactory.create()
        PriceFactory.create_batch(4, product_id = product)
        
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/detail', {})
        self.assertEqual(response.status_code, 400)
    
    def test_detail_fail_no_data(self):
        product = ProductFactory.create()
        PriceFactory.create_batch(4, product_id = product)
        
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/detail', {'product_id': 'odsijf'})
        self.assertEqual(response.status_code, 400)