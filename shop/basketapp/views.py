from django.shortcuts import render
from basketapp.models import BasketItem

def index(request):
    pass


def add(request, pk):
    pass
    # basket = BasketItem.objects.filter(user=request.user)
    # basket = request.user.basketitem_set.all() # тоже самое
    # basket = request.user.basket.all() # если указан related_name в models


def remove(request, pk):
    pass
