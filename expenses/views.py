from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from django.utils.timezone import now
from django.db.models import Sum
from Finance_and_Accounting.models import total_balance
from .models import *
from datetime import datetime, timedelta
from decimal import Decimal


from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.staticfiles.storage import staticfiles_storage
import os
import arabic_reshaper
from bidi.algorithm import get_display

def main_expenses(request):
    
    selected_month = request.GET.get('month', '')
    selected_month = request.GET.get('day', '')
    end_time = now()
    my_data = FixedExpense.objects.all()
    if selected_month == 'روزانه':  # Daily
        start_time = end_time - timedelta(hours=23)
        my_data = my_data.filter(created_at__range=(start_time, end_time))
    elif selected_month == 'هفتگی':  # Weekly
        start_time = end_time - timedelta(days=7)
        my_data = my_data.filter(created_at__range=(start_time, end_time))
    elif selected_month == 'ماهانه':  # Monthly
        start_time = end_time - timedelta(days=30)
        my_data = my_data.filter(created_at__range=(start_time, end_time))
    has_expenses = FixedExpense.objects.exists()
    total_expenses = LoanApprove.objects.aggregate(total=Sum('amounta'))['total'] if has_expenses else 0 
    if request.method == 'POST':
        my_form = FixedExpenseForm(request.POST)
        if my_form.is_valid():
            Purchase_instance = my_form.save(commit=False)
            amount = my_form.cleaned_data.get('amount')
            try:
                total_balances = total_balance.objects.first()
                if total_balances and amount is not None:
                    if amount <= total_balances.total_money_in_system:
                        total_balances.total_money_in_system -= amount
                        total_balances.save()
                        Purchase_instance.reamin_amonts = 0
                        messages.success(request, f"مقدار {amount} با موفقیت کسر شد. موجودی جدید: {total_balances.total_money_in_system}")

                        my_form.save()
                        product = Purchase_instance
                        warehouse = Purchase_instance.date
                        quantity = Purchase_instance.description
                        new_record  = LoanApprove.objects.create(expenses_foriengkey=product,amounta=amount,datea=warehouse,descriptiona=quantity)

                        messages.success(request, ' مصرف موفقانه ثبت شد')
                        return redirect('expenses:main_expenses')
                    else:
                        messages.warning(request, "خطا: مقدار وارد شده بیشتر از موجودی کل سیستم است. لطفاً مقدار کمتری وارد کنید.")
                else:
                    messages.error(request, "خطا: موجودی کل تنظیم نشده است یا مقدار وارد شده نامعتبر است.")
            except total_balance.DoesNotExist:
                messages.error(request, "خطا: رکوردی برای موجودی کل سیستم وجود ندارد.")
        else:

            messages.warning(request, 'مشکل موجود بوده نوعیت گوشت ثبت نشد')

    else:
        my_form = FixedExpenseForm()

    my_data = FixedExpense.objects.all()
    find_all_sale_money = FixedExpense.objects.aggregate(total_should_paid=Sum('total_amount'))

    total_should_paid = find_all_sale_money['total_should_paid'] or 0
    context = {
        'my_form': my_form,
        'total_expenses':total_expenses,
        'has_expenses':has_expenses,
        'selected_month':selected_month,
        'my_data':my_data,
        'total_should_paid':total_should_paid,
    }

    return render(request, 'expenses/main_expenses.html', context)

def reshape_text(text):
    """Reshape Persian text for correct display in PDF"""
    return get_display(arabic_reshaper.reshape(text))


def generate_ecpenses_pdf(request):
    """Generate a PDF report for all sale_item_part records"""
    all_sales = FixedExpense.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expenses.pdf"'
    font_path = staticfiles_storage.path('fonts/Amiri-Regular.ttf')  # Path to the font file
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Amiri', font_path))
        font_name = 'Amiri'
    else:
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
        font_name = 'Arial'
    doc = SimpleDocTemplate(response, pagesize=landscape(A4))  # Use landscape mode
    elements = []

    # Define custom Persian/Arabic text style
    styles = getSampleStyleSheet()
    persian_style = ParagraphStyle(
        name='PersianStyle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=12,
        alignment=1,  # Center alignment
    )
    title_text = "لیست PDF شده همه مصارفات"
    title = Paragraph(reshape_text(title_text), persian_style)
    elements.append(title)
    elements.append(Spacer(1, 20))  # Add space after the title
    headers = [
        reshape_text("توضیحات"),
        reshape_text("تاریخ"), 
        reshape_text("مقدار باقی"), 
        reshape_text("مقدار"), 
        reshape_text("اسم"), 
        reshape_text("شماره"),

    ]
    data = [headers]
    for order in all_sales:
        data.append([
            str(order.description),
            str(order.date),
            str(order.reamin_amonts),
            str(order.amount),
            str(order.name),
            str(order.id),
        ])
    PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)
    total_columns = len(headers)
    col_width = PAGE_WIDTH / total_columns  # Equal column width
    col_widths = [col_width] * total_columns

    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, 0), font_name),  # Header font
        ('FONTNAME', (0, 1), (-1, -1), font_name),  # Data font
        ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Data row background color
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))  # Add space after the table

    # Build the PDF
    doc.build(elements)
    return response









def give_loan(request, id):
    find_records = get_object_or_404(FixedExpense, id=id)
    find_reamin_amount = find_records.reamin_amonts
    name = find_records.name
    if request.method == 'POST':
        my_form = LoanApproveForm(request.POST)
        if my_form.is_valid():
            paid_ammount = my_form.cleaned_data['amounta']
            mines_from_expenses = find_reamin_amount - paid_ammount
            find_records.reamin_amonts = mines_from_expenses
            total_amount = total_balance.objects.first()
            if total_amount:
                find_total = total_amount.total_money_in_system
                total_balance_all = Decimal(find_total) - Decimal(paid_ammount)
                total_amount.total_money_in_system = total_balance_all
                total_amount.save()
            find_records.save()
            loan_approve = my_form.save(commit=False)
            loan_approve.expenses_foriengkey = find_records
            loan_approve.save()
            messages.success(request, 'قرض شما به موفقیت اجرا شد')
            return redirect('expenses:give_loan', id=id)
        else:
            messages.warning(request, 'خطا: فرم معتبر نیست. لطفاً دوباره بررسی کنید.')
            return redirect('expenses:give_loan', id=id)
    else:
        total_expenses = LoanApprove.objects.filter(expenses_foriengkey=id).aggregate(total=Sum('amounta'))['total']
        

        my_data = LoanApprove.objects.filter(expenses_foriengkey=id)
        my_form = LoanApproveForm(initial={'amounta': find_reamin_amount})
        context = {
            'my_data': my_data,
            'name': name,
            'total_expenses': total_expenses,
            'my_form': my_form,
            'find_reamin_amount':find_reamin_amount,
        }
        return render(request, 'expenses/loan.html', context)



def delete_main_expenses(request, id):
    Purchase_instance = get_object_or_404(FixedExpense, id=id)
    find_the_total_amount = Purchase_instance.total_amount
    my_data = total_balance.objects.first()
    my_data.total_money_in_system += find_the_total_amount
    my_data.save()
    Purchase_instance.delete()
    messages.success(request, 'ریکارد مصرف خویش را موفقانه حذف کردید ')
    return redirect('expenses:main_expenses') 


def edit_main_expenses(request, id):
    if request.method == "POST":
        edit_daily_project_task = FixedExpense.objects.get(pk=id)
        edit_daily_project_form = FixedExpenseForm(instance=edit_daily_project_task, data=request.POST)
        if edit_daily_project_form.is_valid():
            edit_daily_project_form.save()
            messages.success(request, ' تغییرات در مشتری ذیل موفقانه انجام پذیرفت')
            id = id
            return HttpResponseRedirect(reverse("expenses:main_expenses"))
    else:
        id = id
        edit_daily_project_task = FixedExpense.objects.get(pk=id)
        edit_daily_project_form = FixedExpenseForm(instance=edit_daily_project_task)
        context = {
            # 'attendance': attendance,
            'edit_daily_project_form': edit_daily_project_form,
            'id':id,
        }
        return render(request, "expenses/edit_expenses.html", context)
