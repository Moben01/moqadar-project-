from django.db import models

# Create your models here.


class coolaborators(models.Model):
    reg_date = models.CharField(max_length=200, verbose_name='تاریخ')
    name_opf = models.CharField(max_length=200, verbose_name='نام شریک')
    phone_num = models.IntegerField(verbose_name='شماره موبایل')
    adreess = models.CharField(max_length=200, verbose_name='آدرس')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_opf

class cuurency(models.Model):
    curr_name = models.CharField(max_length=200,blank=True,null=True)
    balance = models.FloatField(blank=True,null=True,default=0)
    def __str__(self):
        return self.curr_name
    

class income(models.Model):
    SAM = [
        ('دریافت', 'دریافت'),
        ('پرداخت', 'پرداخت'),
    ]
    olabrate = models.ForeignKey(coolaborators, on_delete=models.CASCADE,verbose_name='شریک')
    rec_date = models.CharField(max_length=200, verbose_name='تاریخ')
    curr = models.ForeignKey(cuurency, on_delete=models.CASCADE,verbose_name='واحد پولی',blank=True,null=True)
    exchagne_rate = models.FloatField(blank=True,null=True)
    income_amount = models.IntegerField(verbose_name='مقدار دریافت',blank=True,null=True)
    total_incme_with_last_record = models.IntegerField(blank=True,null=True)
    exchanged_moneey = models.IntegerField(blank=True,null=True)
    descriiption = models.TextField(verbose_name='توضیحات')
    is_income_or_outcome = models.CharField(max_length=200,choices=SAM)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)  
    blooelean_field = models.BooleanField(blank=True,null=True)

    def __str__(self):
        return f"Income: {self.income_amount} on {self.rec_date}"








class outcome(models.Model):
    olabrate = models.ForeignKey(coolaborators, on_delete=models.CASCADE, verbose_name='شریک')
    rec_date = models.CharField(max_length=200, verbose_name='تاریخ')
    out_come_amount = models.IntegerField(verbose_name='مقدار پرداخت')
    descriiption = models.TextField(verbose_name='توضیحات')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.out_come_amount





class total_balance(models.Model):
    total_money_in_system = models.DecimalField(max_digits=12, decimal_places=2,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.total_money_in_system)
    


class exchagn_money_in_system(models.Model):
    currency_that_you_want_tochage = models.ForeignKey(cuurency, on_delete=models.CASCADE,verbose_name='currency that change', related_name='exchanges_as_source',blank=True,null=True)
    amount = models.FloatField()
    currency_that_you_want_to_get_money = models.ForeignKey(cuurency, on_delete=models.CASCADE,verbose_name='currency that want',related_name='exchanges_as_target',blank=True,null=True)
    want_amount = models.FloatField()
    currency_that_will_chage_amount = models.FloatField()
    currency_that_chage_amont = models.FloatField()
    exchabge_rate = models.FloatField()
    chaged_amont = models.FloatField(blank=True,null=True)
    note = models.TextField(blank=True,null=True)

    def __str__(self):
        return str(self.id)

