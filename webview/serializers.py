from rest_framework import serializers
from products.models import Product, ProductImage, Rating

class ProductImageSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        return self.context['request'].build_absolute_uri(obj.file.url)

    class Meta:
        model = ProductImage
        fields = ('file',)

class RatingSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ('user_name', 'rating','review','createdAt')
    
    def get_user_name(self, obj):
        return obj.user.name

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source='productimage_set')
    ratings = RatingSerializer(many=True, source='rating_set')

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'category', 'images', 'ratings')

class AddRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'product', 'user', 'rating', 'review']