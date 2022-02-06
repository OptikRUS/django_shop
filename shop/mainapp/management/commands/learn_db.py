from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from django.db import connection
from django.db.models import Q, F, When, Case, DecimalField, IntegerField
from datetime import timedelta

from mainapp.views import db_profile_by_type
from ordersapp.models import OrderItem


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         test_products = Product.objects.filter(
#             Q(category__name='офис') |
#             Q(category__name='модерн')
#         ).select_related('category')  # объединяем в один запрос
#         print(len(test_products))
#         # print(test_products)
#
#         test_select = Product.objects.filter(
#             Q(category__name='дом') |
#             Q(category__product__price__gte=1500)
#         ).select_related()
#         print(len(test_select))
#         db_profile_by_type('learn db', '', connection.queries)

"""
чит-коды без вызова класса команд

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geekshop.settings')

import django

django.setup()

from django.db import connection
from django.db.models import Q

from mainapp.models import Product
from mainapp.views import db_profile_by_type


def sample_1():
    test_products = Product.objects.filter(
        Q(category__name='офис') |
        Q(category__name='модерн')
    ).select_related('category')

    # print(len(test_products))
    print(test_products)
    # 7 min -> 20:12 AIR

    db_profile_by_type('learn db', '', connection.queries)
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_EXPIRED = 3

        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)

        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05

        action_1__condition = Q(order__update_dt__lte=F('order__add_dt') + action_1__time_delta)

        action_2__condition = Q(order__update_dt__gt=F('order__add_dt') + action_1__time_delta) & \
                              Q(order__update_dt__lte=F('order__add_dt') + action_2__time_delta)

        action_expired__condition = Q(order__update_dt__gt=F('order__add_dt') + action_2__time_delta)

        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(action_expired__condition, then=ACTION_EXPIRED)

        action_1__price = When(action_1__condition, then=F('product__price') * F('qty') * action_1__discount)
        action_2__price = When(action_2__condition, then=F('product__price') * F('qty') * -action_2__discount)
        action_expired__price = When(action_expired__condition, then=F('product__price') * F('qty') * action_expired__discount)

        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            )).annotate(
            discount=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            )).order_by('action_order', 'discount').select_related('order', 'product')

        for orderitem in test_orders:
            print(f'{orderitem.action_order:2}: заказ No{orderitem.pk:3}: '
                  f'{orderitem.product.name:10}: скидка '
                  f'{abs(orderitem.discount):6.2f} руб. | '
                  f'{orderitem.order.update_dt - orderitem.order.add_dt}')
