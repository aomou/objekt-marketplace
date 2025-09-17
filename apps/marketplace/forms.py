# 定義 user objektlists CRUD 列表

from django import forms
from .models import ObjektList
from django.contrib.auth.models import User

class ListEditForm(forms.ModelForm):
    class Meta:
        model = ObjektList
        fields = ['name', 'description', 'is_public', 'objekts']
        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea(attrs={"rows": 4}),
            'is_public': forms.BooleanField(),
            'objekts': forms.ManyToManyField(),
        }