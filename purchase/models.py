from django.db import models
from Supplaier.models import *
from product_and_catagory.models import *
from Customer.models import Customer


class Parchase(models.Model):
    
    STATUS_CHOICES = [
        ('ضرب وزن', 'ضرب وزن'),
        ('ضرب تعداد', 'ضرب تعداد'),
    ]
    supplaier = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE, blank=False)
    warehouse = models.ForeignKey('warehouse.warehouse_info', on_delete=models.CASCADE, blank=False)
    quantity = models.FloatField()
    total_unit = models.IntegerField() 
    date = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # New choice field

    price_per_unit = models.FloatField()
    wegiht = models.FloatField() 
    details = models.TextField(null=True,blank=True) 

    paid_amount = models.IntegerField(null=True,blank=True)
    remain_amount = models.IntegerField(null=True,blank=True)
    reg_date = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد") 

    def __str__(self):
        return f"Supplier: {self.supplaier}, Product: {self.product}, Quantity: {self.quantity},peoduct_type: {self.product.product_type}"


class item_deals(models.Model):
    STATUS_CHOICES = [
        ('رسید', 'رسید'),
        ('برداشت', 'برداشت'),
    ]
    dealer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True)
    item = models.ForeignKey(product, on_delete=models.CASCADE, blank=False)
    godam =  models.ForeignKey('warehouse.warehouse_info', on_delete=models.CASCADE, blank=False)
    date_day = models.CharField(max_length=200)
    number = models.FloatField()
    weighht = models.FloatField() 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    notes = models.TextField(null=True,blank=True) 
    def __str__(self):
        return f"Supplier: {self.dealer}"

class Purchase_loan(models.Model):
    pay_amount = models.IntegerField()
    naem_of_giver = models.CharField(max_length=200)
    date_of_giving = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    def __str__ (self):
        return self.naem_of_giver