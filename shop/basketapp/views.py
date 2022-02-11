from django.contrib.auth.decorators import login_required
from basketapp.models import BasketItem
from django.http import HttpResponseRedirect


@login_required
def index(request):
    pass
    # basket = BasketItem.objects.filter(user=request.user)
    # basket = request.user.basketitem_set.all() # тоже самое
    # basket = request.user.basket.all() # если указан related_name в models


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
def remove(request, pk):
    pass
