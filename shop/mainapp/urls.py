from django.urls import path

from mainapp.views import index, products, contact

app_name = 'mainapp'

urlpatterns = [
    path('', index, name='main'),
    path('products/', products, name='products'),
    path('products/<slug:slug>', products, name='products'),
    path('contact/', contact, name='contact'),
]
