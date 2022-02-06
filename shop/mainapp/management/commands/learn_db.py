from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from django.db import connection
from django.db.models import Q
from mainapp.views import db_profile_by_type


class Command(BaseCommand):
    def handle(self, *args, **options):
        test_products = Product.objects.filter(
            Q(category__name='офис') |
            Q(category__name='модерн')
        ).select_related('category')  # объединяем в один запрос
        print(len(test_products))
        # print(test_products)

        test_select = Product.objects.filter(
            Q(category__name='дом') |
            Q(category__product__price__gte=1500)
        ).select_related()
        print(len(test_select))
        db_profile_by_type('learn db', '', connection.queries)

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