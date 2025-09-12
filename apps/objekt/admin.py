from django.contrib import admin
from .models import Artist, Season, Class, Member, Collection, ObjektType, ObjektCard

# Register models 把定義好的資料表 models 掛到 admin 後台管理系統  
admin.site.register([Artist, Season, Class, Member, ObjektCard, ObjektType])

# 設定後台顯示的欄位
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'physical', )

admin.site.register(Collection, CollectionAdmin)
