from django.db import models


class Fruit(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='fruits/', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class Order(models.Model):

    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20)

    razorpay_order_id = models.CharField(max_length=200, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
class OrderItem(models.Model):

    order = models.ForeignKey(Order,on_delete=models.CASCADE)

    fruit = models.ForeignKey(Fruit,on_delete=models.CASCADE)

    quantity = models.IntegerField()

    price = models.DecimalField(max_digits=10,decimal_places=2)