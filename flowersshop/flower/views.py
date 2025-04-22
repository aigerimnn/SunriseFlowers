from django.shortcuts import render


# Create your views here.

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import Product, Category, Review, Cart, CartProduct
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens for the newly registered user
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": serializer.data,
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=request.data['email']).first()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }, status=status.HTTP_200_OK)

class TokenRefreshView(generics.GenericAPIView):
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken(serializer.validated_data['refresh_token'])
        return Response({
            'access_token': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        category_id = request.query_params.get('category_id')
        if category_id:
            products = Product.objects.filter(category=category_id)
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def review_list(request, product_id):
    if request.method == 'GET':
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create an instance of JWTAuthentication
        jwt_authentication = JWTAuthentication()

        # Authenticate the request
        auth_result = jwt_authentication.authenticate(request)

        # Check if authentication succeeded
        if auth_result is None:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # Unpack the authentication result
        user, _ = auth_result

        user_id = user.id
        data = request.data.copy()
        data['product'] = product_id
        # Update product's average rating
        product = get_object_or_404(Product, id=product_id)

        serializer = ReviewSerializer(data={'user_id': user_id, 'text': data['text'], 'rating': data['rating'], 'product': data['product']})
        if serializer.is_valid():
            serializer.save()

            reviews = Review.objects.filter(product_id=product_id)
            total_rating = sum(review.rating for review in reviews)
            review_count = reviews.count()
            product.average_rating = total_rating / review_count
            product.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['POST'])
def cart_add(request):
    # Create an instance of JWTAuthentication
    jwt_authentication = JWTAuthentication()

    # Authenticate the request
    auth_result = jwt_authentication.authenticate(request)

    # Check if authentication succeeded
    if auth_result is None:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    # Unpack the authentication result
    user, _ = auth_result
    user_id = user.id
    # Get the product instance
    product_id = request.data.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    # Check if there is an open cart for the user
    try:
        cart = Cart.objects.get(user_id=user_id, status=1)
        # Update cart total price
        cart.price += product.price
        cart.save()
    except Cart.DoesNotExist:
        # If no open cart exists, create a new one
        cart = Cart.objects.create(user_id=user_id, price=product.price, status=1)
    
    existing_cart_product = CartProduct.objects.filter(cart=cart, product=product).first()

    if existing_cart_product:
        return Response({"message": "Product already in cart"}, status=status.HTTP_200_OK)

    # Add product to the cart
    serializer = CartProductSerializerForAdd(data={'cart': cart.id, 'product': product_id})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def cart_checkout(request):
    # Create an instance of JWTAuthentication
    jwt_authentication = JWTAuthentication()

    # Authenticate the request
    auth_result = jwt_authentication.authenticate(request)

    # Check if authentication succeeded
    if auth_result is None:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    # Unpack the authentication result
    user, _ = auth_result
    user_id = user.id

    # Find the open cart for the user
    try:
        cart = Cart.objects.get(user_id=user_id, status=1)
    except Cart.DoesNotExist:
        return Response("No open cart found for the user", status=status.HTTP_404_NOT_FOUND)

    # Change the status of the cart to indicate checkout
    cart.status = 2  # Assuming status=2 indicates checkout
    cart.save()

    return Response("Спасибо за покупку!", status=status.HTTP_200_OK)


@api_view(['GET'])
def cart_list(request):
    # Create an instance of JWTAuthentication
    jwt_authentication = JWTAuthentication()

    # Authenticate the request
    auth_result = jwt_authentication.authenticate(request)

    # Check if authentication succeeded
    if auth_result is None:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    # Unpack the authentication result
    user, _ = auth_result
    user_id = user.id

    # Get the active cart for the user
    cart = get_object_or_404(Cart, user_id=user_id, status=1)  # Assuming status=1 means active

    # Retrieve all cart products for the cart
    cart_products = CartProduct.objects.filter(cart=cart)

    # Serialize the data
    serializer = CartProductSerializer(cart_products, many=True)
    return Response(serializer.data)