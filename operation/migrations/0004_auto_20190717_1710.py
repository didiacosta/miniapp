# Generated by Django 2.0.7 on 2019-07-17 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_auto_20190717_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaloperation',
            name='user_ip_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='operation',
            name='user_ip_address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
