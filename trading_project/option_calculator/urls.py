from django.urls import path,include
from option_calculator import views

urlpatterns = [
    path('', views.calculate,name ='calculator'),
]