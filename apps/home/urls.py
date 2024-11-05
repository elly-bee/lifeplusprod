# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views as home_views

app_name = 'apps_home'
urlpatterns = [
    # The home page DashboardBonus post_transaction
    path('', home_views.index, name='index'),
    path('dashboard', home_views.Dashboard.as_view(), name='dashboard'), 
    path('DashboardBonus', home_views.DashboardBonus.as_view(), name='DashboardBonus'),
    path('DashboardOrder', home_views.DashboardOrder.as_view(), name='DashboardOrder'),  
    path('DashboardTransactions', home_views.DashboardTransactions.as_view(), name='DashboardTransactions'),
    path('test1/', home_views.test1, name='test'), 
    path('post_transaction/', home_views.post_transaction, name='post_transaction'), 
    path('test/<int:max_depth>/', home_views.process_and_hierarchies, name='test'), 
    path('process-weekend/', home_views.post_weekend_transaction, name='process_weekend'),
    path('Registration', home_views.create_user, name='Registration'), # Using the 'index' function from the 'home' views
    path('products', home_views.ProductView.as_view(), name='products'),
    path('user_create_info/<int:pk>/', home_views.create_user_details, name='user_create_info'),
    path('user_detail', home_views.user_detail, name='user_detail'),
    path('product_detail/<int:pk>', home_views.ProductDetials.as_view(), name='product_detail'),
    path('client_product_detail/<int:pk>', home_views.ClientProductDetail.as_view(), name='client_ProDetail'),
    path('transactionDetail/<int:pk>/', home_views.TransactionDetail.as_view(), name='transactionDetail'),
    path('get_current_balance/<int:acc_type_id>/', home_views.get_current_balance, name='get_current_balance'),
    path('fund_account', home_views.FundTransfer.as_view(), name='fund_account'),
]