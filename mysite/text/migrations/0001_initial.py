# Generated by Django 3.0.4 on 2021-05-26 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Auth_application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField(verbose_name='工號')),
                ('current_status', models.CharField(blank=True, choices=[('1', '審核中'), ('2', '已通過'), ('3', '未通過')], default=1, max_length=10, null=True, verbose_name='目前狀態')),
                ('reason', models.CharField(blank=True, max_length=255, null=True)),
                ('apply_datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cases',
            fields=[
                ('CaseNumber', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='CaseNumber')),
                ('CreatedDate', models.DateTimeField(blank=True, null=True, verbose_name='CreatedDate')),
                ('Model', models.CharField(max_length=50, verbose_name='Model')),
                ('SerialNumber', models.CharField(max_length=100, verbose_name='SerialNumber')),
                ('Symptom', models.TextField(blank=True, max_length=500, null=True, verbose_name='Symbol')),
                ('Diagnosis', models.TextField(blank=True, max_length=500, null=True, verbose_name='Diagnosis')),
                ('Description', models.TextField(max_length=500, verbose_name='Description')),
                ('PredictErrorCode', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ComboPartsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Vizio_Model', models.CharField(max_length=225, verbose_name='Vizio Model')),
                ('INX_Model', models.CharField(max_length=225, verbose_name='INX Model')),
                ('Parts', models.CharField(max_length=225, verbose_name='Parts')),
                ('Combo_Function', models.CharField(max_length=225, verbose_name='Combo Function')),
            ],
        ),
        migrations.CreateModel(
            name='Defect',
            fields=[
                ('Code', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='Code')),
                ('Symptom', models.CharField(blank=True, max_length=100, null=True, verbose_name='Symptom')),
            ],
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Class', models.CharField(blank=True, max_length=100, null=True, verbose_name='Class')),
                ('Rule', models.TextField(blank=True, null=True, verbose_name='Rule')),
                ('Action', models.TextField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Logfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usageDateTime', models.DateTimeField(auto_now_add=True)),
                ('hostname', models.CharField(blank=True, max_length=50, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=50, null=True)),
                ('action', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OSR',
            fields=[
                ('Work_Order', models.CharField(blank=True, max_length=100, null=True, verbose_name='Work Order #')),
                ('OSRNumber', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='OSR #')),
                ('TV_Model', models.CharField(blank=True, max_length=100, null=True, verbose_name='TV Model')),
                ('TV_SerialNo', models.CharField(blank=True, max_length=100, null=True, verbose_name='TV SerialNo')),
                ('Import_Date', models.DateField(blank=True, null=True, verbose_name='Import Date')),
                ('ProblemDesc', models.TextField(blank=True, max_length=500, null=True, verbose_name='ProblemDesc')),
                ('ErrorCode', models.CharField(blank=True, max_length=225, null=True)),
                ('Train_Parts', models.CharField(blank=True, max_length=225, null=True)),
                ('Sent_Parts', models.CharField(blank=True, max_length=225, null=True)),
                ('Predict_Train_Parts', models.CharField(blank=True, max_length=225, null=True)),
                ('Predict_Sent_Parts', models.CharField(blank=True, max_length=225, null=True)),
                ('F2score', models.CharField(blank=True, max_length=225, null=True)),
                ('Similar_OSRNumber', models.CharField(max_length=225, verbose_name='Similar_OSR #')),
                ('OverSent_Parts', models.CharField(blank=True, max_length=225, null=True)),
                ('UnderSent_Parts', models.CharField(blank=True, max_length=225, null=True)),
                ('Threshold_result', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OsrPartNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Model', models.CharField(max_length=50, verbose_name='MODEL')),
                ('CHILD_PRODUCT_ID', models.CharField(max_length=225, verbose_name='CHILD_PRODUCT_ID')),
                ('PART_DESCRIPTION', models.CharField(max_length=225, verbose_name='PART_DESCRIPTION')),
                ('CHILD_DESCRIPTION', models.CharField(max_length=225, verbose_name='CHILD_DESCRIPTION')),
                ('Tconless', models.TextField(blank=True, max_length=500, null=True, verbose_name='Tconless')),
            ],
        ),
        migrations.CreateModel(
            name='PartsPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TV_Model', models.CharField(blank=True, max_length=255, null=True, verbose_name='TV Model')),
                ('Part_Description', models.CharField(blank=True, max_length=255, null=True)),
                ('Part_Price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SearchData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CaseNumber', models.CharField(blank=True, max_length=12, null=True)),
                ('SRNumber', models.CharField(blank=True, max_length=12, null=True, verbose_name='SRNumber')),
                ('SRType', models.CharField(blank=True, max_length=5, null=True, verbose_name='SRType')),
                ('CreatedDate', models.DateTimeField(blank=True, null=True)),
                ('Model', models.CharField(max_length=15, verbose_name='Model')),
                ('SerialNumber', models.CharField(blank=True, max_length=25, null=True)),
                ('ErrorCode', models.CharField(blank=True, max_length=30, null=True)),
                ('InternalNotes', models.CharField(max_length=300)),
                ('Symptom', models.CharField(blank=True, max_length=100, null=True, verbose_name='Symbol')),
                ('PredictErrorCode', models.CharField(blank=True, max_length=10, null=True)),
                ('Train', models.BooleanField(blank=True, default=True, null=True)),
                ('PredictPart', models.CharField(blank=True, max_length=100, null=True)),
                ('Diagnosis', models.CharField(blank=True, max_length=150, null=True, verbose_name='Diagnosis')),
                ('Data_source_type', models.CharField(blank=True, choices=[(0, 'Case'), (1, 'SRQ')], max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialUsageRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SRType', models.CharField(blank=True, max_length=5, null=True, verbose_name='SRType')),
                ('Created_Date', models.DateField(blank=True, null=True, verbose_name='Created Date')),
                ('Closed_Date', models.DateField(blank=True, null=True, verbose_name='Closed Date')),
                ('Model', models.CharField(max_length=50, verbose_name='Model')),
                ('ErrorCode', models.CharField(max_length=225)),
                ('Parts_delete', models.CharField(max_length=225, verbose_name='Parts delete')),
                ('Parts_added', models.CharField(max_length=225, verbose_name='Parts added')),
                ('Remark', models.TextField(blank=True, max_length=500, null=True, verbose_name='ProblemDesc')),
            ],
        ),
        migrations.CreateModel(
            name='SRQs',
            fields=[
                ('SRNumber', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='SRNumber')),
                ('SRType', models.CharField(max_length=5, verbose_name='SRType')),
                ('CreatedDate', models.DateTimeField(blank=True, null=True)),
                ('Model', models.CharField(max_length=15, verbose_name='Model')),
                ('SerialNumber', models.CharField(blank=True, max_length=25, null=True)),
                ('ErrorCode', models.CharField(max_length=225)),
                ('InternalNotes', models.TextField(blank=True, null=True)),
                ('PredictErrorCode', models.CharField(blank=True, max_length=225, null=True)),
                ('ReviseErrorCode', models.CharField(blank=True, max_length=225, null=True)),
                ('Train', models.BooleanField(blank=True, default=True, null=True)),
                ('PredictPart', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TMPSRQ',
            fields=[
                ('SRNumber', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='SRNumber')),
                ('SRType', models.CharField(max_length=5, verbose_name='SRType')),
                ('CreatedDate', models.DateTimeField(blank=True, null=True)),
                ('Model', models.CharField(max_length=15, verbose_name='Model')),
                ('SerialNumber', models.CharField(blank=True, max_length=25, null=True)),
                ('ErrorCode', models.CharField(blank=True, max_length=225, null=True)),
                ('InternalNotes', models.TextField(blank=True, null=True)),
                ('PredictErrorCode', models.CharField(blank=True, max_length=225, null=True)),
                ('ReviseErrorCode', models.CharField(blank=True, max_length=225, null=True)),
                ('Train', models.BooleanField(blank=True, default=True, null=True)),
                ('UploadDate', models.DateField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ongoing', models.BooleanField(default=False)),
                ('StartTime', models.DateTimeField(auto_now=True)),
                ('EndTime', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Auth_approval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval', models.CharField(blank=True, choices=[('0', '同意'), ('1', '不同意')], max_length=10, null=True)),
                ('opinion', models.CharField(blank=True, max_length=255, null=True)),
                ('apprval_datetime', models.DateTimeField(auto_now=True)),
                ('auth_application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='text.Auth_application')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]