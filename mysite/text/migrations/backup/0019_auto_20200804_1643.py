# Generated by Django 3.0.4 on 2020-08-04 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0018_auto_20200717_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cases',
            name='id',
        ),
        migrations.AlterField(
            model_name='cases',
            name='CaseNumber',
            field=models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='CaseNumber'),
        ),
    ]