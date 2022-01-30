from django.urls import path
from . import views

urlpatterns = [
    path('main/amazon', views.MainAmazonView.as_view()),
    path('main/newegg', views.MainNeweggView.as_view()),
]