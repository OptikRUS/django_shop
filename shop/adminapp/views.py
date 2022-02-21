from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F

from adminapp.forms import AdminShopUserUpdateForm, AdminProductCategoryCreationForm, AdminProductUpdateForm, \
    AdminProductCategoryEditForm
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda user: user.is_superuser)
def index(request):
    page_num = request.GET.get('page', 1)
    all_users = get_user_model().objects.all()
    users_paginator = Paginator(all_users, 2)
    try:
        all_users = users_paginator.page(page_num)
    except PageNotAnInteger:
        all_users = users_paginator.page(1)
    except EmptyPage:
        all_users = users_paginator.page(users_paginator.num_pages)
    content = {
        'page_title': 'админка/пользователи',
        'all_users': all_users,
    }
    return render(request, 'adminapp/index.html', content)


# @user_passes_test(lambda user: user.is_superuser)
# def user_update(request, user_pk):
#     user = get_object_or_404(get_user_model(), pk=user_pk)
#     if request.method == 'POST':
#         user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('new_admin:index'))
#     else:
#         user_form = AdminShopUserUpdateForm(instance=user)
#
#     context = {
#         'page_title': 'админка/пользователи/редактирование',
#         'form': user_form
#     }
#     return render(request, 'adminapp/shopuser_form.html', context)


class ShopUserAdminUpdate(UpdateView):
    model = get_user_model()
    form_class = AdminShopUserUpdateForm
    success_url = reverse_lazy('new_admin:index')
    pk_url_kwarg = 'user_pk'


def user_delete(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    if not user.is_active or request.method == 'POST':
        if user.is_active:
            user.is_active = False
            user.save()
            return HttpResponseRedirect(reverse('new_admin:index'))
    content = {
        'page_title': 'админка/пользователи/удаление',
        'user_to_delete': user,
    }
    return render(request, 'adminapp/user_delete.html', content)


# @user_passes_test(lambda user: user.is_superuser)
# def categories(request):
#     content = {
#         'page_title': 'админка/категории',
#         'category_list': ProductCategory.objects.all()
#     }
#     return render(request, 'adminapp/productcategory_list.html', context=content)


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title_key = 'page_title'
    page_title = None

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content[self.page_title_key] = self.page_title
        return content


class ProductCategoryList(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ProductCategory
    page_title = 'админка/категории'


class ProductCategoryCreate(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    form_class = AdminProductCategoryCreationForm
    success_url = reverse_lazy('new_admin:categories')
    page_title = 'Категории/создание/'


class ProductCategoryUpdate(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    form_class = AdminProductCategoryCreationForm
    success_url = reverse_lazy('new_admin:categories')
    page_title = 'категории/редактирование'
    form_class = AdminProductCategoryEditForm

    def form_valid(self, form):
        if 'discount' or 'undiscount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            undiscount = form.cleaned_data['undiscount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
            else:
                self.object.product_set.update(price=F('price') * (1 + undiscount / 100))
            return super().form_valid(form)


class ProductCategoryDelete(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('new_admin:categories')
    page_title = 'Категории/удаление'


@user_passes_test(lambda user: user.is_superuser)
def category_products(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    object_list = category.product_set.all()
    content = {
        'page_title': f'категория {category.name}/продукты',
        'category': category,
        'object_list': object_list
    }
    return render(request, 'mainapp/category_products_list.html', content)


@user_passes_test(lambda user: user.is_superuser)
def category_product_create(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'new_admin:category_products',
                kwargs={'slug': category.slug}
            ))
    else:
        form = AdminProductUpdateForm(
            initial={
                'category': category,
            }
        )

    content = {
        'page_title': 'продукты/создание',
        'form': form,
        'category': category,
    }
    return render(request, 'mainapp/product_update.html', content)


class ProductDetail(SuperUserOnlyMixin, PageTitleMixin, DetailView):
    model = Product
    page_title = 'товар/подробнее'
