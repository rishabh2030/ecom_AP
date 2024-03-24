from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product,Cart , CartItem, Rating
from .serializers import ProductSerializer,ProductImageSerializer,AddRatingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from products.models import Category
from rest_framework.exceptions import NotFound
from rest_framework import generics

class ProductListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10 
        products = Product.objects.all()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

class AddToCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity') 

        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()

        return Response({"message": "Item added to cart successfully"}, status=status.HTTP_201_CREATED)

class ViewCart(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.get(user=user)
        total = 0
        cart_items = cart.cartitem_set.all()
        cart = []  # Create an empty list to store cart items
        total = 0  # Initialize total variable

        for item in cart_items:
            item_info = {
                "product": {
                    "name": item.product.name,
                    "id": item.product.id,
                    "quantity": item.quantity,
                    "price": item.product.price
                }
            }
            cart.append(item_info)  # Add the item information to the cart list
            total += item.product.price * item.quantity

        response = {
            "cart": cart,
            "total": total
        }

        return Response(response)


class RemoveFromCart(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        product_id = request.data.get('product_id')

        product = get_object_or_404(Product, id=product_id)
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item.delete()

        return Response({"message": "Item removed from cart successfully"}, status=status.HTTP_204_NO_CONTENT)

class ProductListViewSearch(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10 
        
        search_query = request.query_params.get('q', None) 
        
        if search_query:
            products = Product.objects.filter(name__icontains=search_query)  
        else:
            return Response("No products found")
        
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

# class ProductAPIView

class CategoryProductListViewSearch(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs): 
        paginator = PageNumberPagination()
        paginator.page_size = 10 
        search_query = request.query_params.get('q', None)
        
        try:
            category_obj = Category.objects.get(name=search_query)
        except Category.DoesNotExist:
            return Response("No products found")

        products = Product.objects.filter(category=category_obj)
        
        # You can directly pass many=True to serialize a queryset
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

class RatingCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        product_id = request.data.get('product_id')  # Fetch product_id instead of product_obj
        review = request.data.get('review')
        rating = request.data.get('rating')

        try:
            # Assuming Rating model has a ForeignKey field named product
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        rating_obj = Rating.objects.create(user=user, product=product, review=review, rating=rating)
        return Response({"message": "Rating created successfully"}, status=status.HTTP_201_CREATED)
