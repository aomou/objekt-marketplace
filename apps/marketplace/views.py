from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ObjektList
from .forms import ListEditForm
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.http import HttpResponseNotAllowed
from django.contrib import messages

# Create your views here.

@login_required  # for 函數型 FBV (function based view)
def mylists(request):
    mylists = ObjektList.objects.filter(owner=request.user).all()

    context = {
        'mylists': mylists,
    }
    return render(request, template_name='marketplace/mylists.html', context=context)


def marketplace(request):
    all_public_lists = ObjektList.objects.filter(is_public=True).all()

    context = {
        'all_public_lists': all_public_lists,
    }
    return render(request, template_name='marketplace/market.html', context=context)

# CBV - Class Based View
# CRUD edit list

class ObjektListView(LoginRequiredMixin, ListView):  # for 類別型 CBV (Class based view)
    model = ObjektList
    template_name = 'marketplace/mylists.html'
    context_object_name = "mylists"

    def get_queryset(self):
        return ObjektList.objects.filter(owner=self.request.user).order_by('-created_at')

class CreateListView(CreateView):
    model = ObjektList
    form_class = ListEditForm
    success_url = '/marketplace/mylists'  # 儲存成功後要導向的網址

    def form_valid(self, form):
        obj = form.save(commit=False)  # 拿出來 先不存
        obj.owner = self.request.user  # 綁定 user
        obj.save()                     # 存進資料庫
        return super().form_valid(form)

class UpdateListView(UpdateView):
    model = ObjektList
    form_class = ListEditForm
    success_url = '/marketplace/mylists'

    def get_queryset(self):
        return ObjektList.objects.filter(owner=self.request.user).order_by('-created_at')

class DeleteListView(DeleteView):
    model = ObjektList
    success_url = '/marketplace/mylists'

    # 只能刪自己的 list
    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    # 不顯示刪除頁面（GET -> 405）
    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
    
    # 刪除後給訊息
    def post(self, request, *args, **kwargs):
        messages.success(request, 'List deleted!')
        return super().post(request, *args, **kwargs)
