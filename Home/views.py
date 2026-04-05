from django.shortcuts import render, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime, timedelta
from purchase.models import *
from Order.models import *
from expenses.models import *
from Finance_and_Accounting.models import *
import os
import subprocess
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from dbbackup.management.commands.dbbackup import Command
# Create your views here.



def index(request):
    return render (request, 'Home/index.html')

@login_required
def dashboard (request):
    selected_month = request.GET.get('month', '')  # Get the selected filter from the form
    selected_month = request.GET.get('day', '')  # Get the selected filter from the form
    end_time = now()
    Purchases = Parchase.objects.all() 
    sells = sale_item_part.objects.all() 
    masarefat = FixedExpense.objects.all()
    awayed = income.objects.all()

    if selected_month == 'روزانه':  
        start_time = end_time - timedelta(hours=23)
        Purchases = Purchases.filter(created_at__range=(start_time, end_time))
        sells = sells.filter(created_at__range=(start_time, end_time))

        masarefat = masarefat.filter(created_at__range=(start_time, end_time))
        awayed = awayed.filter(created__range=(start_time, end_time))

    elif selected_month == 'هفتگی':  
        start_time = end_time - timedelta(days=7)
        sells = sells.filter(created_at__range=(start_time, end_time))

        Purchases = Purchases.filter(created_at__range=(start_time, end_time))
        masarefat = masarefat.filter(created_at__range=(start_time, end_time))
        awayed = awayed.filter(created__range=(start_time, end_time))

    elif selected_month == 'ماهانه':  # Monthly
        start_time = end_time - timedelta(days=30)
        sells = sells.filter(created_at__range=(start_time, end_time))

        Purchases = Purchases.filter(created_at__range=(start_time, end_time))
        masarefat = masarefat.filter(created_at__range=(start_time, end_time))
        awayed = awayed.filter(created__range=(start_time, end_time))


    context = {
        'sells':sells,
        'masarefat':masarefat,
        'Purchases': Purchases,
        'awayed':awayed,
        'selected_month': selected_month,
    }
    
    return render (request, 'dashboard.html',context)

@login_required
def backup (request):
    # command = Command()
    output = command.handle()
    return HttpResponse(output)
    # management.call_command('dbbackup')
    # messages.success(request, 'دیتابیس شما به موفقیت ذخیره شد. و لطفا آنرا در جای محفوظ نگهدارید.')         
    # return render (request, 'dashboard.html')



