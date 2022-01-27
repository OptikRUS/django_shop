from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from random import choice
from mainapp.models import ProductCategory, Product


def get_hot_product():
    return choice(Product.get_items().filter(category__is_active=True, is_active=True))


def same_products(hot_product):
    return Product.get_items().filter(category=hot_product.category, is_active=True).exclude(pk=hot_product.pk)[:3]


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
        products = Product.get_items().filter(category__is_active=True, is_active=True)
    else:
        category = get_object_or_404(ProductCategory, slug=slug)
        products = category.product_set.filter(is_active=True)

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
