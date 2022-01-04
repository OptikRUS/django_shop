from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('user/delete/<int:user_pk>/', adminapp.user_delete, name='user_delete'),
    # path('user/update/<int:user_pk>/', adminapp.user_update, name='user_update'),
    path('user/update/<int:user_pk>/', adminapp.ShopUserAdminUpdate.as_view(), name='user_update'),

    # path('categories/', adminapp.categories, name='categories'),
    path('categories/', adminapp.ProductCategoryList.as_view(), name='categories'),
    path('category/create/', adminapp.ProductCategoryCreate.as_view(), name='category_create'),
    path('category/update/<slug:slug>/', adminapp.ProductCategoryUpdate.as_view(), name='category_update'),
    path('category/delete/<slug:slug>/', adminapp.ProductCategoryDelete.as_view(), name='category_delete'),
]
