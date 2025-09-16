from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import UserProfile
from .forms import UserForm, ProfileForm

# views

@login_required  # 如果沒登入就跳轉到 /accounts/login/ 登入頁面
def account_info(request):
    # 內建的使用者資料   user 會自動傳入不用放在 context

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

    # 填寫 / 修改 Profile
    # POST
    if request.method == 'POST': 
        user_form = UserForm(request.POST, instance=request.user, prefix='user')
        profile_form = ProfileForm(request.POST, instance=user_profile, prefix='profile')

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'User info and profile updated!')
            return redirect('account_info')  # 在同一頁的話也要 redirect 嗎
        else:
            messages.error(request, 'Wrong input!')
    # GET
    else: 
        user_form = UserForm(instance=request.user, prefix='user')
        profile_form = ProfileForm(instance=user_profile, prefix='profile')
 
    context = {
        'username': request.user.username,
        'user_profile': user_profile,
        'profile_created': profile_created,
        'user_form': user_form,
        'profile_form': profile_form,
        }

    return render(request, template_name='accounts/info.html', context=context)


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(
                username=new_user.username, 
                password=request.POST['password1'] # ??
                )
            login(request, authenticated_user)
            return redirect('account_info')
    context = {
        'form': form
    }
    return render(request, template_name='registration/register.html', context=context)
