
from django.urls import path
from.import views


app_name = 'product_and_catagory'


urlpatterns = [

    path('produce_and_cata',views.produce_and_cata, name='produce_and_cata'),
    path('delete_catagory/<int:product_id>/', views.delete_catagory_product, name='delete_catagory_product'),
    path('edit_cetagory_product/<int:id>/', views.edit_cetagory_product, name='edit_cetagory_product'),
    path('products',views.products,name='products'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),

]