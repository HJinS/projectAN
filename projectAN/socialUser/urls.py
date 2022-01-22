from django.urls import path
from socialUser import views

urlpatterns = [
    path('google/login', views.GoogleLoginView.as_view(), name='google_login'),
    path('google/callback', views.GoogleCallbackView.as_view(), name='google_callback'),
    path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
]