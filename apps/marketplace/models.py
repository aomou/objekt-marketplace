from django.db import models
from django.contrib.auth.models import User
from apps.objekt.models import ObjektType, ObjektCard


class ObjektList(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='objekt_list')
    objekts = models.ManyToManyField(ObjektCard, related_name='objekt_list')
    description = models.TextField()
    # price = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ObjektList.name

# TODO 用 ObjektListItems 記錄 Objekt 和 ObjektList 之間的關係和 price