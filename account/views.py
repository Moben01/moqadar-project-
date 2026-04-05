from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegistrationForm, UserEditForm, Employeement_typeForm, Employeement_InfoForm
from django.contrib import messages
from .models import Employee
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import render_to_string
# from .tokens import account_activation_token
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage
from django.contrib.auth.models import User, Group, Permission
from .models import Employee, Employeement_type, Employeement_Info
from .forms import *

from django.db import transaction
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType


ACTION_TRANSLATIONS = {
    ADDITION: "اضافه سول",
    CHANGE: "لتغییرات راوستل شو ",
    DELETION: "پاک شوی",
}
# Create your views here.

def account_register(request, id):
    url = request.META.get('HTTP_REFERER')  # get last URL

    find_emp = Employeement_Info.objects.get(id=id)
    find_name = find_emp.name
    find_email = find_emp.email
    initial_data = {
        'name': find_name,
        'email': find_email,
    }
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST, initial=initial_data)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_agree_policy = True
            user.is_active = False
            user.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Employee).pk,
                object_id=user.pk,
                object_repr=str(user),
                action_flag=ADDITION,
                change_message="د ستاسو اکونت بریالیتوب سره جور سو"
            )
            
            # Assign the selected group to the user
            # selected_group_id = registerForm.cleaned_data['group']
            # if selected_group_id:
            #     group = get_object_or_404(Group, id=selected_group_id)
            #     group.user_set.add(user)
            # login(request, user)
            messages.success(request, 'د ستاسو اکونت بریالیتوب سره جوړ سه .')
            return redirect('account:employee_info')
    else:
        registerForm = RegistrationForm(initial=initial_data)

    context = {
        'registerForm': registerForm,
        'id': id,
        'user': request.user,
    }

    return render(request, 'Home/sign_up.html', context)




@login_required
def delete_user(request):
    user = Employee.objects.get(name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse("account:dashboard"))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        
    return render(request, 'Account/user/dashboard/edit_password.html', {
        'form': form
    })



def emp_type(request):
    if request.method == "POST":

        emp_type_info = Employeement_typeForm(data=request.POST)
        if emp_type_info.is_valid():
            att_save = emp_type_info.save()
            messages.success(request, 'Your fiscal year has been Added successfully')
            return redirect('account:emp_type')

    else:
        save_emp_type = Employeement_type.objects.all()
        user_form = Employeement_typeForm()

        
        context={
            'save_emp_type':save_emp_type,
            'user_form':user_form,
        }
    return render(request, 'Account/emp_type.html', context)






def employee_info(request):
    if request.method == "POST":

        user_emp_form = Employeement_InfoForm(data=request.POST)
        if user_emp_form.is_valid():
            att_save = user_emp_form.save()
            messages.success(request, 'Your fiscal year has been Added successfully')
            return redirect('account:employee_info')

    else:
        saved_emp = Employeement_Info.objects.all()
        emp_form = Employeement_InfoForm()
        all_users = Employee.objects.all()

        
        context={
            'saved_emp':saved_emp,
            'emp_form':emp_form,
            'all_users':all_users,
        }
    return render(request, 'Account/accounts.html', context)




def delete_employee(request, employee_id):
    if request.method == "GET":
        employee = get_object_or_404(Employee, id=employee_id)
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(Employee).pk,
            object_id=employee.pk,
            object_repr=str(employee),
            action_flag=DELETION,  # Log as a deletion
            change_message="کارکونکی سیسنم نه پاک وشول"
        )
        employee.delete()
        messages.success(request, "کارمند بریالیتوب سره حذف شو.")
    return redirect('account:employee_info')



def more_information(request,id):
    
    employee_data = Employee.objects.get(id=id)
    context = {
        'employee_data':employee_data,
        'id':id,
    }
    return render (request,'Account/more_information.html',context)


def activate_employee(request, employee_id):
    url = request.META.get('HTTP_REFERER')  # get last URL

    if request.method == "GET":
        employee = get_object_or_404(Employee, id=employee_id)
        employee.is_active = True
        employee.is_staff = True
        employee.is_employee = True
        employee.save()
        LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Employee).pk,
                object_id=employee.pk,
                object_repr=str(employee),
                action_flag=ADDITION,
                change_message=" کارکونکی سیسنم کی فعال شو"
            )
        messages.success(request, "د تاسو اکونت بریالیتوب سره فعال شو .")
    return redirect(url)  


def diactivate_employee(request, employee_id):
    url = request.META.get('HTTP_REFERER')  # get last URL

    if request.method == "GET":
        employee = get_object_or_404(Employee, id=employee_id)
        employee.is_active = False
        employee.is_staff = False
        employee.is_employee = False
        employee.save()
        LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Employee).pk,
                object_id=employee.pk,
                object_repr=str(employee),
                action_flag=ADDITION,
                change_message=" کارکونکی سیسنم کی غیر فعال شو"
            )
        messages.success(request, "د تاسو اکونت په بریالیتوب سره غیر فعاله شو .")
    return redirect(url)  




@login_required
def assign_permission_for_user(request, id):
    user = get_object_or_404(Employee, id=id)
    if request.method == 'POST':
        form = UserPermissionAssignForm(request.POST)
        if form.is_valid():
            permissions = form.cleaned_data['permissions']
            user.user_permissions.set(permissions)  # Assign selected permissions to the user
            user.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(Permission).pk,
                object_id=user.pk,
                object_repr=str(user), 
                action_flag=ADDITION,
                change_message="حساب به ته بریالیتوب سره اجازه ورکول شو"  
            )  
            messages.success(request, 'کارمند ته بریالیتوب سره اجازه ورکرل شوو')
            return redirect('account:more_information' ,id=id)  # Redirect to a success page or show a success message
    else:
        form = UserPermissionAssignForm()
        context = {
            'form':form,
            'user':user,
        }
    return render(request,'Account/assign_perm copy.html',context)