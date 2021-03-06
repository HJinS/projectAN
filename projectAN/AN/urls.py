from django.urls import path
from .views import DetailView, ListView, MainView

urlpatterns = [
    path('main/amazon', MainView.MainAmazonView.as_view()),
    path('main/newegg', MainView.MainNeweggView.as_view()),
    path('list/amazon', ListView.ListAmazonView.as_view()),
    path('list/newegg', ListView.ListNeweggView.as_view()),
    path('list/search', ListView.ProductSearchView.as_view()),
    path('detail', DetailView.DetailProductView.as_view()),
]