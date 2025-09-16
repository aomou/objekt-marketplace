from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ObjektList
from django.contrib.auth.models import User

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