from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory
from django.db import transaction
from django.http import HttpResponseRedirect
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete

from ordersapp.forms import OrderForm, OrderItemForm
from ordersapp.models import Order, OrderItem


# def index(request):
#     return render(request, 'ordersapp/index.html')


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return self.request.user.orders.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Заказы'
        return context


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """
        inlineformset_factory принимает на вход:
        главный класс заказа Order,
        класс элементов заказа OrderItem(one-to-many),
        класс формы OrderItemForm,
        количество форм в наборе extra
        """
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=3)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES)
        else:
            context['form'].initial['user'] = self.request.user
            basket_items = self.request.user.basket.all()
            if basket_items and basket_items.count():
                OrderFormSet = inlineformset_factory(
                    Order, OrderItem, form=OrderItemForm,
                    extra=basket_items.count() + 1
                )
                formset = OrderFormSet()
                for form, basket_item in zip(formset.forms, basket_items):
                    form.initial['product'] = basket_item.product
                    form.initial['qty'] = basket_item.qty
                # basket_items.delete()
            else:
                formset = OrderFormSet()

        context['orderitems'] = formset
        context['page_title'] = 'Создание заказа'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():  # аналог NTFS
            order = super().form_valid(form)
            if orderitems.is_valid():
                orderitems.instance = self.object  # one to many
                orderitems.save()
                self.request.user.basket.all().delete()

        # удаляем пустой заказ
        if self.object.total_cost == 0:
            self.object.delete()

        return order


class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                instance = form.instance
                if instance.pk:
                    form.initial['price'] = instance.product.price
        context['orderitems'] = formset
        context['page_title'] = 'Редактирование заказа'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            order = super().form_valid(form)
            if orderitems.is_valid():
                orderitems.save()

        # удаляем пустой заказ
        if self.object.total_cost == 0:
            self.object.delete()

        return order


class FormingComplete(UpdateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        order.set_paid_status()
        order.save()
        return context


class OrderDetail(DetailView):
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Просмотр заказа'
        return context


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Удаление заказа'
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.STATUS_PAID
    order.save()
    return HttpResponseRedirect(reverse('orders:index'))


@receiver(pre_save, sender=OrderItem)
def product_quantity_update_save(sender, instance, **kwargs):
    if instance.pk:
        instance.product.quantity += sender.objects.get(pk=instance.pk).qty - instance.qty
    else:
        instance.product.quantity -= instance.qty
    instance.product.save()
