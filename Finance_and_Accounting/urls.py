from django.urls import path
from.import views


app_name = 'Finance_and_Accounting'

urlpatterns = [

    path('malle_wa_mahaseba',views.malle_wa_mahaseba,name='malle_wa_mahaseba'),
    path('collaborates',views.collaborates,name='collaborates'),
    path('edit_collaborators/<int:id>/', views.edit_collaborators, name='edit_collaborators'),
    path('delete_collaborators/<int:id>/', views.delete_collaborators, name='delete_collaborators'),
    path('partners_loan_amount/', views.partners_loan_amount, name='partners_loan_amount'),
    path('loan_collaborate_partners/', views.loan_collaborate_partners, name='loan_collaborate_partners'),
    


    path('col_balance/<int:id>/', views.col_balance, name='col_balance'),
    path('edit_col_balance/<int:id>', views.edit_col_balance, name='edit_col_balance'),
    path('delete_col_balance/<int:id>', views.delete_col_balance, name='delete_col_balance'),
    path('generate_pdf/<int:id>/', views.generate_pdf, name='generate_pdf'),
    path('currency/', views.currency, name='currency'),
    path('find_folar_records/<int:id>/', views.find_folar_records, name='find_folar_records'),
    path('all_records/<int:id>/', views.all_records, name='all_records'),
    path('edit_financial_record/<int:record_id>/', views.edit_financial_record, name='edit_financial_record'),
    path('exchang_money/',views.exchang_money,name='exchang_money'),




]