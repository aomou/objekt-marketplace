from django.shortcuts import render  # 把 data 和 html template 結合
from .models import ObjektType  # 從 models.py 匯入資料表
from .filters import ObjektTypeFilter
from .utils import get_ordering


# views
# 接收 request → 取得資料 models → 把資料丟給 template → render 渲染產生 HTML → 回傳給瀏覽器

def filtered_objekt_type(request):
    # get all data
    objekts = ObjektType.objects.select_related('artist', 'member', 'season', 'collection', 'objekt_class').all()
    
    # filter
    objektFilter = ObjektTypeFilter(request.GET, queryset=objekts)  # queryset 搜尋的範圍
    
    # sort
    ordering = get_ordering(request)  # 在 objekts/urils.py 裡面定義
    sorted_qs = objektFilter.qs.order_by(*ordering)

    context = {
        'objektFilter': objektFilter,
        'cards': sorted_qs, # 篩選排序完的結果
        }
    return render(request, template_name='objekt/list.html', context=context)