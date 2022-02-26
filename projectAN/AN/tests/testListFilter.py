from rest_framework.test import APIClient, APITestCase
import json
from AN.tests.productFactory import ProductFactory
from likeAN.tests.likeFactory import LikeFactory
from socialUser.tests.userFactory import UserFactory
from priceInfo.tests.priceFactory import PriceFactory


class ListViewTestFilter(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        super(ListViewTestFilter, cls).setUpClass()
        cls.client = APIClient()
        cls.correctFilter = ["intel cpu", "amd cpu", "ddr5 ram", "nvme ssd", "liquid cpu cooler", "air cpu cooler"]
        cls.wrongFilter = ["int cpu", "nvid gpu", "ddr ram"]
        
    def test_list_amazon_with_login_and_correct_filter(self):
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
        
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/list/amazon', {"filter": self.correctFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
        
    def test_list_amazon_with_login_like_and_correct_filter(self):
        for i in range(1000):
            product = ProductFactory.create()
        PriceFactory.create_batch(4, product_id = product)
        user = UserFactory.create()
        
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/list/amazon', {"filter": self.correctFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
        
    def test_list_newegg_with_login_and_correct_filter(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
        LikeFactory.create(user_id=user, product_id = product)
        self.client.force_authenticate(user=user)
        
        response = self.client.post('/product/list/newegg', {"filter": self.correctFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
    
    def test_list_newegg_with_login_like_correct_filter(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
            LikeFactory.create(user_id=user, product_id = product)
        
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/list/newegg', {"filter": self.correctFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)
        
    def test_list_amazon_without_login_and_correct_filter(self):
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)

        response = self.client.post('/product/list/amazon', {"filter": self.correctFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)

        
    def test_list_newegg_without_login_and_correct_filter(self):
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
        
        response = self.client.post('/product/list/newegg', {"filter": self.correctFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 30)

    def test_list_amazon_with_login_and_wrong_filter(self):
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
        
        user = UserFactory.create()
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/list/amazon', {"filter": self.wrongFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 0)
        
    def test_list_amazon_with_login_like_and_wrong_filter(self):
        for i in range(1000):
            product = ProductFactory.create()
        PriceFactory.create_batch(4, product_id = product)
        user = UserFactory.create()
        
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/list/amazon', {"filter": self.wrongFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 0)
        
    def test_list_newegg_with_login_and_wrong_filter(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
        LikeFactory.create(user_id=user, product_id = product)
        self.client.force_authenticate(user=user)
        
        response = self.client.post('/product/list/newegg', {"filter": self.wrongFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 0)
    
    def test_list_newegg_with_login_like_wrong_filter(self):
        user = UserFactory.create()
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
            LikeFactory.create(user_id=user, product_id = product)
        
        self.client.force_authenticate(user=user)
        response = self.client.post('/product/list/newegg', {"filter": self.wrongFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 0)
        
    def test_list_amazon_without_login_and_wrong_filter(self):
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)

        response = self.client.post('/product/list/amazon', {"filter": self.wrongFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 0)

        
    def test_list_newegg_without_login_and_wrong_filter(self):
        for i in range(1000):
            product = ProductFactory.create()
            PriceFactory.create_batch(4, product_id = product)
        
        response = self.client.post('/product/list/newegg', {"filter": self.wrongFilter}, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['results']), 0)