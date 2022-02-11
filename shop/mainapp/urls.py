from django.urls import path
from mainapp.views import index, products, contact, category

app_name = 'mainapp'

urlpatterns = [
    path('', index, name='main'),
    path('products/', products, name='products'),
    path('category/<slug:slug>/', category, name='category'),
    path('contact/', contact, name='contact'),
]
