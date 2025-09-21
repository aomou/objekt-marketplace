# 定義 user objektlists CRUD 列表

from django import forms
from .models import ObjektList, ObjektType
from django.contrib.auth.models import User

class ListEditForm(forms.ModelForm):
    objekts = forms.ModelMultipleChoiceField(
        queryset = ObjektType.objects.all(),
        widget = forms.CheckboxSelectMultiple
    )

    class Meta:
        model = ObjektList
        fields = ['name', 'description', 'is_public', 'objekts']
        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea(attrs={"rows": 4}),
            'is_public': forms.CheckboxInput(),
        }
