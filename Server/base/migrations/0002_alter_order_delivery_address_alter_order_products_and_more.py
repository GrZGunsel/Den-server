# Generated by Django 4.2 on 2023-04-24 14:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='base.cart'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
