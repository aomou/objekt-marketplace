# objekt 過濾器

import django_filters
from django import forms
from .models import ObjektType, ObjektCard, Artist, Member, Class, Season, Collection

class ObjektTypeFilter(django_filters.FilterSet):
    artist = django_filters.ModelChoiceFilter(
        field_name = 'artist',
        queryset = Artist.objects.all().order_by('tokenId'),
        widget = forms.Select(attrs={'onchange': 'this.form.submit()'})
    )
    member = django_filters.ModelChoiceFilter(
        field_name = 'member',
        queryset = Member.objects.filter(artist__isnull=False).order_by('artist__tokenId', 'memberNum'),
        widget = forms.Select(attrs={'onchange': 'this.form.submit()'})
    )
    objekt_class = django_filters.ModelChoiceFilter(
        field_name = 'objekt_class',
        queryset = Class.objects.all().order_by('artist__name', 'name'),
        widget = forms.Select(attrs={'onchange': 'this.form.submit()'})
    )

    class Meta:
        model = ObjektType
        fields = ['artist', 'member', 'objekt_class'] # 指定篩選欄位 ['attr'] or '__all__'