from django.shortcuts import render  # 把 data 和 html template 結合
from .models import ObjektType  # 從 models.py 匯入資料表
from .filters import ObjektTypeFilter

# views
# 接收 request → 取得資料 models → 把資料丟給 template → render 渲染產生 HTML → 回傳給瀏覽器

# objekt cards
# def all_card_list(request):
#     # 取得要顯示的資料 QuerySet
#     # 取出所有資料(前50) 先查詢好 FK ???
#     qs = ObjektCard.objects.select_related('objekt_type', 'objekt_type__artist').all()[:50]
#     context = {
#         'cards': qs
#         }
#     return render(request, template_name='objekt/list.html', context=context)

# objekt types
# def all_objekt_type(request):
#     qs = ObjektType.objects.select_related('artist', 'member', 'season', 'collection', 'objekt_class').all()[:50]
#     context = {
#         'cards': qs,
#     }
#     return render(request, template_name='objekt/list.html', context=context)


def filtered_objekt_type(request):
    # get all data
    objekts = ObjektType.objects.select_related('artist', 'member', 'season', 'collection', 'objekt_class').all()
    
    # filter
    objektFilter = ObjektTypeFilter(request.GET, queryset=objekts)  # queryset 搜尋的範圍
    
    # sort
    sort_by = request.GET.get('sort_by', 'season') # 預設用 season 排序
    sort_secondary = request.GET.get('sort_secondary', '') # 次要排序
    order = request.GET.get('order', 'asc')  # 預設 ascending

    # 建立排序列表
    ordering = []
    if order == 'asc':
        ordering.append(sort_by)
        if sort_secondary:
            ordering.append(sort_secondary)
    else:
        ordering.append(f'-{sort_by}')
        if sort_secondary:
            ordering.append(f'-{sort_secondary}')
    
    sorted_qs = objektFilter.qs.order_by(*ordering)

    context = {
        'objektFilter': objektFilter,
        'cards': sorted_qs, # 篩選排序完的結果
        }
    return render(request, template_name='objekt/list.html', context=context)