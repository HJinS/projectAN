from email.policy import default
from django.conf import settings
from rest_framework.response import Response
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
from silk.profiling.profiler import silk_profile

state = getattr(settings, 'STATE')
BASE_URL = str(getattr(settings, "BASE_URL"))
GOOGLE_CALLBACK_URI = BASE_URL + 'social/google/callback'
client_id = getattr(settings, "GOOGLE_OAUTH2_CLIENT_ID")
client_secret = getattr(settings, "GOOGLE_OAUTH2_CLIENT_SECRET")

class GoogleCallbackView(APIView):
    def __signIn_or_signUp(self, access_token, code):
        data = {'access_token': access_token, 'code': code }
        accept = requests.post(f"{BASE_URL}social/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return accept, accept_status
        accept_json = accept.json()
        accept_json.pop('user', None)
        return accept_json, accept_status

    def __get_access_token(self, code):
        data = {
            'code': code,
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            'redirect_uri': GOOGLE_CALLBACK_URI,
            'grant_type': 'authorization_code'
        }
        token_req = requests.post(
            f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}", data=data)
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
    
    @silk_profile(name = "Google Login Callback")
    def get(self, request):
        code = request.GET.get('code')
        try:
            access_token = self.__get_access_token(code)
        except Exception as e:
            raise JSONDecodeError
            
        email = self.__get_email_address(access_token)
        if email is None:
            return Response({'err_msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            # ????????? ????????? ????????? Provider??? google??? ????????? ?????? ??????, ????????? ?????????
            # ?????? SNS??? ????????? ??????
            social_user = SocialAccount.objects.get(user=user)
            if social_user is None:
                return Response({'err_msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
            if social_user.provider != 'google':
                return Response({'err_msg': 'no matching social type'}, status=status.HTTP_400_BAD_REQUEST)
            # ????????? Google??? ????????? ??????
            accept_json, status_result = self.__signIn_or_signUp(access_token, code)
            if status_result == 200:
                refresh = accept_json.pop('refresh_token', None)
                response = Response(accept_json, status=status_result)
                response.set_cookie('refresh_token', refresh)
                return response
            else:
                return accept_json
        except User.DoesNotExist:
            accept_json, status_result = self.__signIn_or_signUp(access_token, code)
            if status_result == 200:
                refresh = accept_json.pop('refresh_token', None)
                response = Response(accept_json, status=status_result)
                response.set_cookie('refresh_token', refresh)
                return response
            else:
                return accept_json
    
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client