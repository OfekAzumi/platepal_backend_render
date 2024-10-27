from django.conf import settings
from django.shortcuts import render
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Dish,Worker,Customer,Category,Order,OrderDetails
import paypalrestsdk

# ****************************
# ******* Serizlizers ********
# ****************************

# paypal serializer
class CreatePaymentSerializer(serializers.Serializer):
    total = serializers.IntegerField()  
    unicode = serializers.IntegerField(min_value=10000, max_value=99999)  # Ensure unicode is a 5-digit number

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'


# ***************************
# ******* Implements ********
# ***************************


# ******* Register ********
@api_view(['POST'])
def register(req):
    print(req.data)
    User.objects.create_user(username=req.data["username"],password=req.data["password"])
    return Response({"user":"created"})


# ******* Login ********
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom columns (user return payload - when login)
        token['username'] = user.username
        token['email'] = user.email
        token['isadmin'] = user.is_superuser
        # ...
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ******* Dish ********
class DishView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            # If a specific ID is provided, retrieve a single dish
            return self.get_by_id(request, pk)
        my_model = Dish.objects.all()
        serializer = DishSerializer(my_model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
        my_model = Dish.objects.get(pk=pk)
        serializer = DishSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk):
        my_model = Dish.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_by_id(self, request, pk):
        try:
            dish = Dish.objects.get(pk=pk)
            serializer = DishSerializer(dish)
            return Response(serializer.data)
        except Dish.DoesNotExist:
            return Response({"error": "Dish not found"}, status=status.HTTP_404_NOT_FOUND)
        

# ******* Category ********
class CategoryView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            # If a specific ID is provided, retrieve a single category
            return self.get_by_id(request, pk)
        
        my_model = Category.objects.all()
        serializer = CategorySerializer(my_model, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        my_model = Category.objects.get(pk=pk)
        serializer = CategorySerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        my_model = Category.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_by_id(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


# ******* Worker ********
class WorkerView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            # If a specific ID is provided, retrieve a single worker
            return self.get_by_id(request, pk)
        my_model = Worker.objects.all()
        serializer = WorkerSerializer(my_model, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
        my_model = Worker.objects.get(pk=pk)
        serializer = WorkerSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk):
        my_model = Worker.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_by_id(self, request, pk):
        try:
            worker = Worker.objects.get(pk=pk)
            serializer = WorkerSerializer(worker)
            return Response(serializer.data)
        except Worker.DoesNotExist:
            return Response({"error": "Worker not found"}, status=status.HTTP_404_NOT_FOUND)


# ******* Customer ********
class CustomerView(APIView):
    def get(self, request,pk=None, phone=None):
        if pk is not None:
            return self.get_by_id(request, pk)
        if phone is not None:
            # Call the get_by_phone method
            return self.get_by_phone(request, phone)
        else:
            # Handle other cases or return a list of customers
            my_model = Customer.objects.all()
            serializer = CustomerSerializer(my_model, many=True)
            return Response(serializer.data)
    
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, pk):
        my_model = Customer.objects.get(pk=pk)
        serializer = CustomerSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, pk):
        my_model = Customer.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_by_id(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

    def get_by_phone(self, request, phone):
        try:
            customer = Customer.objects.get(phone=(phone))
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

# ******* Orders ********
class OrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            
            # Create OrderDetails objects for each item in the list
            for item in request.data['cart']:
                item['order'] = order.id
                item['dish'] = item['id']
                serializerDt = OrderDetailsSerializer(data=item)
                if serializerDt.is_valid():
                    serializerDt.save()
                else:
                    return Response(serializerDt.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk is not None:
            # If a specific ID is provided, retrieve a single worker
            return self.get_by_id(request, pk)
        my_model = Order.objects.all()
        serializer = OrderSerializer(my_model, many=True)
        return Response(serializer.data)
    
    def get_by_id(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer)
            customer_orders = customer.orders.all()
            formatted_orders = []         
            for order in customer_orders:
                formatted_orders.append({'id': order.id })
            return Response(formatted_orders)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

class OrderDetailsViewSet(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_by_id(request, pk)
        my_model = OrderDetails.objects.all()
        serializer = OrderDetailsSerializer(my_model, many=True)
        return Response(serializer.data)

    def get_by_id(self, request, pk):
        try:
            order_details = OrderDetails.objects.filter(order_id=pk)
            serializer = OrderDetailsSerializer(order_details, many=True)
            return Response(serializer.data)
        except OrderDetails.DoesNotExist:
            return Response({"error": "Order details not found"}, status=status.HTTP_404_NOT_FOUND)
        
# ***********************
# ******* PayPal ********
# ***********************
        

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

class CreatePaymentView(APIView):
    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        
        # Validate the incoming data
        if serializer.is_valid():
            total = serializer.validated_data['total']  # Total is an integer
            unicode = serializer.validated_data['unicode']  # 5-digit order number
            
            # Generate the order name using the provided unicode
            order_name = f"platepal order no. {unicode}"

            # Create PayPal payment object
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": "http://localhost:3000/loading",
                    "cancel_url": "http://localhost:3000/"
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": order_name,  # Dynamic order name
                            "price": str(total),  # Convert total to string for PayPal
                            "currency": "USD",
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(total),  # PayPal expects the total as a string
                        "currency": "USD"
                    },
                    "description": f"Payment for {order_name}"
                }]
            })

            if payment.create():
                approval_url = next(link['href'] for link in payment['links'] if link['rel'] == 'approval_url')
                return Response({"approval_url": approval_url}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)

        # If serializer is invalid, return error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExecutePaymentView(APIView):
    def post(self, request):
        payment_id = request.data.get('paymentId')
        payer_id = request.data.get('payerId')

        if not payment_id or not payer_id:
            return Response({"error": "Missing paymentId or payerId"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the payment object using the payment_id
        payment = paypalrestsdk.Payment.find(payment_id)

        # Execute the payment
        if payment.execute({"payer_id": payer_id}):  # PayerID is required to execute the payment
            return Response({"message": "Payment executed successfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)