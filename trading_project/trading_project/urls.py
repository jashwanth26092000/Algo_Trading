# trading_project/urls.py
from django.contrib import admin
from django.urls import path,include
from trading_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('run_backtest/', views.run_backtest, name='run_backtest'),
    path('trades/', views.trades_list, name='trades_list'),
    path('options_calculator/',include('option_calculator.urls')),
]
