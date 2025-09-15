from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,  # 當 user 被刪除，profile 也會被刪除
        )
    wallet_address = models.CharField(max_length=100, db_index=True, blank=True)
    contact_info = models.CharField(max_length=300, blank=True)  # 可考慮擴充成不同平台的 dict 形式

    def __str__(self):
        return f"{self.user.username} ({self.wallet_address})"
