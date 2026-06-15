from django.db import models
from django.core.exceptions import ValidationError
from product_and_catagory.models import *

from django.db.models.signals import post_save
from django.dispatch import receiver
from purchase.models import *
# Create your models here.


def validate_non_negative_fields(instance, field_names):
    errors = {}
    for field_name in field_names:
        value = getattr(instance, field_name, None)
        if value is not None and value < 0:
            errors[field_name] = 'مقدار نمی‌تواند منفی باشد.'
    if errors:
        raise ValidationError(errors)


class warehouse_info(models.Model):
    name=models.CharField(max_length=200)
    location=models.CharField(max_length=200)
    capacity=models.IntegerField() 
    capacity_by_num=models.IntegerField() 
    current_stock=models.IntegerField(blank=True, null=True)
    description=models.TextField()
    reg_date = models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def clean(self):
        validate_non_negative_fields(self, ['capacity', 'capacity_by_num', 'current_stock'])

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class inventrories(models.Model):  
    IN_OUT_CHOICES = [
        ('IN', 'In'),
        ('OUT', 'Out'),
    ]      
    product_foerignkey=models.ForeignKey(product,on_delete=models.CASCADE, related_name="product_foerignkey",null=True,blank=True)
    pucrchase_foerignkey=models.ForeignKey(Parchase,on_delete=models.CASCADE, related_name="product_foerignkey",null=True,blank=True)
    warehouse_foerignkey=models.ForeignKey(warehouse_info,on_delete=models.CASCADE,related_name="warehouse_foerignkey",null=True,blank=True)
    sale_forignkey = models.ForeignKey('Order.sale_item_part',on_delete=models.CASCADE,related_name="sale_forignkey",null=True,blank=True)
    Quantity=models.FloatField()
    weight_field = models.FloatField()
    in_and_out = models.CharField(
        max_length=3,
        choices=IN_OUT_CHOICES,
         
    )

    def clean(self):
        validate_non_negative_fields(self, ['Quantity', 'weight_field'])

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class tranfer_products(models.Model):
    date=models.CharField(max_length=200,blank=True,null=True)
    source_warehouse = models.ForeignKey(warehouse_info,on_delete=models.CASCADE,related_name="source_wareouse")
    to_warehouse = models.ForeignKey(warehouse_info,on_delete=models.CASCADE,related_name="to_warehouse")
    product_send = models.ForeignKey(product,on_delete=models.CASCADE, related_name="p")
    quantity = models.FloatField()
    weight = models.FloatField()

    def clean(self):
        validate_non_negative_fields(self, ['quantity', 'weight'])
        if self.source_warehouse_id and self.to_warehouse_id and self.source_warehouse_id == self.to_warehouse_id:
            raise ValidationError({'to_warehouse': 'گدام گیرنده باید از گدام ارسال کننده متفاوت باشد.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    


