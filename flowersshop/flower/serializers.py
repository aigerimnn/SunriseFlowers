
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Category, Review, Cart, CartProduct


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password')

        return attrs

class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'image_url', 'price', 'average_rating', 'category', 'description', 'reviews_count']

    def get_reviews_count(self, obj):
        count = Review.objects.filter(product=obj).count()
        return self.get_reviews_declension(count)
    
    def get_reviews_declension(self, count):
        if count == 1:
            return f"{count} отзыв"
        elif 2 <= count <= 4:
            return f"{count} отзыва"
        else:
            return f"{count} отзывов"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user_id', 'text', 'rating', 'product', 'created_at']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'price', 'status']

class CartProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) 

    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'cart'] 

class CartProductSerializerForAdd(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['id', 'product', 'cart'] 
