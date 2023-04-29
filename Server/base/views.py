from rest_framework import generics
from .models import CustomUser, Category, Product, Order,Cart
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, OrderSerializer, CustomUserSerializer, ChangePasswordSerializer,CartSerializer,CreateCartSerializer
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.middleware.csrf import get_token
from django.core import serializers
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt





class CustomUserViewSet(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer



class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

        
    # class OrderCreateAPIView(APIView):
    #     serializer_class = OrderSerializer
    #     def post(self, request):
    #         serializer = self.serializer_class(data=request.data)
    #         if serializer.is_valid():
    #             order = serializer.save()
    #             response_serializer = self.serializer_class(instance=order)
    #             return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class OrderRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()


class OrderListAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class CartAPIView(generics.ListAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        carts = Cart.objects.filter(user_id=user_id)
        
        return carts


# login
@csrf_exempt
@api_view(['POST'])
def add_to_cart(request):
    data = request.data.copy()
    data['quantity'] = 1
    # data['user'] = request.user.id  # set the user ID in the data # Assuming you're using Django authentication
    serializer = CreateCartSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['PUT'])
def update_cart(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CreateCartSerializer(cart, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        csrf_token = get_token(request)
        response_data = {'message': 'Successfully logged in', 'user_id': user.id, 'csrf_token': csrf_token}
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({'success': 'User logged out'})

@csrf_exempt
@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



@login_required
def user_detail(request, user_id):
    try:
        # Get CustomUser object with the given user_id
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        # Return 404 response if user does not exist
        return HttpResponseNotFound()
    # Serialize user object and convert to JSON
    user_data = serializers.serialize('json', [user, ])
    # Return user data as JSON response
    return JsonResponse(user_data, safe=False)

@csrf_exempt
@api_view(['PUT'])
def change_password(request):
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        if not user.check_password(serializer.data.get('old_password')):
            return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data.get('new_password'))
        user.save()
        return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)