from django.shortcuts import render, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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


DASHBOARD_PAGE_SIZE = 10


def paginate_dashboard_records(request, queryset, page_param):
    paginator = Paginator(queryset, DASHBOARD_PAGE_SIZE)
    return paginator.get_page(request.GET.get(page_param))


def index(request):
    return render (request, 'Home/index.html')

@login_required
def dashboard (request):
    selected_month = request.GET.get('month') or request.GET.get('day') or ''
    end_time = now()
    Purchases = Parchase.objects.select_related('supplaier', 'product').all().order_by('-id')
    sells = sale_item_part.objects.select_related('sell_forei__customer', 'product').all().order_by('-id')
    masarefat = FixedExpense.objects.all().order_by('-id')
    awayed = income.objects.select_related('olabrate', 'curr').all().order_by('-id')
    receipts = item_deals.objects.select_related('dealer', 'item', 'godam').filter(status='رسید').order_by('-id')

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


    purchases_page = paginate_dashboard_records(request, Purchases, 'purchases_page')
    sells_page = paginate_dashboard_records(request, sells, 'sells_page')
    receipts_page = paginate_dashboard_records(request, receipts, 'receipts_page')
    masarefat_page = paginate_dashboard_records(request, masarefat, 'masarefat_page')
    awayed_page = paginate_dashboard_records(request, awayed, 'awayed_page')

    context = {
        'sells': sells_page,
        'masarefat': masarefat_page,
        'Purchases': purchases_page,
        'purchases': purchases_page,
        'awayed': awayed_page,
        'receipts': receipts_page,
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



