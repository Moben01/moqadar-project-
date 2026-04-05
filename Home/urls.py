from django.contrib import admin
from django.urls import path
from Home import views
from django.contrib.auth import views as auth_views
from account.forms import (UserLoginForm)
from django.contrib.auth.views import LogoutView 


app_name ='Home'

urlpatterns = [

    path('', auth_views.LoginView.as_view(template_name='Home/index.html',
                                                form_class=UserLoginForm), name='login'),
    path('dashboard', views.dashboard, name='dashboard'), 
    path('logout/', LogoutView.as_view(next_page='/account/login/'),name='logout'),
    path('backup', views.backup, name='backup'), 




]
