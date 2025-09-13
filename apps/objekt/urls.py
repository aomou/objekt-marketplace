from django.urls import path
from . import views

# 從 proj 層級導航過來的 `objekt` 開頭 urls 

urlpatterns = [
    path("card/", views.filtered_objekt_type, name="card_list"),  # 先預留
]