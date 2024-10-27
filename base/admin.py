from django.contrib import admin
from .models import Category,Dish,Customer,Order,OrderDetails,Worker
# Register your models here.
admin.site.register([Category,Dish,Customer,Order,OrderDetails,Worker])