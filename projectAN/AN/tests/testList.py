from rest_framework.test import APIClient, APITestCase
import json
from AN.tests.productFactory import ProductFactory
from likeAN.tests.likeFactory import LikeFactory
from socialUser.tests.userFactory import UserFactory
from priceInfo.tests.priceFactory import PriceFactory


class ListViewTest(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super(ListViewTest, cls).setUpClass()
        cls.client = APIClient()
        
    def test_list_amazon_with_login(self):
        for i in range(30):
            product = ProductFactory.create(site=0)
            PriceFactory.create_batch(4, product_id = product)
        
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/list/amazon')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
        
    def test_list_amazon_with_login_like(self):
        for i in range(30):
            product = ProductFactory.create(site=0)
        PriceFactory.create_batch(4, product_id = product)
        user = UserFactory.create()
        
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/list/amazon')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
        
    def test_list_newegg_with_login(self):
        user = UserFactory.create()
        for i in range(30):
            product = ProductFactory.create(site=1)
            PriceFactory.create_batch(4, product_id = product)
        LikeFactory.create(user_id=user, product_id = product)
        self.client.force_authenticate(user=user)
        
        response = self.client.get('/product/list/newegg')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
    
    def test_list_newegg_with_login_like(self):
        user = UserFactory.create()
        for i in range(30):
            product = ProductFactory.create(site=1)
            PriceFactory.create_batch(4, product_id=product)
            LikeFactory.create(user_id=user, product_id=product)
        
        self.client.force_authenticate(user=user)
        response = self.client.get('/product/list/newegg')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
        
    def test_list_amazon_without_login(self):
        for i in range(30):
            product = ProductFactory.create(site=0)
            PriceFactory.create_batch(4, product_id = product)

        response = self.client.get('/product/list/amazon')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)

        
    def test_list_newegg_without_login(self):
        for i in range(30):
            product = ProductFactory.create(site=1)
            PriceFactory.create_batch(4, product_id = product)
        
        response = self.client.get('/product/list/newegg')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
        
    def test_list_search_with_login(self):
        user = UserFactory.create()
        for i in range(30):
            product = ProductFactory.create(site=1, name='sample product name')
            PriceFactory.create_batch(4, product_id = product)
        LikeFactory.create(user_id=user, product_id = product)
        self.client.force_authenticate(user=user)
        
        response = self.client.post('/product/list/search', {"keyword":'a b c difhso sample'}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
    
    def test_list_search_with_login_like(self):
        user = UserFactory.create()
        for i in range(30):
            product = ProductFactory.create(site=1, name='sample product name')
            PriceFactory.create_batch(4, product_id=product)
            LikeFactory.create(user_id=user, product_id=product)
        
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/list/search', {"keyword":'a b c difhso sample'}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
        
    def test_list_search_without_login(self):
        for i in range(30):
            product = ProductFactory.create(site=0, name='sample product name')
            PriceFactory.create_batch(4, product_id = product)

        response = self.client.post('/product/list/search', {"keyword":'a b c difhso sample'}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)