from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.utils.decorators import method_decorator

from adminapp.forms import AdminShopUserUpdateForm, ProductCategoryCreationForm
from mainapp.models import ProductCategory


@user_passes_test(lambda user: user.is_superuser)
def index(request):
    all_users = get_user_model().objects.all()
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
    form_class = ProductCategoryCreationForm
    success_url = reverse_lazy('new_admin:categories')
    page_title = 'Категории/создание/'


class ProductCategoryUpdate(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    form_class = ProductCategoryCreationForm
    success_url = reverse_lazy('new_admin:categories')
    page_title = 'Категории/редактирование/'


class ProductCategoryDelete(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('new_admin:categories')
    page_title = 'Категории/удаление'