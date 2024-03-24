from django.urls import path
from .views import *

urlpatterns = [
    path('product_list/', ProductListView.as_view(), name='Product List'),
    path('add_cart/',AddToCart.as_view(), name='add cart'),
    path('remove_cart/',RemoveFromCart.as_view(), name='remove cart'),
    path('view_cart/',ViewCart.as_view(), name='view cart'),
    path('search/', ProductListViewSearch.as_view(), name='product-search'),
    path('category_search/', CategoryProductListViewSearch.as_view(), name='category-search'),
    path('add_review/', RatingCreateAPIView.as_view(), name='category-search'),

]