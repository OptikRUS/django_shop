from django.db import models
from django.contrib.auth import get_user_model
from django.utils.functional import cached_property

from mainapp.models import Product


class Order(models.Model):
    STATUS_FORMNING = 'F'
    STATUS_SENDED = 'S'
    STATUS_PAID = 'P'
    STATUS_CANCELED = 'D'

    STATUS_CHOICES = (
        (STATUS_FORMNING, 'формируется'),
        (STATUS_SENDED, 'отправлен'),
        (STATUS_PAID, 'оплачен'),
        (STATUS_CANCELED, 'отменён'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    add_dt = models.DateTimeField('время', auto_now_add=True, db_index=True)
    update_dt = models.DateTimeField('время', auto_now=True)
    status = models.CharField('статус', max_length=1, choices=STATUS_CHOICES, default=STATUS_FORMNING, db_index=True)
    is_active = models.BooleanField(verbose_name='активен', default=True, db_index=True)

    @cached_property
    def total_items(self):
        return self.items.select_related().all()

    @cached_property
    def is_forming(self):
        return self.status == self.STATUS_FORMNING

    def set_paid_status(self):
        self.status = self.STATUS_PAID
        self.save()

    @cached_property
    def total_quantity(self):
        return sum(map(lambda x: x.qty, self.total_items))

    @cached_property
    def total_cost(self):
        return sum(map(lambda x: x.product_cost, self.total_items))

    # возвращает на склад при удалении заказа
    def delete(self, using=None, keep_parents=False):
        for item in self.total_items:
            item.product.quantity += item.qty
            item.product.save()
        super().delete()

    class Meta:
        ordering = ('-add_dt',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField('количество', default=0)

    @cached_property
    def product_cost(self):
        return self.product.price * self.qty
