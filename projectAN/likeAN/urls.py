from django.urls import path
from . import views

urlpatterns = [
    path('main/like', views.MainLikeView.as_view()),
    path('list/like', views.ListLikeView.as_view()),
]