from django.urls import path
from. import views



app_name ='Order'

urlpatterns = [


    path('order', views.order, name='order'),
    path('return-order/<int:sale_id>/', views.return_order, name='return_order'),
    path('Direct_sale', views.Direct_sale, name='Direct_sale'),
    path('bill_details/<int:id>/', views.bill_details, name='bill_details'),
    path('delete_sale/<int:sale_item_id>/', views.delete_sale, name='delete_sale'),
    path('delete_order/<int:id>/', views.delete_order, name='delete_order'),
    path('edit/<int:id>/', views.edit_order, name='edit_order'),
    path('edit_direct_sale/<int:id>/', views.edit_Direct_sale, name='edit_Direct_sale'),
    path('sale-details/<int:sale_id>/', views.sale_details, name='sale_details'),
    path('full-details/<int:sale_id>/', views.full_details, name='full_details'),


    path('order_loans', views.order_loans, name='order_loans'),
    path('generate_sale_item_pdf', views.generate_sale_item_pdf, name='generate_sale_item_pdf'),


]
