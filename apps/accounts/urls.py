from django.urls import path, include
from . import views

# 從 proj 層級導航過來的 `accounts` 開頭 urls 

urlpatterns = [
    path('', include('django.contrib.auth.urls')), 
    path('info/', views.account_info, name='account_info')
    ]