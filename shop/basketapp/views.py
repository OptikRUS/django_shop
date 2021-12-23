from django.contrib.auth.decorators import login_required
from basketapp.models import BasketItem
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


@login_required
def index(request):
    basket = request.user.basket.all() # если указан related_name в models
    content = {
        'page_title': 'корзина',
        'basket': basket,
    }
    return render(request, 'basketapp/index.html', content)


@login_required
def add(request, product_pk):
    basket_item, _ = BasketItem.objects.get_or_create(
        user=request.user,
        product_id=product_pk,
    )
    basket_item.qty += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove(request, basket_item_pk):
    item = get_object_or_404(BasketItem, pk=basket_item_pk)
    item.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))