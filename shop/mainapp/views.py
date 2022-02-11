from random import choice
from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product


def get_menu():
    return ProductCategory.objects.filter()


def get_hot_product():
    return choice(Product.objects.all())


def same_products(hot_product):
    return Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]


def index(request):
    content = {
        'page_title': 'Главная',
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    hot_product = get_hot_product()
    content = {
        'page_title': 'Продукты',
        'categories': get_menu(),
        'hot_product': hot_product,
        'same_products': same_products(hot_product),
    }
    return render(request, 'mainapp/products.html', content)


def product_page(request, pk):
    product = get_object_or_404(Product, pk=pk)
    content = {
        'page_title': 'страница продукта',
        'categories': get_menu(),
        'product': product,
    }
    return render(request, 'mainapp/product_page.html', content)


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
