from django.urls import path
from . import views



app_name ='Supplaier'

urlpatterns = [
    path('supplaier', views.supplaier, name='supplaier'),
    path('delete/<int:id>/', views.delete_supplaier, name='delete_supplaier'),
    path('edit/<int:id>/', views.edit_supplaier, name='edit_supplaier'),
    path('supplaer_info/<int:id>/', views.supplaer_info, name='supplaer_info'),
    path('supp_loans/<int:id>/', views.supp_loans, name='supp_loans'),
    # path('paind_supp_loans/<int:id>/', views.paid_customer_loans, name='paind_customer_loans'),
    # path('supp_paid_loans/<int:id>/', views.customer_paid_loans, name='customer_paid_loans'),
    path('paid_supp_loans/<int:id>/', views.paid_supp_loans, name='paid_supp_loans'),
    path('supp_paid_loans/<int:id>/', views.supp_paid_loans, name='supp_paid_loans'),
    path('delete_paid_record/<int:id>/', views.delete_paid_record, name='delete_paid_record'),


]
