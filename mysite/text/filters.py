from django import forms
from django.db.models import Q
from .models import SRQs, Cases, Keywords, SearchData, TMPSRQ, OSR
import django_filters
from django_filters import DateRangeFilter ,DateFilter
import itertools

class SrqsFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='gte', label='Start Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt1'},
        ))
    end_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='lte', label='End Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt2'},
        ))
    errorCode = django_filters.CharFilter(lookup_expr='icontains', label='Error Code', field_name='ErrorCode')

    class Meta:
        model = SRQs
        fields = ['SRNumber', 'SRType', 'Model', 'errorCode', 'InternalNotes', 'start_date', 'end_date', 'SerialNumber' ]

class TMPSrqsFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='gte', label='Start Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt1'},
        ))
    end_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='lte', label='End Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt2'},
        ))
    errorCode = django_filters.CharFilter(lookup_expr='icontains', label='Error Code', field_name='ErrorCode')

    class Meta:
        model = TMPSRQ
        fields = ['SRNumber', 'SRType', 'Model', 'errorCode', 'InternalNotes', 'start_date', 'end_date', 'SerialNumber' ]



class SrqsKeywordsFilter(django_filters.FilterSet):


    start_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='gte', label='Start Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt1',  'placeholder': '2020-02-01', 'pattern': '\d{4}-\d{2}-\d{2}','autocomplete':'off', 'required':'true'},
        ))
    end_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='lte', label='End Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt2',  'placeholder': '2020-03-01', 'pattern': '\d{4}-\d{2}-\d{2}','autocomplete':'off', 'required':'true'},
        ))
    class Meta:
        model = SRQs
        fields = ['start_date', 'end_date', ]

class SrqsOSRFilter(django_filters.FilterSet):

    CHOICES = (('Option 1', 'Option 1'),('Option 2', 'Option 2'),)

    start_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='gte', label='Start Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt1',  'placeholder': '2020-02-01', 'pattern': '\d{4}-\d{2}-\d{2}', 'autocomplete':'off'},
        ))
    end_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='lte', label='End Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt2',  'placeholder': '2020-03-01', 'pattern': '\d{4}-\d{2}-\d{2}', 'autocomplete':'off'},
        ))
    machine_model = django_filters.CharFilter(field_name='Model',lookup_expr='icontains', label='客戶機種')
    part = django_filters.ChoiceFilter(field_name='Model', label='Part 名稱(下拉選單)', widget=forms.Select(attrs={'class': 'form-control'},choices=CHOICES))

    class Meta:
        model = SRQs
        fields = ['machine_model', 'start_date', 'end_date', 'part']


class SearchdataFilter(django_filters.FilterSet):

    data_source_type_choices = ((0, 'Case'), (1, 'SRQ'))

    start_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='gte', label='Start Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt1', 'placeholder': '2020-02-01', 'pattern': '\d{4}-\d{2}-\d{2}'},
        ))
    end_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='lte', label='End Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt2', 'placeholder': '2020-03-01', 'pattern': '\d{4}-\d{2}-\d{2}'},
        ))
    errorCode = django_filters.CharFilter(lookup_expr='icontains', label='Error Code', field_name='ErrorCode',
    widget=forms.TextInput(
           attrs={'maxlength': '3', 'pattern': '[a-zA-Z]{1}[0-9]{2}'},
        ))
    data_source_type = django_filters.ChoiceFilter(choices=data_source_type_choices, empty_label='both')

    class Meta:
        model = SearchData
        fields = ['SRNumber', 'Model', 'errorCode', 'InternalNotes', 'start_date', 'end_date', 'data_source_type', 'SerialNumber']


class CasesFilter(django_filters.FilterSet):

    start_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='gte', label='Start Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt1'},
        ))
    end_date = django_filters.DateTimeFilter(field_name='CreatedDate', lookup_expr='lte', label='End Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt2'},
        ))
    errorCode = django_filters.CharFilter(lookup_expr='icontains', label='Error Code', field_name='PredictErrorCode')
    internalNotes = django_filters.CharFilter(lookup_expr='icontains', label='Internal Notes', field_name='Discription')


    class Meta:
        model = Cases
        fields = ['Model', 'errorCode', 'internalNotes', 'start_date', 'end_date', 'SerialNumber' ]

class _OSRFilter(django_filters.FilterSet):
    osr_no = django_filters.CharFilter(lookup_expr='icontains', label='OSR no.', field_name='OSRNumber')

    class Meta:
        model = OSR
        fields = ['osr_no']


class OSRDateFilter(django_filters.FilterSet):


    start_date = django_filters.DateTimeFilter(field_name='Import_Date', lookup_expr='gte', label='Start Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt1',  'placeholder': '2021-01-01', 'pattern': '\d{4}-\d{2}-\d{2}', 'autocomplete':'off', 'required':'true'},
        ))
    end_date = django_filters.DateTimeFilter(field_name='Import_Date', lookup_expr='lte', label='End Date', widget=forms.DateInput(
           format=('%Y-%m-%d'), attrs={'id': 'dt2',  'placeholder': '2021-01-31', 'pattern': '\d{4}-\d{2}-\d{2}', 'autocomplete':'off', 'required':'true'},
        ))

    class Meta:
        model = OSR
        fields = ['start_date', 'end_date']