from rest_framework.test import APIClient, APITestCase
import json
from AN.tests.productFactory import ProductFactory
from socialUser.tests.userFactory import UserFactory
from priceInfo.tests.priceFactory import PriceFactory
from .likeFactory import LikeFactory

class LikeViewTest(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super(LikeViewTest, cls).setUpClass()
        cls.client = APIClient()
        
    def test_main_like_with_like(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id=product)
            LikeFactory.create(user_id=user, product_id=product)
        
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/main/like')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 10)
        
    def test_list_like_with_like(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id=product)
            LikeFactory.create(user_id=user, product_id=product)
        
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/list/like')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
    
    def test_main_like_without_like(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id=product)
        
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/main/like')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)
        
    def test_list_like_without_like(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
        
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/list/like')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 0)
        
    def test_add_like(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id=product)
            product_id = product.id
        req_data = {
            'product_id': product_id,
        }
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/like/add', data=req_data)
        self.assertEqual(response.status_code, 201)
        
    def test_add_like_fail(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id=product)
        req_data = {}
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/like/add', data=req_data)
        self.assertEqual(response.status_code, 400)
        
    def test_delete_like(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id=product)
            product_id = product.id
        LikeFactory.create(user_id=user, product_id=product)
        req_data = {
            'product_id': product_id,
        }
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/like/delete', data=req_data)
        self.assertEqual(response.status_code, 202)
        
    def test_delete_like_fail(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id=product)
        req_data = {
            'product_id': "id",
        }
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/like/delete', data=req_data)
        self.assertEqual(response.status_code, 400)