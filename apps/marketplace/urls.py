from django.urls import path
from . import views

# 從 proj 層級導航過來的 `marketplace` 開頭 urls 

urlpatterns = [
   path("mylists/", views.mylists, name="mylists"), 
   path("market/", views.marketplace, name="market"),  
]