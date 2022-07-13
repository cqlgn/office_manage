from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('total_table', views.total_table, name='total_table'),
    path('fine_table', views.fine_table, name='fine_table'),
    path('back_money_table', views.back_money_table, name='back_money_table'),
    path('office',views.office,name='office'),
    path('card',views.card,name='card'),
    path('benefit',views.benefit,name='benefit'),
    path('consume',views.consume,name='consume'),
    path('fine',views.fakuan,name='fine'),
    path('back_money',views.back,name='back_money'),
    path('statistic',views.statistic,name='statistic'),
    path('/statistic/',views.statistic,name='statistic'),
]
