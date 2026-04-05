from django.db import models
from Customer.models import Customer
from product_and_catagory.models import product
from warehouse.models import warehouse_info

class Order(models.Model):
    STATUS_CHOICES = [
    ('pending', 'در انتظار'),
    ('cancel', 'لغو شده'),
    ('complete', 'تکمیل شده'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.FloatField()
    reg_date = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)



class Order_Item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=False)
    product = models.ForeignKey(product, on_delete=models.CASCADE, blank=False)
    quantity = models.IntegerField()
    total_amount = models.FloatField(blank=True, null=True)
    price_per_unit = models.FloatField()
    total_price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)






class Sale(models.Model):
    reg_date = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    total_paid_amount = models.FloatField(null=True,blank=True)
    total_remain_amount = models.FloatField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.reg_date)


class sale_item_part(models.Model):
    STATUS_CHOICES = [
        ('ضرب وزن', 'ضرب وزن'),
        ('ضرب تعداد', 'ضرب تعداد'),
    ]
    sell_forei = models.ForeignKey(Sale, on_delete=models.CASCADE, blank=True,null=True)
    product = models.ForeignKey(product, on_delete=models.CASCADE, blank=False,default='none')
    warehouse = models.ForeignKey(warehouse_info, on_delete=models.CASCADE, blank=False)
    quantity = models.FloatField()
    weight = models.FloatField()
    should_paid = models.FloatField()
    borrow_amount = models.FloatField() 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # New choice field
    paid_amount_for_every_record = models.FloatField()
    price_per_unit = models.FloatField()
    notes = models.TextField(blank=True, null=True)  

    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_money_approved = models.BooleanField(default=False)
    reamin_amount_according_to_sale_record = models.FloatField(blank=True,null=True)

    def save(self, *args, **kwargs):
        # Normalize None to zero
        remain = self.reamin_amount_according_to_sale_record or 0

        # Float-safe comparison
        if abs(remain) < 0.0001:
            self.reamin_amount_according_to_sale_record = 0
            self.is_money_approved = True
        else:
            self.is_money_approved = False

        super().save(*args, **kwargs)


    def __str__(self):
        return str(self.id)
    




class Return(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='returns')
    weight = models.FloatField()
    price_per = models.IntegerField()
    data = models.CharField(max_length=200)
    quantity = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.quantity)
    

class Return_Details(models.Model):
    customer_of_sale = models.CharField(max_length=500)
    product_of_sale = models.CharField(max_length=500)
    quantity_of_sale = models.CharField(max_length=500)
    total_amount_of_sale = models.CharField(max_length=500)
    price_per_unit_of_sale = models.CharField(max_length=500)
    rerun_of_quantity = models.CharField(max_length=400)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'Sale ID: {self.customer_of_sale.id}, Return ID: {self.rerun_of_quantity.id}'


class order_loan(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='loans')
    pay_amount = models.IntegerField()
    naem_of_giver = models.CharField(max_length=200)
    date_of_giving = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    def __str__ (self):
        return self.naem_of_giver