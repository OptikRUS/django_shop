from django.shortcuts import render
import json

# Create your views here.
with open('links.json', 'r', encoding='utf-8') as f:
    links_menu = json.load(f)

def main(request):
    content = {
        'title': 'Главная',
    }
    return render(request, 'mainapp/index.html', content)

def products(request):
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)

def contact(request):
    content = {
        'title': 'контакты',
    }
    return render(request, 'mainapp/contact.html', content)
