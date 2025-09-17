from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import ObjektList
from .forms import ListEditForm
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DeleteView, UpdateView


# Create your views here.

@login_required
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

@method_decorator(login_required, name="dispatch")
class ObjektListView(ListView):
    model = ObjektList
    template_name = 'marketplace/mylists.html'
    context_object_name = "mylists"

    def get_queryset(self):
        return ObjektList.objects.filter(owner=self.request.user).order_by('-created_at')

class CreateListView(CreateView):
    model = ObjektList
    form_class = ListEditForm
