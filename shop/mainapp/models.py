from django.db import models


class ProductCategory(models.Model):
    name = models.CharField('имя', max_length=64)
    description = models.TextField('описание', blank=True)
    short_desc = models.CharField('краткое описание', max_length=200, blank=True)
    href = models.CharField('href', max_length=64)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категорияя продукта'
        verbose_name_plural = 'категории продукта'
        ordering = ['name']

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField('имя', max_length=64)
    image = models.ImageField(upload_to='products_images', blank=True)
    description = models.TextField('описание', blank=True)
    short_desc = models.CharField('краткое описание', max_length=200, blank=True)
    price = models.DecimalField('цена', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField('количество на складе', default=0)

    def __str__(self):
        return f'{self.name} ({self.category.name})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']