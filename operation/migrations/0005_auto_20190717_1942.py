# Generated by Django 2.0.7 on 2019-07-18 00:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20190717_1602'),
        ('operation', '0004_auto_20190717_1710'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='detailoperation',
            unique_together={('operation', 'product')},
        ),
    ]
