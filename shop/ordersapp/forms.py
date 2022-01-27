from django import forms
from django.forms import HiddenInput

from ordersapp.models import Order, OrderItem


class BaseOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'user':
                field.widget = HiddenInput()
            field.widget.attrs['class'] = 'form-control'


class OrderForm(BaseOrderForm):
    class Meta:
        model = Order
        fields = ('user',)


class OrderItemForm(BaseOrderForm):
    price = forms.FloatField(required=False)

    # def clean_qty(self):
    #     qty = self.cleaned_data.get('qty')
    #     if qty > self.instance.product.quantity:
    #         raise forms.ValidationError('На складе больше нет товара')
    #     return qty

    class Meta:
        model = OrderItem
        fields = '__all__'
