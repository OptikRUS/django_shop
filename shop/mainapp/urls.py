from django.urls import path
from mainapp.views import index, products, contact, category, product_page, get_product_price

app_name = 'mainapp'

urlpatterns = [
    path('', index, name='main'),
    path('products/', products, name='products'),
    path('category/<slug:slug>/', category, name='category'),
    path('contact/', contact, name='contact'),
    path('product/<int:pk>/', product_page, name='product_page'),
    path('product/<int:pk>/price/', get_product_price),
]
