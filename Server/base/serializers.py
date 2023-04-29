from rest_framework import serializers
from .models import CustomUser, Category, Product, Order,Cart,OrderProduct


from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
     

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'location', 'phone_number', 'image', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'




class CreateCartSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Cart
        fields = ['user', 'product', 'quantity']




# class OrderCartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = ['id','user', 'product', 'quantity']
#         extra_kwargs = {'product': {'required': True}}



class CartSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    product = ProductSerializer()
    class Meta:
        model = Cart
        fields = ['id','user', 'product', 'quantity']

class OrderCartSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Cart
        fields = ['product', 'quantity']

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity')



class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'delivery_address', 'is_paid', 'delivery_option', 'user', 'products')

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            product = product_data.get('product')
            quantity = product_data.get('quantity')
            order_product = OrderProduct.objects.create(product=product, quantity=quantity)
            order.products.add(order_product)
        return order








class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



    #     extra_kwargs = {
    #         'password': {'write_only': True},
    #         'email': {'required': True}
    #     }

    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         email=validated_data['email'],
    #         username=validated_data['email'],
    #         password=validated_data['password']
    #     )
    #     return user

