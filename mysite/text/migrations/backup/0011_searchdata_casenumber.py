# Generated by Django 3.0.4 on 2020-07-08 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0010_auto_20200708_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchdata',
            name='caseNumber',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
