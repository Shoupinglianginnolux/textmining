from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
class Cases(models.Model):
    CaseNumber = models.CharField(max_length=100, verbose_name="CaseNumber", primary_key=True)
    CreatedDate = models.DateTimeField("CreatedDate",  blank=True, null=True)
    Model = models.CharField("Model", max_length=50)
    SerialNumber = models.CharField("SerialNumber", max_length=100)
    Symptom = models.TextField("Symbol", max_length=500, blank=True, null=True)
    Diagnosis = models.TextField("Diagnosis", max_length=500, blank=True, null=True)
    Description = models.TextField("Description", max_length=500)
    PredictErrorCode = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.CaseNumber

class SRQs(models.Model):
    SRNumber = models.CharField("SRNumber", max_length=12, primary_key=True)
    SRType = models.CharField("SRType", max_length= 5)
    CreatedDate	= models.DateTimeField(blank=True, null=True)
    Model = models.CharField("Model", max_length=15)
    SerialNumber = models.CharField(max_length=25, blank=True, null=True)
    ErrorCode = models.CharField(max_length=225)
    InternalNotes = models.TextField(blank=True, null=True)
    PredictErrorCode = models.CharField(max_length=225, blank=True, null=True)
    ReviseErrorCode = models.CharField(max_length=225, blank=True, null=True)
    Train = models.BooleanField(default=True, blank=True, null=True)
    PredictPart = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.SRNumber

class Keywords(models.Model):
    Class = models.CharField(max_length=100, verbose_name='Class', blank=True, null=True)
    Rule = models.TextField(verbose_name='Rule', blank=True, null=True)
    Action = models.TextField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.Class

class Logfiles(models.Model):
    usageDateTime = models.DateTimeField(auto_now_add=True)
    hostname = models.CharField(max_length=50, blank=True, null=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    action = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.usageDateTime) + ' ' + self.hostname + ' with IP: ' + self.ip_address + ' ' + self.action

class SearchData(models.Model):

    data_source_type_choices = ((0, 'Case'), (1, 'SRQ'))

    CaseNumber = models.CharField(max_length=12, blank=True, null=True)
    SRNumber = models.CharField("SRNumber", max_length=12, blank=True, null=True)
    SRType = models.CharField("SRType", max_length= 5, null=True, blank=True)
    CreatedDate	= models.DateTimeField(blank=True, null=True)
    Model = models.CharField("Model", max_length=15)
    SerialNumber = models.CharField(max_length=25, blank=True, null=True)
    ErrorCode = models.CharField(max_length=30, blank=True, null=True)
    InternalNotes = models.CharField(max_length=300)
    Symptom = models.CharField("Symbol", max_length=100, blank=True, null=True)
    PredictErrorCode = models.CharField(max_length=10, blank=True, null=True)
    Train = models.BooleanField(default=True, blank=True, null=True)
    PredictPart = models.CharField(max_length=100, blank=True, null=True)
    Diagnosis = models.CharField("Diagnosis", max_length=150, blank=True, null=True)
    Data_source_type = models.CharField(max_length=10, choices=data_source_type_choices, blank=True, null=True)

    def __str__(self):
        return self.Model + ' ' + self.InternalNotes


class TMPSRQ(models.Model):
    SRNumber = models.CharField("SRNumber", max_length=12, primary_key=True)
    SRType = models.CharField("SRType", max_length= 5)
    CreatedDate	= models.DateTimeField(blank=True, null=True)
    Model = models.CharField("Model", max_length=15)
    SerialNumber = models.CharField(max_length=25, blank=True, null=True)
    ErrorCode = models.CharField(max_length=225, blank=True, null=True)
    InternalNotes = models.TextField(blank=True, null=True)
    PredictErrorCode = models.CharField(max_length=225, blank=True, null=True)
    ReviseErrorCode = models.CharField(max_length=225, blank=True, null=True)
    Train = models.BooleanField(default=True, blank=True, null=True)
    UploadDate = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.SRNumber

class Training(models.Model):
    Ongoing = models.BooleanField(default=False)
    StartTime = models.DateTimeField(auto_now=True, auto_now_add=False)
    EndTime = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.Ongoing) + 'Starting at: ' + self.StartTime.strftime() + 'Ends at : ' + self.EndTime.strftime()


class Defect(models.Model):
    Code = models.CharField("Code", max_length=12, primary_key=True)
    Symptom = models.CharField("Symptom", max_length=100, blank=True, null=True)
    def __str__(self):
        return self.Code + self.Symptom

    def __unicode__(self):
        return self.Code

class Auth_approval(models.Model):
    auth_application = models.ForeignKey("Auth_application", on_delete=models.CASCADE)
    approval = models.CharField(choices=(("0", "同意"), ("1","不同意")), max_length=10, blank=True, null=True)
    opinion = models.CharField(max_length=255, blank=True, null=True)
    apprval_datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

class Auth_application(models.Model):
    employee_id = models.IntegerField(verbose_name="工號")
    current_status = models.CharField(choices=(("1","審核中"), ("2", "已通過"), ("3", "未通過")), default= 1, verbose_name='目前狀態', max_length=10, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    apply_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.employee_id)

class OSR(models.Model):
    Work_Order = models.CharField("Work Order #", max_length=100, blank=True, null=True)
    OSRNumber = models.CharField("OSR #", primary_key=True, max_length=100)
    TV_Model = models.CharField("TV Model", max_length=100, blank=True, null=True)
    TV_SerialNo = models.CharField("TV SerialNo", max_length=100, blank=True, null=True)
    Import_Date = models.DateField("Import Date", blank=True, null=True)
    ProblemDesc = models.TextField("ProblemDesc", max_length=500, blank=True, null=True)
    ErrorCode = models.CharField(max_length=225, blank=True, null=True)
    Train_Parts = models.CharField(max_length=225, blank=True, null=True)
    Sent_Parts = models.CharField(max_length=225, blank=True, null=True)
    Predict_Train_Parts = models.CharField(max_length=225, blank=True, null=True)
    Predict_Sent_Parts = models.CharField(max_length=225, blank=True, null=True)
    F2score = models.CharField(max_length=225,blank=True, null=True)
    Similar_OSRNumber = models.CharField("Similar_OSR #", max_length=225)
    OverSent_Parts = models.CharField(max_length=225, blank=True, null=True)
    UnderSent_Parts = models.CharField(max_length=225, blank=True, null=True)
    Threshold_result = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.Work_Order) + str(self.OSRNumber)

class SpecialUsageRule(models.Model):
    SRType = models.CharField("SRType", max_length= 5, null=True, blank=True)
    Created_Date = models.DateField("Created Date", blank=True, null=True)
    Closed_Date = models.DateField("Closed Date", blank=True, null=True)
    Model = models.CharField("Model", max_length=50)
    ErrorCode = models.CharField(max_length=225)
    Parts_delete = models.CharField("Parts delete",max_length=225)
    Parts_added = models.CharField("Parts added", max_length=225)
    Remark = models.TextField("ProblemDesc", max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.Remark)

class ComboPartsList(models.Model):
    Vizio_Model = models.CharField("Vizio Model", max_length=225)
    INX_Model = models.CharField("INX Model", max_length=225)
    Parts = models.CharField("Parts", max_length=225)
    Combo_Function = models.CharField("Combo Function", max_length=225)


    def __str__(self):
        return str(self.Vizio_Model)

class PartsPrice(models.Model):
    TV_Model = models.CharField("TV Model", max_length=255, blank=True, null=True)
    Part_Description = models.CharField(max_length=255, blank=True, null=True)
    Part_Price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.TV_Model) + str(self.Part_Description) + str(self.Part_Price)

class OsrPartNumber(models.Model):
    MODEL = models.CharField("MODEL", max_length=50)
    CHILD_PRODUCT_ID = models.CharField("CHILD_PRODUCT_ID", max_length=225)
    PART_DESCRIPTION = models.CharField("PART_DESCRIPTION",max_length=225)
    CHILD_DESCRIPTION = models.CharField("CHILD_DESCRIPTION", max_length=225)
    TCONLESS = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.CHILD_PRODUCT_ID)