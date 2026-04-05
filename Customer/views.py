from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from Order.models import Order_Item, Order,Sale,sale_item_part
from .forms import *
from django.db.models import Sum,Q
from decimal import Decimal
from django.db.models import OuterRef, Subquery

from .models import *
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from django.db.models import Q, Sum
from product_and_catagory.models import *
from purchase.models import *
def customer(request):
    if request.method == 'POST':
        my_form = CustomerForm(request.POST)
        if my_form.is_valid():
            try:
                with transaction.atomic():  
                    is_supplier = request.POST.get('type', False) 
                    is_supplier = True if is_supplier == 'on' else False
                    if is_supplier:
                        customer_instance = my_form.save(commit=False)
                        customer_instance.role = 'هردو'
                    else:
                        customer_instance = my_form.save(commit=False)
                        customer_instance.role = 'مشتری'  
                    customer_instance.save()
                    messages.success(request, 'معلومات مشتری به موفقیت در سیستم ثبت شد')
                    return redirect('Customer:customer')
            except Exception as e:
                messages.error(request, f'خطای سیستمی در ثبت مشتری: {str(e)}')
                return redirect('Customer:customer')
        else:
            messages.warning(request, 'لطفا معلومات مشتری را به درستی وارد کنید')
            return redirect('Customer:customer')
    else:
        collect_all = 0
        sum_of_total_amount = 0 
        total_paid_amount = Loan.objects.filter(
            status='پرداخت شده'
        ).exclude(
            notes__isnull=True
        ).exclude(
            notes=''
        ).aggregate(
            total_amount_sum=Sum('amount')
        )['total_amount_sum'] or 0
     

        sum_of_all_sale = sale_item_part.objects.all()
        total_paid_amoun = sum_of_all_sale.aggregate(total=Sum('paid_amount_for_every_record'))['total']
        
        find_paid_amounts_that_paid_by_sale = Loan.objects.filter(status='پرداخت نه شده',sale_id=None).aggregate(total_amount=Sum('amount'))['total_amount']
        collect_all = (total_paid_amoun or 0) + (total_paid_amount or 0) + (find_paid_amounts_that_paid_by_sale or 0)
      


        latest_loans = Loan.objects.filter(customer=OuterRef('customer')).order_by('-created').values('id')[:1]
        loans_with_latest = Loan.objects.filter(id__in=Subquery(latest_loans))
        total_sum = loans_with_latest.aggregate(total_amount_sum=Sum('total_amount'))['total_amount_sum'] or 0  




        latest_loans = Loan.objects.filter(customer_id=OuterRef('id')).order_by('-id')
        my_data = Customer.objects.filter(role__in=['مشتری', 'هردو']).annotate(
            total_borrow=Subquery(latest_loans.values('total_amount')[:1])
        )

        for cus in my_data:
            id = cus.id
            deals = item_deals.objects.filter(dealer=id)
            product_ids = deals.values_list('item', flat=True).distinct()

            product_summaries = []
            cus.msg=False

            for pid in product_ids:
                product_obj = product.objects.get(id=pid)
                product_name = product_obj.meat_name  

                recv = deals.filter(item=pid, status='رسید')
                give = deals.filter(item=pid, status='برداشت')

                total_recv_num = recv.aggregate(total=Sum('number'))['total'] or 0
                total_recv_weight = recv.aggregate(total=Sum('weighht'))['total'] or 0

                total_give_num = give.aggregate(total=Sum('number'))['total'] or 0
                total_give_weight = give.aggregate(total=Sum('weighht'))['total'] or 0
                
                
                if total_recv_weight > total_give_weight:
                    cus.msg=True
                else:
                    cus.msg=True
            
            

        my_form = CustomerForm()
     
        context = {
            'total_sum':total_sum,
            'collect_all':collect_all,
            'my_form': my_form,
            'my_data': my_data,
        
        }
    return render(request, 'customer/customer.html', context)

def loan_people(request):
    all_customer = Customer.objects.filter(role='مشتری')
    loan_data = []
    for c in all_customer:
        find_loan_record = Loan.objects.filter(customer=c).last()
        if find_loan_record:
            if find_loan_record.total_amount > 0:
                loan_data.append({
                    'name':c.name,
                    'loan_amount':find_loan_record.total_amount if find_loan_record else 0,
                })
            else:
                pass
        else:
            pass

    context = {
        'loan_data':loan_data,
    }
    return render(request, 'customer/loan_people.html',context)


def loan_people_print(request):
    all_customer = Customer.objects.filter(role='مشتری')
    loan_data = []

    for c in all_customer:
        find_loan_record = Loan.objects.filter(
            customer=c,
            total_amount__gt=0
        ).last()
        
        if find_loan_record:
            loan_data.append({
                'name':c.name,
                'loan_amount':find_loan_record.total_amount if find_loan_record else 0,
            })
        else:
            pass


    context = {
        'loan_data': loan_data,
    }

    return render(request, 'customer/loan_people_print.html', context)






def delete_customer(request, customer_id):
    # Fetch the Purchase object or return a 404 error
    Purchase_instance = get_object_or_404(Customer, id=customer_id)
    
    # Delete the object 
    Purchase_instance.delete()
    messages.success(request, 'مشتری شما موفقانه حذف شد ')
    return redirect('Customer:customer')  # Redirect to the main Purchase page


def edit_customer(request, id):
    if request.method == "POST":
        edit_daily_project_task = Customer.objects.get(pk=id)
        edit_daily_project_form = CustomerForm(instance=edit_daily_project_task, data=request.POST)
        if edit_daily_project_form.is_valid():
            edit_daily_project_form.save()
            messages.success(request, ' تغییرات در مشتری ذیل موفقانه انجام پذیرفت')
            id = id
            return HttpResponseRedirect(reverse("Customer:customer"))
    else:
        id = id
        edit_daily_project_task = Customer.objects.get(pk=id)
        edit_daily_project_form = CustomerForm(instance=edit_daily_project_task)
        context = {
            # 'attendance': attendance,
            'edit_daily_project_form': edit_daily_project_form,
            'id':id,
        }
        return render(request, "customer/edit_customer.html", context)


    
def customer_order_detail(request, slug):
    # Get the specific customer
    try:
        customer = Customer.objects.get(slug=slug)
    except Customer.DoesNotExist:
        return HttpResponse("Customer not found.")

    # Handle status update
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("status")

        try:
            # Get the order based on order_id and customer
            order = Order.objects.get(id=order_id, customer=customer)

            # Check if the status is changing
            previous_status = order.status
            order.status = new_status
            order.save()

            # Update the total_amount based on the status
            order_items = Order_Item.objects.filter(order=order)

            if new_status == 'complete' and previous_status != 'complete':
                # Recalculate total_amount for each item when status becomes 'complete'
                for item in order_items:
                    item.total_amount = item.quantity * item.price_per_unit
                    item.save()
            elif new_status != 'complete':
                # Set total_amount to 0 when status is not 'complete'
                for item in order_items:
                    item.total_amount = 0
                    item.save()

            messages.success(request, "وضعیت سفارش با موفقیت بروزرسانی شد.")
        except Order.DoesNotExist:
            messages.error(request, "سفارش برای این مشتری یافت نشد.")

        return redirect("Customer:customer_order_detail", slug=slug)

    # Get all orders for this customer
    customer_orders = Order.objects.filter(customer=customer)

    # Get all order items for this customer's orders
    customer_order_items = Order_Item.objects.filter(order__in=customer_orders)

    context = {
        'customer': customer,
        'customer_orders': customer_orders,
        'customer_order_items': customer_order_items,
    }

    return render(request, 'customer/customer_order_detail.html', context)




def customer_full_info(request, id):
    customer = Customer.objects.get(id=id) 
    filer_records = sale_item_part.objects.filter(sell_forei__customer__id=id)
    customer_loan = Loan.objects.filter(customer_id=id)
    sale_ids = customer_loan.values_list('sale_id', flat=True)

   
    total_sale_amount = sale_item_part.objects.filter(id__in=sale_ids).aggregate(
        paid_amount_for_every_record_sum=Sum('paid_amount_for_every_record') 
    )['paid_amount_for_every_record_sum']or 0


    customer_loan_with_notes_sum = Loan.objects.filter(
        customer_id=id,
        status='پرداخت شده'
    ).exclude(
        notes__isnull=True 
    ).exclude(
        notes='' 
    ).aggregate(
        total_amount_sum=Sum('amount')
    )['total_amount_sum'] or 0
    

    find_paid_with_sale = Loan.objects.filter(status='پرداخت نه شده',customer_id=id,sale_id=None).aggregate(paid=Sum('amount'))['paid'] or 0
    given_money = round(total_sale_amount + customer_loan_with_notes_sum + find_paid_with_sale)

    latest_unpaid_loan = Loan.objects.filter(customer_id=customer.id).order_by('-id').first()
    total_borrow = Loan.objects.filter(customer_id=id).last()
    total_reamin = round(total_borrow.total_amount)

 
    last_record = 0
    if sale_item_part.objects.filter(sell_forei__customer__id=id).exists():
        last_record = sale_item_part.objects.filter(sell_forei__customer__id=id).latest('product')
    total_paid = sale_item_part.objects.filter(sell_forei__customer__id=id).aggregate(should_paid=Sum('should_paid'))['should_paid']

    product_sold = []
    all_products = product.objects.all()
    for i in all_products:
        product_id = i.id 
        find_all_sale_q = sale_item_part.objects.filter(product=product_id,sell_forei__customer=id).aggregate(total_quantity_in_sale=Sum('quantity'))
        sold_quantity = find_all_sale_q['total_quantity_in_sale'] or 0

        find_all_sale_weight = sale_item_part.objects.filter(product=product_id,sell_forei__customer=id).aggregate(total_weight_in_sale=Sum('weight'))
        sold_weight = find_all_sale_weight['total_weight_in_sale'] or 0
        product_sold.append({
            'P_id':product_id,
            'p_name':i.meat_name,
            'sold_q':sold_quantity,
            'sold_w':sold_weight,
        })


    context = {
        'customer': customer,
        'product_sold':product_sold,
        'filer_records':filer_records,
        'total_reamin':total_reamin,
        'given_money':given_money,
        'last_record':last_record,
        'total_paid':total_paid,
    }
    return render(request, 'customer/customer_full_info.html', context)

def delete_paid_record_od_cudtomer(request,id):
    find_total_money_in_system = total_balance.objects.last()
    find_total = Decimal(find_total_money_in_system.total_money_in_system)
    
    find_record =  Loan.objects.filter(id=id).last()
    find_amount = find_record.amount
    find_user = find_record.customer.id
    
    find_last_record = Loan.objects.filter(customer=find_user).last()
    last_total_amount = find_last_record.total_amount
    sum_t = last_total_amount + find_amount
    find_last_record.total_amount = sum_t
    find_last_record.save() 
    try:
        find_delete_record = find_record.sale_id_to_find_the_deletion.id
        find_sale_record = sale_item_part.objects.filter(id=find_delete_record).last()
        find_sale_record.reamin_amount_according_to_sale_record = find_amount
        find_sale_record.is_money_approved = False
        
        find_sale_record.save()
    except:
        pass
    

    find_total_money_in_system.total_money_in_system -= Decimal(find_amount)
    find_total_money_in_system.save()
    
    find_record.delete()
    messages.success(request, 'ریکارد موفقانه حذف شد ')
    return redirect(request.META.get('HTTP_REFERER', '/'))




def customer_loans(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer_loan = Loan.objects.filter(customer_id=id).order_by('id')
    sale_ids = customer_loan.values_list('sale_id', flat=True)
    total_sale_amount = sale_item_part.objects.filter(id__in=sale_ids).aggregate(
        paid_amount_for_every_record_sum=Sum('paid_amount_for_every_record') 
    )['paid_amount_for_every_record_sum']or 0


    customer_loan_with_notes_sum = Loan.objects.filter(
        customer_id=id,
        status='پرداخت شده'
    ).exclude(
        notes__isnull=True  
    ).exclude(
        notes=''  
    ).aggregate(
        total_amount_sum=Sum('amount')
    )['total_amount_sum'] or 0

    find_all_total_sale_amount = round(total_sale_amount + customer_loan_with_notes_sum)

    latest_unpaid_loan = Loan.objects.filter(customer_id=customer.id).order_by('-id').first()
    total_borrow = Loan.objects.filter(customer_id=id).last()
    total_borrow_amount = round(total_borrow.total_amount)

    if not latest_unpaid_loan:
        latest_unpaid_loan = 0
    else:
        latest_unpaid_loan = Decimal(latest_unpaid_loan.total_amount)
    latest_paid_loan = Loan.objects.filter(customer_id=customer.id, status='پرداخت شده').order_by('-id').first()

    if not latest_paid_loan:
        latest_paid_loan = 0
    else:
        latest_paid_loan = Decimal(latest_paid_loan.total_amount)
    context = {
        'customer': customer,
        'customer_loan':customer_loan,
        'find_all_total_sale_amount':find_all_total_sale_amount,
        'total_borrow_amount':total_borrow_amount,
     
    }
    return render(request, 'customer/customer_loans.html', context)


from Finance_and_Accounting.models import *



def paid_customer_loans(request, id):
    customer = get_object_or_404(Customer, id=id)
    system_all_money = total_balance.objects.first()
    first_record = system_all_money.total_money_in_system


    latest_unpaid_loan = Loan.objects.filter(customer_id=customer.id).order_by('-id').first()
    find_total_ammoun = latest_unpaid_loan.total_amount


    if request.method == "POST":
        paid_amount = request.POST.get("amount")
        find_current_balance = float(find_total_ammoun) - float(paid_amount)


        loan_form = LoanForm(request.POST)
        if loan_form.is_valid():
            # Create a new loan entry based on form data
            new_loan = loan_form.save(commit=False)
            new_loan.customer = customer
            new_loan.total_amount = find_current_balance
              # Link the loan to the current customer
            new_loan.status = 'پرداخت شده'
            sum_with_total = first_record + Decimal(paid_amount)
            system_all_money.total_money_in_system = sum_with_total
            system_all_money.save()

            new_loan.save()

            # Optionally update the status of unpaid loans to 'پرداخت شده'
            messages.success(request, "پول قرض په موفقیت پرداخت شد.")
            return redirect('Customer:customer_loans', id=id)  # Redirect to a relevant page
        else:
            messages.error(request, "مشکلی موجود است به موفقیت پرداخت نه شد.")
    else:
        # If GET request, create an empty form
        loan_form = LoanForm()    
        context = {
            'customer': customer,
            'loan_form':loan_form,
            'amount':find_total_ammoun,
        }
        return render(request, 'customer/paid_customer_loans.html', context)



def paid_with_sale(request, id):
    customer_id = id
    customer = get_object_or_404(Customer, id=id)
    system_all_money = total_balance.objects.first()
    first_record = system_all_money.total_money_in_system

    latest_unpaid_loan = Loan.objects.filter(customer_id=customer.id).order_by('-id').first()
    find_total_ammoun = latest_unpaid_loan.total_amount
    

    if request.method == "POST":
        paid_amount = request.POST.get("amount")
        find_current_balance = float(find_total_ammoun) - float(paid_amount)
        loan_form = LoansaleForm(request.POST, customer_id=customer_id)
        if loan_form.is_valid():
            new_loan = loan_form.save(commit=False)
            all_money_of_remain_amount = 0
            for item in loan_form.cleaned_data['sale_id_for_pay']:
                item = sale_item_part.objects.get(id=item.id)
                find_borrow_amount = item.reamin_amount_according_to_sale_record
                all_money_of_remain_amount += find_borrow_amount
            if float(all_money_of_remain_amount) == float(paid_amount):  
                  
                new_loan.customer = customer
                new_loan.total_amount = find_current_balance
                new_loan.status = 'پرداخت شده'
                new_loan.sale_id_to_find_the_deletion = item
                
                sum_with_total = first_record + Decimal(paid_amount)
                system_all_money.total_money_in_system = sum_with_total
                system_all_money.save() 
                new_loan.save() 
                for items in loan_form.cleaned_data['sale_id_for_pay']: 
                    item = sale_item_part.objects.get(id=items.id)                    
                    item.reamin_amount_according_to_sale_record = 0
                    
                    item.save()
                messages.success(request, "پول قرض په موفقیت پرداخت شد.")
                return redirect('Customer:customer_loans', id=id)
            else:
                
                if float(paid_amount) > float(all_money_of_remain_amount):
                    messages.success(request, f"پول پرداختی بیشتر از مجموعه پول است.")
                    return redirect('Customer:customer_loans', id=id)
                else:
                    new_loan.customer = customer
                    new_loan.total_amount = find_current_balance
                    new_loan.status = 'پرداخت نه شده'
                    new_loan.sale_id_to_find_the_deletion = item
                    
                    sum_with_total = first_record + Decimal(paid_amount)
                    system_all_money.total_money_in_system = sum_with_total
                    system_all_money.save() 
                    new_loan.save() 
                    for item in loan_form.cleaned_data['sale_id_for_pay']:
                        item = sale_item_part.objects.get(id=item.id) 
                        find_item_reamin = item.reamin_amount_according_to_sale_record - float(paid_amount)
                        item.reamin_amount_according_to_sale_record = find_item_reamin
                        item.save()
                messages.success(request, f"پول قرض په موفقیت پرداخت شد.")
                return redirect('Customer:customer_loans', id=id)
        else:
            messages.error(request, "مشکلی موجود است به موفقیت پرداخت نه شد.")
    else:
        loan_form = LoansaleForm(customer_id=customer_id)    
        context = {
            'customer': customer,
            'loan_form':loan_form,
            'amount':find_total_ammoun,
        }
        return render(request, 'customer/pais_with_sale.html', context) 
    



def customer_paid_loans(request, id):
    customer = get_object_or_404(Customer, id=id)

    latest_unpaid_loan = Loan.objects.filter(customer_id=customer.id, status ='پرداخت شده')
    context = {
            'customer': customer,
            'latest_unpaid_loan':latest_unpaid_loan,
            
        }
    return render(request, 'supplaier/supplaier_paid_loans.html', context)

