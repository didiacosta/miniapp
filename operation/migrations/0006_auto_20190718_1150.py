# Generated by Django 2.0.7 on 2019-07-18 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0005_auto_20190717_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaloperation',
            name='date_operation',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='historicaloperation',
            name='status',
            field=models.CharField(default='provisioned', max_length=200),
        ),
        migrations.AlterField(
            model_name='operation',
            name='date_operation',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='operation',
            name='status',
            field=models.CharField(default='provisioned', max_length=200),
        ),
    ]