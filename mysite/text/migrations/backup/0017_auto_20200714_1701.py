# Generated by Django 3.0.4 on 2020-07-14 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0016_auto_20200713_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='TMPSRQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SRNumber', models.CharField(max_length=12, verbose_name='SRNumber')),
                ('SRType', models.CharField(max_length=5, verbose_name='SRType')),
                ('CreatedDate', models.DateTimeField(blank=True, null=True)),
                ('Model', models.CharField(max_length=15, verbose_name='Model')),
                ('SerialNumber', models.CharField(blank=True, max_length=25, null=True)),
                ('ErrorCode', models.CharField(max_length=30)),
                ('InternalNotes', models.CharField(max_length=300)),
                ('PredictErrorCode', models.CharField(blank=True, max_length=10, null=True)),
                ('ReviseErrorCode', models.CharField(blank=True, max_length=10, null=True)),
                ('Train', models.BooleanField(blank=True, default=True, null=True)),
                ('UploadDate', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='srqs',
            name='ReviseErrorCode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
