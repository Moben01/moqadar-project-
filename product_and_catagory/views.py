from django.shortcuts import render,redirect, get_object_or_404
from django.shortcuts import HttpResponse , render
from .forms import *
from django.contrib import messages
from .models import *
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
# Create your views here.

def produce_and_cata(request):
    if request.method == 'POST':
        my_form = catagoriesForm(request.POST)
        try:
            with transaction.atomic():
                
                if my_form.is_valid():
                    my_form.save()
                    messages.success(request, 'نوعیت محصول موفقانه ثبت شد')
                    return redirect('product_and_catagory:produce_and_cata')
                else:
                    messages.warning(request, 'مشکل موجود بوده نوعیت محصول ثبت نشد')
                    return redirect('product_and_catagory:produce_and_cata')
        except Exception as e:
            messages.error(request, f'خطای سیستمی در ثبت نوعیت محصول: {str(e)}')
            return redirect('product_and_catagory:produce_and_cata')
    else:
        my_data = catagories.objects.all()
        my_form = catagoriesForm()
        context = {
            'my_form':my_form,
            'my_data':my_data,
        }
    return render (request,'product_and_catago/catagory.html',context)




def delete_catagory_product(request, product_id):
    # Fetch the Purchase object or return a 404 error
    Purchase_instance = get_object_or_404(catagories, id=product_id)
    
    # Delete the object
    Purchase_instance.delete()
    messages.success(request, 'محصول موفقانه حذف شد')
    return redirect('product_and_catagory:produce_and_cata')  # Redirect to the main Purchase page


def edit_cetagory_product(request, id):
    if request.method == "POST":
        edit_daily_project_task = catagories.objects.get(pk=id)
        edit_daily_project_form = catagoriesForm(instance=edit_daily_project_task, data=request.POST)
        if edit_daily_project_form.is_valid():
            edit_daily_project_form.save()
            messages.success(request, ' تغییرات در ریکورد موفقانه انجام پذیرفت')
            id = id
            return HttpResponseRedirect(reverse("product_and_catagory:produce_and_cata"))
    else:
        id = id
        edit_daily_project_task = catagories.objects.get(pk=id)
        edit_daily_project_form = catagoriesForm(instance=edit_daily_project_task)
        context = {
            # 'attendance': attendance,
            'edit_daily_project_form': edit_daily_project_form,
            'id':id,
        }
        return render(request, "product_and_catago/catagory.html", context)



def products(request):
    if request.method == 'POST':
        my_form = productForm(request.POST)
        try:
            with transaction.atomic(): 
                if my_form.is_valid():
                    my_form.save() 
                    messages.success(request, 'محصول موفقانه ثبت شد')
                    return redirect('product_and_catagory:products')
                else:
                    messages.warning(request, 'مشکل موجود بوده محصول ثبت نشد')
                    return redirect('product_and_catagory:products')
        
        except Exception as e:
            messages.error(request, f'خطای سیستمی در ثبت محصول: {str(e)}')
            return redirect('product_and_catagory:products')
    else:
        my_data = product.objects.all()
        my_form = productForm()
        context = {
            'my_form':my_form,
            'my_data':my_data,
        }
    return render(request,'product_and_catago/product.html',context)



def delete_product(request, product_id):
    # Fetch the Purchase object or return a 404 error
    Purchase_instance = get_object_or_404(product, id=product_id)
    
    # Delete the object
    Purchase_instance.delete()
    messages.success(request, 'محصول موفقانه حذف شد')
    return redirect('product_and_catagory:products')  # Redirect to the main Purchase page



def edit_product(request, id):
    if request.method == "POST":
        edit_daily_project_task = product.objects.get(pk=id)
        edit_daily_project_form = productForm(instance=edit_daily_project_task, data=request.POST)
        if edit_daily_project_form.is_valid():
            edit_daily_project_form.save()
            messages.success(request, ' تغییرات در ریکورد موفقانه انجام پذیرفت')
            id = id
            return HttpResponseRedirect(reverse("product_and_catagory:products"))
    else:
        id = id
        edit_daily_project_task = product.objects.get(pk=id)
        edit_daily_project_form = productForm(instance=edit_daily_project_task)
        context = {
            # 'attendance': attendance,
            'edit_daily_project_form': edit_daily_project_form,
            'id':id,
        }
        return render(request, "product_and_catago/Edit/edit_product.html", context)
