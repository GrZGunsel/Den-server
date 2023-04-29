from django.urls import path
from . import views
from .views import user_register, user_login, user_logout, user_detail,CustomUser,add_to_cart,update_cart

urlpatterns = [
    path('', views.CustomUserViewSet.as_view(), name='user_list'),
    path('users/', views.CustomUserViewSet.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('products/', views.ProductList.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('orders/', views.OrderCreateAPIView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('change-password', views.change_password, name='change_password'),
    path('cart/', add_to_cart, name='add_to_cart'),
    path('cart/<int:cart_id>/', update_cart, name='update_cart'),
    path('carts/<int:user_id>/', views.CartAPIView.as_view(), name='cart-list'),
     path('orderLists/', views.OrderListAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderRetrieveAPIView.as_view(), name='order-detail'),
]
