from django.shortcuts import render
from .models import UserProfile
from django.contrib.auth.decorators import login_required

# views

@login_required  # 如果沒登入就跳轉到 /accounts/login/ 登入頁面
def account_info(request):
    # 內建的使用者資料
    user = request.user  # user 會自動傳入不用放在 context
    # 自訂的 user profile
    # 如果沒有 Profile 就先 create
    user_profile, profile_created = UserProfile.objects.get_or_create(
        user = request.user,
        defaults = {
            'wallet_address': '',
            'contact_info': '',
        }
    )

    # todo 帶入擁有的 objekt or list
    # example 
    # owned_list = ObjektList.objects.filter(owner=request.user).order_by('created_at')

    context = {
        'username': request.user.username,
        'user_profile': user_profile,
        'profile_created': profile_created,
        }

    return render(request, template_name='accounts/info.html', context=context)