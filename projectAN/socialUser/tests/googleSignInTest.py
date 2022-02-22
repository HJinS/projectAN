from rest_framework.test import APIClient, APITestCase
from unittest.mock import patch, MagicMock
from requests import models

from ..models import User

class GoogleSignInTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(GoogleSignInTest, cls).setUpClass()
        cls.client = APIClient(enforce_csrf_checks=True)
    
    def tearDown(self):
        User.objects.all().delete()
    
    @patch("socialUser.views.requests")
    def test_google_sign_in_success(self, mocked_requests):
        class MockedPost:
            def json(self):
                return {
                    'refresh_token': 'DIDUwuhOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0NjExNTQyNCwiaWF0IjoxNjQ1NTEwNjI0LCJqdGkiOiI5YzZkYjU3MThmY2M0OTdiODg2MzkwMjRmNzJkM2QzYyIsInVzZXJfaWQiOjJ9.EGtMlIkIQjwrgkpFNltQuOTLQ6gV-p8p2Ivc5Bw-2FE',
                    'access_token': 'DIDUwuhOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ1NTE3ODI0LCJpYXQiOjE2NDU1MTA2MjQsImp0aSI6IjMyMTM2MTc2ZDBiOTRhMDRhODZmZjExOWRiM2U4ZDUxIiwidXNlcl9pZCI6Mn0.NpakGLDdgyaDZ8YDvK69zEIU4cVi64gun474uYpHut0',
                    'expires_in': 3599,
                    'scope': 'openid https://www.googleapis.com/auth/userinfo.email',
                    'token_type': 'Bearer',
                    'id_token': 'eyJhbGciFsadrEI1NiIsImtpZCI6ImFjYjZiZTUxZWZlYTZhNDE5ZWM5MzI1ZmVhYTFlYzQ2NjBmNWIzN2MiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI1MzM0MTczNzg5OTctbDRjM20yZHQzN3Y1dWs3OXYycTZqbjUyNzd1Z3JyZHMuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI1MzM0MTczNzg5OTctbDRjM20yZHQzN3Y1dWs3OXYycTZqbjUyNzd1Z3JyZHMuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTU5NDA1MDQzODM2NjkyMjI0MDEiLCJlbWFpbCI6IndpbmRvd2VkMThAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJEZloyYlVZZ2pxSzdRWEd4M0tNOEZ3IiwiaWF0IjoxNjQ1NTA5NjMxLCJleHAiOjE2NDU1MTMyMzF9.xNiD2GW22rL_hGh8whX6a47_nWqfeQKIMkn_nAwT3URfAjUd9arHyKuuUf_zQ4o6RHWFzMofSQQkbvOUvQZScWgv33tV3naIIfs5sCGa3ndZ6kAtw0GVhVmiXqpPeb-60-WeEUhsVZquFMP21tvcWMtowY1pIIO2EycLzodUFF-yLa5qVFCoJVbFuc70iHrRJVOhOTuCkHr0kzOO2m7-1w9Vj_7PVVW_vaQ1Vbx53p0aGNTsPleGucNab87nQqoQd89k3W9npPqLnQABQU3VNnyYTDDkexp5ziEdpVmZWD9hqWJkD5w4shUKy5cS50qAGVJjy2YFN69cLMqnovjdtw',
                    'user': {'pk': 1,
                             'email': 'test@email.com',
                             'first_name': '',
                             'last_name': ''
                            }
                }
        class MockedGet:
            def json(self):
                return {
                    'issued_to': '533127378997-l4c3m2dt37v5uk79v2q6jn5277ugrrds.apps.googleusercontent.com',
                    'audience': '533127378997-l4c3m2dt37v5uk79v2q6jn5277ugrrds.apps.googleusercontent.com',
                    'user_id': '115940504313669222412',
                    'scope': 'https://www.googleapis.com/auth/userinfo.email openid',
                    'expires_in': 3598,
                    'email': 'test@email.com',
                    'verified_email': True,
                    'access_type': 'online'
                }
        
        header = {'HTTP_Authorization': 'google_auth_token'}
        response = self.client.get('/social/google/login', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 302)
        mocked_requests.get = MagicMock(spec_from_loader=models.Response, return_value=MockedGet())
        mocked_requests.get.return_value.status_code = 200
        mocked_requests.post = MagicMock(spec_from_loader=models.Response, return_value=MockedPost())
        mocked_requests.post.return_value.status_code = 200
        response = self.client.get('/social/google/callback', content_type='applications/json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'access_token')