from rest_framework import serializers
from .models import AddressHandler,OrderItem

class AddressHandlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressHandler
        fields = '__all__'

class OrderListSerializer(serializers.ModelSerializer):
    address = AddressHandlerSerializer(source='user.addresshandler_set.first', read_only=True)
    product_name = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity', 'orginal_price', 'discounted_price', 'payment_method', 'address']
    
    def get_product_name(self, obj):
        return obj.product.name