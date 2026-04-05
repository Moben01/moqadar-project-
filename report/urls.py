
from.import views
from django.urls import path


app_name = 'report'

urlpatterns = [


    path('reports', views.reports, name='reports'),
    path('sell_report', views.sell_report, name='sell_report'),
    path('awayaed_report', views.awayaed_report, name='awayaed_report'),
    path('masrafha', views.masrafha, name='masrafha'),
    path('allr', views.allr, name='allr'),
    path('sell_1_month/<slug:slug>/', views.sell_1_month, name='sell_1_month'),


]