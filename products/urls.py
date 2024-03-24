from django.urls import path
from .views import *

urlpatterns = [
    path('get_product/<int:id>/',ProductView.as_view(),name="product_view"),
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
]
