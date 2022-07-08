from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('office',views.office,name='office'),
    path('card',views.card,name='card'),
    path('benefit',views.benefit,name='benefit'),
]
