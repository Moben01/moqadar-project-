from django.db import models
from django.utils.text import slugify
import uuid
from django.apps import apps

class Customer(models.Model):
    ROLE_CHOICES = (
        ('تامین کننده', 'تامین کننده'),
        ('مشتری', 'مشتری'),
        ('هردو', 'هردو'),
    )
    reg_date = models.CharField(max_length=200,blank=True, null=True)

    name = models.CharField(max_length=30, blank=False)
    phone = models.CharField(max_length=13, blank=False)
    address = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    detail = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's not already set
            base_slug = slugify(self.name)
            unique_suffix = str(uuid.uuid4())[:8]  # Short unique identifier
            self.slug = f"{base_slug}-{unique_suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Loan(models.Model):
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
        related_name='loanss'
    )  
    sale_id = models.ForeignKey(
        'Order.sale_item_part',
        on_delete=models.CASCADE,
        related_name='saless',
        blank=True, null=True
    )  
    sale_id_for_pay = models.ManyToManyField(
        'Order.sale_item_part',
        related_name='payed',
        blank=True
    )
    sale_id_to_find_the_deletion = models.ForeignKey('Order.sale_item_part', on_delete=models.CASCADE,related_name='for_deletion',blank=True, null=True)
       
        
        

    amount = models.FloatField()  
    total_amount = models.FloatField(blank=True, null=True)  
    total_balance = models.FloatField(blank=True, null=True) 

    date_issued = models.CharField(max_length=200)  # When the loan was issued
    due_date = models.CharField(max_length=200)  # When the loan is due
    status_choices = (
        ('پرداخت نه شده', 'پرداخت نه شده'),
        ('ّپرداخت شده', 'پرداخت شده'),
        ('رسید کامل', 'رسید کامل'),
    )
    status = models.CharField(max_length=50, choices=status_choices, default='پرداخت نه شده')  # Loan status
    notes = models.TextField()  # Additional details
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan #{self.id} - {self.customer.name} - {self.notes}"



class SLoan(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='sloanss')
    sale_id = models.ForeignKey('purchase.Parchase',on_delete=models.CASCADE,related_name='ssaless',blank=True, null=True) 
    amount = models.FloatField()  
    total_amount = models.FloatField(blank=True, null=True) 
    total_balance = models.FloatField(blank=True, null=True) 

    date_issued = models.CharField(max_length=200)  
    due_date = models.CharField(max_length=200)  
    status_choices = (
        ('پرداخت نه شده', 'پرداخت نه شده'),
        ('ّپرداخت شده', 'پرداخت شده'),
        ('رسید کامل', 'رسید کامل'),
    )
    status = models.CharField(max_length=50, choices=status_choices, default='پرداخت نه شده')  
    notes = models.TextField()  
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan #{self.id} - {self.customer.name}"
