from django.shortcuts import render  # 把 data 和 html template 結合
from .models import ObjektCard  # 從 models.py 匯入資料表

# views
# 接收 request → 取得資料 models → 把資料丟給 template → render 渲染產生 HTML → 回傳給瀏覽器

def all_card_list(request):
    # 取出所有資料(前50) 先查詢好 FK
    qs = ObjektCard.objects.select_related('artist', 'member', 'season', 'objekt_class', 'collection').all()[:50]
    return render(request, template_name='object/list.html', context={'cards': qs})

