from django.urls import path
from .views import (
    register,
    MyTokenObtainPairView,
    DishView,
    CategoryView,
    WorkerView,
    CustomerView,
    OrderView,
    OrderDetailsViewSet,
    CreatePaymentView,
    ExecutePaymentView
)

urlpatterns = [
    path('register/', register),
    path('login/', MyTokenObtainPairView.as_view()),
    path('dishes/', DishView.as_view()),
    path('dishes/<int:pk>/', DishView.as_view(), name='dish-detail'),
    path('categories/', CategoryView.as_view()),
    path('categories/<int:pk>/', CategoryView.as_view(), name='category-detail'),
    path('orders/', OrderView.as_view()),
    path('orders/<int:pk>/', OrderView.as_view(), name='customer-orders'),
    path('orderdetails/', OrderDetailsViewSet.as_view(), name='order-details'),
    path('orderdetails/<int:pk>/', OrderDetailsViewSet.as_view(), name='order-details-by-id'),
    path('workers/', WorkerView.as_view(), name='worker-list'),
    path('workers/<int:pk>/', WorkerView.as_view(), name='worker-detail'),
    path('customers/', CustomerView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerView.as_view(), name='customer-detail'),
    path('customers/phone/<str:phone>/', CustomerView.as_view(), name='customer-by-phone'),
    path('api/payment/create/', CreatePaymentView.as_view(), name='create-payment'), 
    path('api/payment/execute/', ExecutePaymentView.as_view(), name='execute-payment'),
]
