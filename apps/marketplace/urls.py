from django.urls import path
from . import views
from .views import ObjektListView, CreateListView, UpdateListView, DeleteListView

# 從 proj 層級導航過來的 `marketplace` 開頭 urls 

urlpatterns = [
   path("market/", views.marketplace, name="market"), 
   path("mylists/", ObjektListView.as_view(), name="mylists"), 
   path('mylists/create/', CreateListView.as_view(), name='create_list'), 
   path('mylists/update/', UpdateListView.as_view(), name='update_list'), 
   path('mylists/delete/', DeleteListView.as_view(), name='delete_list'), 
]