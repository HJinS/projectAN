from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from unittest.mock import patch, MagicMock

from ..models import User

class GoogleSignInTest(APITestCase):
    def setUp(self):
        User.objects.create(
            email = 'aaaa@aaaa.com',
        )
    
    def tearDown(self):
        User.objects.all().delete()
     
    @patch("socialUser.views.requests")   
    def test_google_sign_up_success(self, mocked_request):
        client = APIClient()
        
        class MockedResponse:
            def json(self):
                return {
                    'email': 'bbb@bbb.com',
                    'first_name': 'bbbb',
                    'last_name': 'cccc',
                }
        mocked_request.get = MagicMock(return_value = MockedResponse())
        header = {'HTTP_Authorization': 'google_auth_token'}
        response = client.get('/social/google/login', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)