# Generated by Django 3.0.4 on 2020-06-04 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='createdDate',
            field=models.DateTimeField(blank=True, null=True, verbose_name='CreatedDate'),
        ),
        migrations.AlterField(
            model_name='cases',
            name='purchaseDate',
            field=models.DateField(blank=True, null=True, verbose_name='PurchaseDate'),
        ),
        migrations.AlterField(
            model_name='srqs',
            name='createdDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
