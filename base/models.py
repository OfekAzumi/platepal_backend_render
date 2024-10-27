from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    unicode = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(100), MaxValueValidator(999)])  # 3 digit number
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    unicode = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(100000), MaxValueValidator(999999)])  # 6 digit number
    phone = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    floor = models.CharField(max_length=50)
    apt = models.CharField(max_length=50)
    entry = models.CharField(max_length=50, default='', blank=True)
    notes = models.CharField(max_length=500, default='', blank=True)

    def __str__(self):
        return self.name

class Worker(models.Model):
    id = models.AutoField(primary_key=True)
    unicode = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(100000), MaxValueValidator(999999)])  # 6 digit number
    name = models.CharField(max_length=50)
    notes = models.CharField(max_length=500, default='')
    permission = models.JSONField(default=dict)
    hours = models.JSONField(default=list)

    def __str__(self):
        return self.name

class Dish(models.Model):
    id = models.AutoField(primary_key=True)
    unicode = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(1000), MaxValueValidator(9999)])  # 4 digit number
    name = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    unicode = models.PositiveIntegerField(unique=True, validators=[MinValueValidator(10000), MaxValueValidator(99999)])  # 5 digit number
    createdTime = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE, null=False, blank=False)
    payment = models.CharField(max_length=100, default='')
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.unicode)

class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    typecode = models.PositiveIntegerField() # 0 / 1
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    is_free = models.BooleanField(default=False)
    adjusted_price = models.FloatField(default=0.0) # if is_free && adjusted_price==0.0 --> a free dish

    def __str__(self):
        return f'order no.{self.order.id}'