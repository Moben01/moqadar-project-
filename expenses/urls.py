from django.urls import path
from . import views



app_name ='expenses'

urlpatterns = [

    path('main_expenses', views.main_expenses, name='main_expenses'),   
    path('delete/<int:id>/', views.delete_main_expenses, name='delete_main_expenses'),
    path('edit/<int:id>/', views.edit_main_expenses, name='edit_main_expenses'),
    path('give_loan/<int:id>/', views.give_loan, name='give_loan'),
    path('generate_ecpenses_pdf', views.generate_ecpenses_pdf, name='generate_ecpenses_pdf'),


]
