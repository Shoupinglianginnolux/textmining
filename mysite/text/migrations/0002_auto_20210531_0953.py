# Generated by Django 3.0.4 on 2021-05-31 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='osrpartnumber',
            old_name='Model',
            new_name='MODEL',
        ),
        migrations.RemoveField(
            model_name='osrpartnumber',
            name='Tconless',
        ),
        migrations.AddField(
            model_name='osrpartnumber',
            name='TCONLESS',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
