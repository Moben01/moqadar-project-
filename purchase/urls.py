
from django.urls import path
from . import views



app_name ='purchase'

urlpatterns = [
    path('purchase', views.Purchase, name='purchase'),
    path('loan', views.loan, name='loan'),
    path('delete/<int:id>/', views.delete_Purchase, name='delete_purchase'),
    path('edit_purchase/<int:purchase_id>/', views.edit_purchase, name='edit_purchase'),
    path('log_in_our_system', views.log_in_our_system, name='log_in_our_system'),
    path('purhase_with_item/<int:id>/', views.purhase_with_item, name='purhase_with_item'),
    path('reciving_item/<int:id>/', views.reciving_item, name='reciving_item'),
    path('giving_item/<int:id>/', views.giving_item, name='giving_item'),
    path('delete_item_deal/<int:id>/', views.delete_item_deal, name='delete_item_deal'),
    path('purchase/pdf/<int:id>/', views.purchase_with_item_pdf, name='purchase_with_item_pdf'),



]