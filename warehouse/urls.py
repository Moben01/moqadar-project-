
from.import views
from django.urls import path
app_name ='warehouse'

urlpatterns = [

    path('warehouse_part',views.warehouse_part,name='warehouse_part'),
    path('delete/<int:id>/', views.delete_warehouse, name='delete_warehouse'),
    path('edit/<int:id>/', views.edit_warehouse, name='edit_warehouse'),
    path('ware_data/<int:id>/', views.ware_data, name='ware_data'),
    path('transfer_pro_to_godams/',views.transfer_pro_to_godams,name='transfer_pro_to_godams'),



]