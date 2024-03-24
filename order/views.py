from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from products.models import Product,Cart , CartItem
from .serializers import AddressHandlerSerializer , OrderListSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status,generics
from .models import AddressHandler,OrderItem
from helper.functions import generate_bill_and_send_email
class PlaceOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        request.data["user"] = user.id
        # existing_address = AddressHandler.objects.filter(user=user).exists()
        # if existing_address:
        #     return Response({"error": "User already has an address."}, status=400)
        
        serializer = AddressHandlerSerializer(data=request.data)
        if serializer.is_valid():
            cart = Cart.objects.get(user=user)
            cart_items = cart.cartitem_set.all()
            for item in cart_items:
                order_item = OrderItem.objects.create(user=user,product=item.product,quantity=item.quantity,orginal_price=item.product.price*item.quantity,payment_method= request.data["payment_type"])
            serializer.save()
            generate_bill_and_send_email(cart_items,user.email,user)
            for cart_item in cart_items:
                cart_item.delete()
            return Response({"message": "Order placed successfully."})
        else:
            return Response(serializer.errors, status=400)

class OrderItemListAPIView(generics.ListAPIView):
    serializer_class = OrderListSerializer

    def get_queryset(self):
        user = self.request.user
        return OrderItem.objects.filter(user=user)
        