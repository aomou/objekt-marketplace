from django.contrib import admin
from .models import Artist, Season, Class, Member, Collection, ObjektType, ObjektCard

# Register models 把定義好的資料表 models 掛到 admin 後台管理系統  
admin.site.register([Artist, Class, ObjektCard, ObjektType])

# 設定後台顯示的欄位
# Member
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'memberCode', 'memberNum')
admin.site.register(Member, MemberAdmin)

# Collection
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'physical')
admin.site.register(Collection, CollectionAdmin)

# Season
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'seasonPrefix', 'seasonNum')
admin.site.register(Season, SeasonAdmin)
