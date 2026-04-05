from django.db import models



class catagories(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField()
    reg_date = models.CharField(max_length=200)

    def __str__(self):
        return self.name
        



class product(models.Model):
    TYPE = [
        ('کیلوگرام', 'کیلوگرام'), 
        ('تعداد', 'تعداد'),  
    ]
    meat_catagory=models.ForeignKey(catagories,on_delete=models.CASCADE, related_name="meats",null=True,blank=True)
    meat_name=models.CharField(max_length=200,default='none')
    product_type = models.CharField(max_length=10,choices=TYPE,default='count',)
    reg_date = models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now=True)
    description=models.TextField()
    def __str__(self):
        return self.meat_name

