from django.contrib import admin

from Customer.models import Customer,Loan,SLoan

# Register your models here.
admin.site.register(Customer)
admin.site.register(Loan)
admin.site.register(SLoan)