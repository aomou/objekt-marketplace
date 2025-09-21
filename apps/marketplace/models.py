from django.db import models
from django.contrib.auth.models import User
from apps.objekt.models import ObjektType, ObjektCard
from django.db.models import Count

class ObjektList(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='objekt_list')
    objekts = models.ManyToManyField(ObjektCard, related_name='objekt_list', blank=True)
    description = models.TextField(blank=True)
    # price = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.owner}"

    def get_objekts_stats(self):
        def to_dict(qs, key):
            return {row[key]: row['count'] for row in qs}
        class_count = self.objekts.values('objekt_type__objekt_class__name').annotate(count=Count('id')).order_by('-count')
        artist_count = self.objekts.values('objekt_type__artist__name').annotate(count=Count('id')).order_by('-count')
        season_count = self.objekts.values('objekt_type__season__name').annotate(count=Count('id')).order_by('-count')
        traits_count = {
            'class': to_dict(class_count, 'objekt_type__objekt_class__name'),
            'artist': to_dict(artist_count, 'objekt_type__artist__name'),
            'season': to_dict(season_count, 'objekt_type__season__name'),
        }
        return traits_count

# TODO 用 ObjektListItems 記錄 Objekt 和 ObjektList 之間的關係和 price