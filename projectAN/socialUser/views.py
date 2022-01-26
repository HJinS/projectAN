from email.policy import default
from django.conf import settings
from rest_framework.response import Response
from rest_framework.request import Request
from .models import User
import requests
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import status
from json.decoder import JSONDecodeError
from json import loads
from django.shortcuts import redirect
from rest_framework.views import APIView

state = getattr(settings, 'STATE')
BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'social/google/callback'
client_id = getattr(settings, "GOOGLE_OAUTH2_CLIENT_ID")
client_secret = getattr(settings, "GOOGLE_OAUTH2_CLIENT_SECRET")

class GoogleLoginView(APIView):
    def get(self, request):
        print("login first")
        print("callback uri = ", GOOGLE_CALLBACK_URI)
        scope = "https://www.googleapis.com/auth/userinfo.email"
        response = redirect(f"https://accounts.google.com/o/oauth2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST'
        return response

class GoogleCallbackView(APIView):
    def __signIn_or_signUp(self, access_token, code):
        print("signup start")
        data = {'access_token': access_token, 'code': code }
        accept = requests.post(f"{BASE_URL}social/google/login/finish/", data=data)
        print("check12")
        accept_status = accept.status_code
        print("check123")
        if accept_status != 200:
            print("failed status = ", accept_status)
            return accept, accept_status
        print("first pass")
        accept_json = accept.json()
        print("check")
        accept_json.pop('user', None)
        return accept_json, accept_status

    def __get_access_token(self, code):
        token_req = requests.post(
            f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
        token_req_json = token_req.json()
        error = token_req_json.get("error")
        if error is not None:
            raise JSONDecodeError(error)
        access_token = token_req_json.get('access_token')
        return access_token

    def __get_email_address(self, access_token):
        email_req = requests.get(
            f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
        email_req_status = email_req.status_code
        if email_req_status != 200:
            return None
        email_req_json = email_req.json()
        email = email_req_json.get('email')
        return email
    
    def get(self, request):
        print("callback")
        code = request.GET.get('code')

        try:
            access_token = self.__get_access_token(code)
        except JSONDecodeError:
            raise JSONDecodeError
            
        email = self.__get_email_address(access_token)
        if email is None:
            return Response({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
            # 다른 SNS로 가입된 유저
            social_user = SocialAccount.objects.get(user=user)
            if social_user is None:
                return Response({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
            if social_user.provider != 'google':
                return Response({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
            # 기존에 Google로 가입된 유저
            accept_json, status_result = self.__signIn_or_signUp(access_token, code)
            print(accept_json)
            refresh = accept_json.pop('refresh_token')
            response = Response(accept_json, status=status_result)
            response.set_cookie('refresh_token', refresh)
            return response
        except User.DoesNotExist:
            accept_json, status_result = self.__signIn_or_signUp(access_token, code)
            print(accept_json)
            refresh = accept_json.pop('refresh_token')
            response = Response(accept_json, status=status_result)
            response.set_cookie('refresh_token', refresh)
            return response
    
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client