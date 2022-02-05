from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from django.views.decorators.cache import cache_page, never_cache

from random import choice
from mainapp.models import ProductCategory, Product
from shop import settings


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.get_items()
            cache.set(key, products)
        return products
    return Product.get_items()


def get_category(slug):
    if settings.LOW_CACHE:
        key = f'category_{slug}'
        products = cache.get(key)
        if products is None:
            products = Product.get_items().filter(category__slug=slug)
            cache.set(key, products)
        return products
    return Product.get_items().filter(category__slug=slug)


def get_hot_product():
    return choice(get_products().filter(category__is_active=True, is_active=True))


def same_products(hot_product):
    return get_products().filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]


def index(request):
    content = {
        'page_title': 'Главная',
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    hot_product = get_hot_product()
    content = {
        'page_title': 'Продукты',
        'hot_product': hot_product,
        'same_products': same_products(hot_product),
    }
    return render(request, 'mainapp/products.html', content)


# @never_cache
def product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    content = {
        'page_title': 'страница продукта',
        'product': product,
    }
    return render(request, 'mainapp/product_page.html', content)


def category(request, slug=None):
    page_num = request.GET.get('page', 1)
    if not slug or slug == 'all':
        category = {'slug': 'all', 'name': 'все'}
        products = get_products()
    else:
        category = get_object_or_404(ProductCategory, slug=slug)
        products = get_category(slug)

    products_paginator = Paginator(products, 3)
    try:
        products = products_paginator.page(page_num)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products  = products_paginator.page(products_paginator.num_pages)

    content = {
        'page_title': 'категории',
        'category': category,
        'products': products,

    }
    return render(request, 'mainapp/category.html', content)


# @cache_page(3600)
def contact(request):
    locations = [
        {'city': 'Москва',
         'phone': '+7-888-888-8888',
         'email': 'info@geekshop.ru',
         'address': 'В пределах МКАД',
         },
        {'city': 'Санкт-Петербург',
         'phone': '+7-999-999-9999',
         'email': 'info.spb@geekshop.ru',
         'address': 'В пределах КАД',
         },
        {'city': 'Ростов-на-Дону',
         'phone': '+7-000-000-0000',
         'email': 'info.rnd@geekshop.ru',
         'address': 'В пределах области',
         },
    ]
    content = {
        'page_title': 'контакты',
        'locations': locations,
    }
    return render(request, 'mainapp/contact.html', content)


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.filter(pk=pk).first()
        return JsonResponse({'price': product and product.price or 0})


def db_profile_by_type(sender, q_type, queries):
    print(f'db_profile {q_type} for {sender}:')
    for query in filter(lambda x: q_type in x['sql'], queries):
        print(query['sql'])


@receiver(pre_save, sender=ProductCategory)
def update_product_category_save(sender, instance, **kwargs):
    """
    зависимость активности товаров от активности категорий
    """
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)
        db_profile_by_type(sender, 'UPDATE', connection.queries)