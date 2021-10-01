# Generated by Django 3.0.4 on 2020-07-08 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0008_auto_20200708_1027'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sr_number', models.CharField(blank=True, max_length=12, null=True, verbose_name='SRNumber')),
                ('sr_type', models.CharField(blank=True, max_length=5, null=True, verbose_name='SRType')),
                ('createdDate', models.DateTimeField(blank=True, null=True)),
                ('machine_model', models.CharField(max_length=15, verbose_name='Model')),
                ('serialNumber', models.CharField(blank=True, max_length=25, null=True)),
                ('errorCode', models.CharField(blank=True, max_length=30, null=True)),
                ('internalNotes', models.CharField(max_length=300)),
                ('predict_error_code', models.CharField(blank=True, max_length=10, null=True)),
                ('train', models.BooleanField(blank=True, default=True, null=True)),
                ('predict_partial', models.CharField(blank=True, max_length=100, null=True)),
                ('data_source_type', models.CharField(blank=True, choices=[(0, 'Case'), (1, 'SRQ')], max_length=10, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='cases',
            name='action',
        ),
        migrations.RemoveField(
            model_name='cases',
            name='driver',
        ),
        migrations.RemoveField(
            model_name='cases',
            name='mailing_postal_code',
        ),
        migrations.RemoveField(
            model_name='cases',
            name='odm',
        ),
        migrations.RemoveField(
            model_name='cases',
            name='purchaseDate',
        ),
        migrations.RemoveField(
            model_name='cases',
            name='purchaseLocation',
        ),
        migrations.RemoveField(
            model_name='cases',
            name='resolution',
        ),
        migrations.RemoveField(
            model_name='cases',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='srqs',
            name='odm',
        ),
        migrations.RemoveField(
            model_name='srqs',
            name='purchaseDate',
        ),
        migrations.RemoveField(
            model_name='srqs',
            name='purchaseLocation',
        ),
        migrations.RemoveField(
            model_name='srqs',
            name='status',
        ),
        migrations.AddField(
            model_name='srqs',
            name='predict_partial',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
