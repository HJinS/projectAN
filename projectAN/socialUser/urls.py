from django.urls import path
from . import views

urlpatterns = [
    path('google/callback', views.GoogleCallbackView.as_view(), name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
]