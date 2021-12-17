from django.shortcuts import render
import json

# Create your views here.
from mainapp.models import Product, ProductCategory

# with open('links.json', 'r', encoding='utf-8') as f:
#     links_menu = json.load(f)

submenu = ProductCategory.objects.all()

def main(request):
    content = {
        'page_title': 'Главная',
    }
    return render(request, 'mainapp/index.html', content)

def products(request):

    content = {
        'page_title': 'Продукты',
        # 'links_menu': links_menu,
        'submenu': submenu,
    }
    return render(request, 'mainapp/products.html', content)

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
