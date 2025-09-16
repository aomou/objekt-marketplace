# 定義 update User, Profile 的填寫欄位

from django import forms
from .models import User, UserProfile
from django.contrib.auth.models import User  # 修正 import

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "username"}),
            "email": forms.EmailInput(attrs={"placeholder": "email@example.com"}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['wallet_address', 'contact_info']
        widgets = {
            "wallet_address": forms.TextInput(attrs={"placeholder": "0x123456..."}),
            "contact_info": forms.Textarea(attrs={
                "rows": 4, 
                "placeholder": "Discord username, X id, ..."
                }),
        }
    
