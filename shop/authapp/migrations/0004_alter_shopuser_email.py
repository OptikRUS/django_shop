# Generated by Django 3.2.9 on 2021-12-22 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_alter_shopuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
