from django.urls import path
from .views import *

urlpatterns = [
    path('place_orders/',PlaceOrderAPIView.as_view(),name="palce order"),
    path('order_list/',OrderItemListAPIView.as_view(),name="palce order list"),
]