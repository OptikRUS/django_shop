from random import choice
from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product


def get_menu():
    return ProductCategory.objects.filter()


def get_hot_product():
    return choice(Product.objects.all())


def index(request):
    content = {
        'page_title': 'Главная',
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    content = {
        'page_title': 'Продукты',
        'categories': get_menu(),
        'hot_product': get_hot_product(),
    }
    return render(request, 'mainapp/products.html', content)


def category(request, slug=None):
    if not slug or slug == 'all':
        category = {'slug': 'all', 'name': 'все'}
        products = Product.objects.all()
    else:
        category = get_object_or_404(ProductCategory, slug=slug)
        products = category.product_set.all()

    content = {
        'page_title': 'категории',
        'category': category,
        'categories': get_menu(),
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
