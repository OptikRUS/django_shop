from django.shortcuts import render, get_object_or_404

# Create your views here.
from basketapp.models import BasketItem
from mainapp.models import ProductCategory, Product
from django.db.models import Sum


def get_menu():
    return ProductCategory.objects.filter()


def index(request):
    content = {
        'page_title': 'Главная',
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    content = {
        'page_title': 'Продукты',
        'categories': get_menu(),
    }
    return render(request, 'mainapp/products.html', content)


def category(request, slug=None):
    count = BasketItem.objects.filter(user_id=request.user).aggregate(total=Sum('qty'))['total']
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
        'count': count,
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
