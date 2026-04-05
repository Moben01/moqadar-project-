from django.shortcuts import render,HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import datetime, timedelta
from purchase.models import *
from Order.models import *
from expenses.models import *
from django.db.models import Sum
from Finance_and_Accounting.models import *

# Create your views here.


def reports(request):

    selected_month = request.GET.get('month', '') 
    selected_month = request.GET.get('day', '') 
    end_time = now()
    Purchases = Parchase.objects.all() 


    if selected_month == 'روزانه':  
        start_time = end_time - timedelta(hours=23)
        Purchases = Purchases.filter(created_at__range=(start_time, end_time))

    elif selected_month == 'هفتگی':  
        start_time = end_time - timedelta(days=7)
        sells = sells.filter(created__range=(start_time, end_time))

    elif selected_month == 'ماهانه':  # Monthly
        start_time = end_time - timedelta(days=30)
        sells = sells.filter(created__range=(start_time, end_time))
    total_units = Purchases.aggregate(total_unit_sum=Sum('total_unit'))['total_unit_sum'] or 0


    context = {
        'Purchases': Purchases,
        'selected_month': selected_month,
        'total_units':total_units,
    }
    
    return render(request, 'report/all_report.html',context)


def sell_report(request):
    selected_month = request.GET.get('month', '')  # Get the selected filter from the form
    selected_month = request.GET.get('day', '')  # Get the selected filter from the form
    end_time = now()
    sells = Sale.objects.all() 

    if selected_month == 'روزانه':  
        start_time = end_time - timedelta(hours=23)
        sells = sells.filter(created__range=(start_time, end_time))

    elif selected_month == 'هفتگی':  
        start_time = end_time - timedelta(days=7)
        sells = sells.filter(created__range=(start_time, end_time))

    elif selected_month == 'ماهانه':  # Monthly
        start_time = end_time - timedelta(days=30)
        sells = sells.filter(created__range=(start_time, end_time))
    total_sales = sells.aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        'sells':sells,
        'selected_month': selected_month,
        'total_sales':total_sales,
    }
    return render(request, 'report/sell.html',context)


def awayaed_report(request):
    selected_month = request.GET.get('month', '')  # Get the selected filter from the form
    selected_month = request.GET.get('day', '')  # Get the selected filter from the form
    end_time = now()
    awayed = income.objects.all()

    if selected_month == 'روزانه':  
        start_time = end_time - timedelta(hours=23)
        awayed = awayed.filter(created__range=(start_time, end_time))

    elif selected_month == 'هفتگی':  
        start_time = end_time - timedelta(days=7)
        awayed = awayed.filter(created__range=(start_time, end_time))

    elif selected_month == 'ماهانه':  # Monthly
        start_time = end_time - timedelta(days=30)
        awayed = awayed.filter(created__range=(start_time, end_time))

    total_income = awayed.aggregate(total=Sum('income_amount'))['total'] or 0
    context = {
        'awayed':awayed,
        'selected_month': selected_month,
        'total_income':total_income,
    }
    return render(request, 'report/awared.html',context)
    
def masrafha(request):
    selected_month = request.GET.get('month', '')  # Get the selected filter from the form
    selected_month = request.GET.get('day', '')  # Get the selected filter from the form
    end_time = now()
    masarefat = FixedExpense.objects.all()

    if selected_month == 'روزانه':  
        start_time = end_time - timedelta(hours=23)
        masarefat = masarefat.filter(created_at__range=(start_time, end_time))

    elif selected_month == 'هفتگی':  
        start_time = end_time - timedelta(days=7)
        masarefat = masarefat.filter(created_at__range=(start_time, end_time))

    elif selected_month == 'ماهانه':  # Monthly
        start_time = end_time - timedelta(days=30)
        masarefat = masarefat.filter(created_at__range=(start_time, end_time))


    context = { 
        'masarefat':masarefat,
        'selected_month': selected_month,
    }
    return render(request, 'report/mas.html',context)


def allr(request):
    selected_month = request.GET.get('month', '')  # Get the selected filter from the form
    selected_month = request.GET.get('day', '')  # Get the selected filter from the form
    end_time = now()
    Purchases = Parchase.objects.all() 
    sells = Sale.objects.all() 
    masarefat = FixedExpense.objects.all()
    awayed = income.objects.all()

    if selected_month == 'روزانه':  
        start_time = end_time - timedelta(hours=23)
        Purchases = Purchases.filter(created_at__range=(start_time, end_time))
        sells = sells.filter(created__range=(start_time, end_time))
        masarefat = masarefat.filter(created_at__range=(start_time, end_time))
        awayed = awayed.filter(created__range=(start_time, end_time))

    elif selected_month == 'هفتگی':  
        start_time = end_time - timedelta(days=7)
        sells = sells.filter(created__range=(start_time, end_time))
        Purchases = Purchases.filter(created_at__range=(start_time, end_time))
        masarefat = masarefat.filter(created_at__range=(start_time, end_time))
        awayed = awayed.filter(created__range=(start_time, end_time))

    elif selected_month == 'ماهانه':  # Monthly
        start_time = end_time - timedelta(days=30)
        sells = sells.filter(created__range=(start_time, end_time))
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
    return render(request, 'report/allrepo.html',context)



from convertdate import persian
from datetime import date


def sell_1_month(request, slug):
    end_time = now()
    start_time = end_time - timedelta(days=30)

    try:
        customer = Customer.objects.get(slug=slug)
    except Customer.DoesNotExist:
        return HttpResponse('nothing')
    first_data = Sale.objects.filter(customer=customer).order_by('created_at').first()
    today_gregorian = date.today()

    # Convert to Shamsi (Persian/Solar Hijri) date
    today_shamsi = persian.from_gregorian(today_gregorian.year, today_gregorian.month, today_gregorian.day)

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')


        filtered_incomes = Sale.objects.filter(customer_id = customer,created_at__range=[start_date, end_date])
        total_quantity = filtered_incomes.aggregate(Sum('borrow_amount'))['borrow_amount__sum'] or 0

    
        context = {
            'end_date':end_date,
            'total_quantity':total_quantity,
            'start_date':start_date,
            'one_month': filtered_incomes,
            'filtered_incomes':filtered_incomes
        }
        return render(request, 'report/result_filteration.html', context)
    else:


        one_month = Sale.objects.filter(customer_id = customer, created_at__range=(start_time, end_time))
        total_quantity = one_month.aggregate(Sum('borrow_amount'))['borrow_amount__sum'] or 0


        context = {
            'one_month':one_month,
            'total_quantity':total_quantity,
            'customer':customer,
            'first_data':first_data,
            'today_shamsi':today_shamsi
        }

        return render(request, 'report/one_month_record.html', context)
