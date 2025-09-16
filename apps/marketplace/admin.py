from django.contrib import admin
from .models import ObjektList

# Register your models here.
# admin.site.register([ObjektList])


class ObjektListAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_public', 'created_at')
admin.site.register(ObjektList, ObjektListAdmin)
