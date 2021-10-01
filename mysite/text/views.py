from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.db.models import Q, Count, Sum, F, Avg
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.datastructures import MultiValueDictKeyError
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.views.decorators.cache import cache_control
from django.views.generic.base import RedirectView
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.db import connections
from dateutil import parser


import pandas as pd
import numpy as np


from .algorithm import main

from . import forms
from .models import Cases, SRQs, Keywords, OsrPartNumber, Logfiles, SearchData, TMPSRQ, Training, Defect, User, OSR, Auth_application, ComboPartsList, SpecialUsageRule, PartsPrice, OsrPartNumber
from .filters import SrqsFilter, SrqsKeywordsFilter, SrqsOSRFilter, SearchdataFilter, CasesFilter, TMPSrqsFilter, _OSRFilter, OSRDateFilter

from rest_framework.views import APIView
from vincent.colors import brews
import datetime
from datetime import timezone
from distutils.util import strtobool
from .inx_sso import CheckAD
from .mapppost_content import mapppost_content
from requests.adapters import HTTPAdapter
from io import BytesIO

import numpy as np
import json
import gc
import xlsxwriter
import xlwt
import socket
import requests
import nltk
import logging, ast
import re
import time
from wsgiref.util import FileWrapper
import os

## configure the ip where algorithm locates
algorithm_ip = 'http://127.0.0.1'

## for local test
# algorithm_ip = 'http://10.55.14.205'


## set up logfiles
logging.basicConfig(filename='logfile.log',level=logging.DEBUG)
gc.DEBUG_STATS

## set up retries of requests
s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))

# print(time.strftime('%Y-%m-%d %H:%M:%S'))


# model classification
@permission_required('text.add_cases')
@cache_control(no_cache=True, must_revalidate=True)
def latest_errorcode(request):
    """View function for home page of site."""
    # try:
    if Training.objects.all().order_by('-id')[0].Ongoing:
        context = {

        }
        return render(request, 'latest_errorcode_traing.html', context)

    if 'case_statistic_to_draw' not in request.session.keys() and 'srq_statistic_to_draw' not in request.session.keys() or 'result'  not in request.session.keys():
        context = {

        }
        return render(request, 'latest_errorcode.html', context)

    case_statistic_to_draw = request.session['case_statistic_to_draw']
    srq_statistic_to_draw = request.session['srq_statistic_to_draw']
    result = request.session['result']

    context = {
            'c': srq_statistic_to_draw,
            'd': case_statistic_to_draw,
            'result':result,
        }
    return render(request, 'latest_errorcode.html', context)
    # except:
    #     logging.exception('Exception occurred while loading latest errorcode page.')
    #     return render(request, 'latest_errorcode.html', context)


@login_required
def latest_keyword(request):
    if 'analytics_to_display_list_cat' not in request.session.keys():

        context = {

        }
        return render(request, 'latest_keyword.html', context)
    ## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    connections.close_all()
    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='load latest keyword page')

    ## Garbage collection
    gc.collect()
    analytics_to_display_list_cat = request.session['analytics_to_display_list_cat']
    analytics_to_display_cases = request.session['analytics_to_display_cases']
    analytics_to_display_list_data_cases = request.session['analytics_to_display_list_data_cases']
    analytics_to_display_list_cat_cases = request.session['analytics_to_display_list_cat_cases']
    data_to_draw_cases = request.session['data_to_draw_cases']
    labels_cases = request.session['labels_cases']
    analytics_to_display_list_data  = request.session['analytics_to_display_list_data']
    analytics_to_display = request.session['analytics_to_display']
    labels = request.session['labels']
    data_to_draw = request.session['data_to_draw']

    context = {
                'analytics_to_display': analytics_to_display,
                'analytics_to_display_list_cat': analytics_to_display_list_cat,
                'analytics_to_display_list_data': analytics_to_display_list_data,
                'analytics_to_display_cases': analytics_to_display_cases,
                'analytics_to_display_list_cat_cases': analytics_to_display_list_cat_cases,
                'analytics_to_display_list_data_cases': analytics_to_display_list_data_cases,
                'data_to_draw': data_to_draw,
                'labels': labels,
                'data_to_draw_cases': data_to_draw_cases,
                'labels_cases': labels_cases,
            }


            # Render the HTML template index.html with the data in the context variable
    return render(request, 'latest_keyword.html', context)


    # except:
    #     print('it goes to except')
    #     logging.exception('Exeption on latest keyword happened.')
    #     context = {}

    #     return render(request, 'latest_keyword.html', context)

@login_required
def historical_errorcode(request):
    try:
        connections.close_all()
        if Training.objects.all().order_by('-id')[0].Ongoing:
            context = {

            }
            return render(request, 'latest_errorcode_traing.html', context)
        # handles user data
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='load historical_Errorcode page')

        search_data_filter = SearchdataFilter(request.GET, queryset=SearchData.objects.all())

        firstload = 'Please enter the search fields, and press Submit to start the search.'
        logging.debug('load historical_errorcode')


        context = {

        'filter': search_data_filter,
        'firstload': firstload,
        }
        return render(request,'historical_errorcode.html',context)

    except:

        search_data_filter = SearchdataFilter(request.GET, queryset=SearchData.objects.all())
        firstload = 'Please enter the search fields, and press Submit to start the search.'
        logging.error('An error happened when trying to handle the search' + str(request.GET))

        context = {

        'filter': search_data_filter,
        'firstload': firstload,
        }
        return render(request,'historical_errorcode.html',context)

@login_required
def historical_errorcode_result(request):

    # try:
        if request.method == 'GET':  #redundent line, just for ease of testing
            search_type = ''

            if not request.GET._mutable:
                request.GET._mutable = True

            if request.GET['data_source_type'] == 'SRQ':
                del request.GET['data_source_type']
                connections.close_all()
                srqs_filter = SrqsFilter(request.GET, queryset=SRQs.objects.all())
                tmpsrq_filter = TMPSrqsFilter(request.GET, queryset=TMPSRQ.objects.all())
                ## handle qs
                srq_df = pd.DataFrame(list(srqs_filter.qs.values()))
                tmpsrq_df = pd.DataFrame(list(tmpsrq_filter.qs.values()))
                srq_df = srq_df.append(tmpsrq_df)
                ## handle files
                if len(srq_df) == 0:
                    context = {
                    'filter': srqs_filter,
                    'data_source': "SRQs",
                    'error_count_sum': 0
                    }
                    return render(request,'historical_errorcode.html',context)

                srq_df['SerialNumber_manufature_year'] = np.where((srq_df['SerialNumber'].str.len()) > 15, srq_df["SerialNumber"].astype(str).str[9].str.capitalize(), srq_df["SerialNumber"].astype(str).str[7].str.capitalize())
                srq_df['SerialNumber_manufature_week'] = np.where((srq_df['SerialNumber'].str.len()) > 15, srq_df["SerialNumber"].astype(str).str[10:12].str.capitalize(), srq_df["SerialNumber"].astype(str).str[8:10].str.capitalize())
                srq_df["Manufacturing wk code (yyww)"] = srq_df['SerialNumber_manufature_year'].map({'U': '18', 'V': '19', 'W':'20', 'X':'21', 'Y':'22', 'Z': '23'})+srq_df['SerialNumber_manufature_week']
                srq_df["Week code (yyww)"] = srq_df["CreatedDate"].dt.strftime('%y%V')
                mapping = pd.DataFrame(list(Defect.objects.all().values()))
                mapping = mapping[["Code", "Symptom"]].astype(str)
                mapping.drop_duplicates(subset ="Code", keep='last', inplace = True)
                mapping.dropna(subset=['Code', 'Symptom'], inplace=True)
                mapping.reset_index(drop=True, inplace=True)
                mapping_dict = mapping.set_index('Code').to_dict()['Symptom']
                srq_df['Details'] = srq_df['ErrorCode'].astype(str).str[0:3].map(mapping_dict)


                ## Handle Historical Errorcode Error Data
                srq_error_df = srq_df.copy()
                revised_df = srq_error_df[srq_error_df["ReviseErrorCode"].notna()]
                revised_error = revised_df.loc[(revised_df['ReviseErrorCode'] != revised_df['PredictErrorCode'])]
                not_revised = srq_error_df[srq_error_df["ReviseErrorCode"].isna()]
                srq_error_df_to_export_from_filtered = not_revised.loc[(not_revised['ErrorCode'].astype(str).str[:3] != not_revised['PredictErrorCode'].astype(str).str[:3] )]
                revised_error = revised_error.append(srq_error_df_to_export_from_filtered)
                if 'PredictPart' not in list(revised_error.columns):
                    revised_error['PredictPart'] = ''

                if len(revised_error) > 0:
                    with pd.ExcelWriter('Historical ErrorCode Error Data.xlsx') as writer:
                        revised_error.to_excel(writer, sheet_name='SRQs',index=False, columns=['SRNumber','SRType','CreatedDate','Model','SerialNumber','ErrorCode','InternalNotes','PredictErrorCode',	'ReviseErrorCode','Train','PredictPart','Manufacturing wk code (yyww)',	'Week code (yyww)','Details'])

                ## Prepares front end with pandas
                srq_fields_df_copy = srq_df.copy()
                # if user is searching for general inf.
                if request.GET['errorCode'] == "" and request.GET['Model'] == "":
                    srq_count_series = srq_fields_df_copy.groupby(['ErrorCode']).size()
                    srq_statistic_df = srq_count_series.to_frame(name = 'size').reset_index().sort_values(['size'], ascending=False)
                    srq_statistic_df.reset_index(drop=True, inplace=True)
                    final_df_for_cqe = pd.DataFrame(columns = ['ErrorCode', 'size', 'percentage'])
                    size_sum = srq_statistic_df.sum()[-1]
                    temp = srq_statistic_df.head(10)
                    top10_sum = temp.sum()[-1]
                    temp['percentage'] = temp['size'] / size_sum
                    temp = temp.append({'ErrorCode': 'Others', 'size': size_sum-top10_sum, 'percentage': (size_sum-top10_sum)/size_sum  }, ignore_index=True)
                    final_df_for_cqe = final_df_for_cqe.append(temp, ignore_index=True)
                    df_to_export = srq_statistic_df.iloc[0:5]
                    all_model_size_sum = srq_statistic_df.sum()[-1]
                    top5_sum = df_to_export.sum()[-1]
                    others_df = df_to_export.append({'ErrorCode': 'Others', 'size': all_model_size_sum - top5_sum}, ignore_index=True)
                    others_df['error_count_sum'] = all_model_size_sum
                    srq_statistic_df_dict = others_df.to_dict(orient='records')
                    search_type = 'general'
                    writer = pd.ExcelWriter('Historical ErrorCode Summary Data.xlsx', engine='xlsxwriter')
                    if 'PredictPart' not in list(srq_df.columns):
                        srq_df['PredictPart'] = ''
                    srq_df.to_excel(writer, sheet_name='SRQs',index=False, columns=['SRNumber','SRType','CreatedDate','Model','SerialNumber','ErrorCode','InternalNotes','PredictErrorCode','ReviseErrorCode','Train','PredictPart','Manufacturing wk code (yyww)',	'Week code (yyww)','Details'])
                    final_df_for_cqe.to_excel(writer, sheet_name="Statistics", index=False)
                    # Access the XlsxWriter workbook and worksheet objects from the dataframe.
                    workbook = writer.book
                    worksheet = writer.sheets['Statistics']
                    worksheet.set_column('A:B', 12, None)
                    # Create a chart object.
                    chart = workbook.add_chart({'type': 'pie'})
                    chart.set_size({'x_scale': 1.5, 'y_scale': 2})
                    percent_fmt = workbook.add_format({'num_format': '0.00%'})
                    worksheet.set_column('C:C', 12, percent_fmt)
                    chart.add_series({
                        'categories': '=Statistics!A2:A12',
                        'values':     '=Statistics!B2:B12',
                        'points': [
                            {'fill': {'color': brews['Set1'][0]}},
                            {'fill': {'color': brews['Set1'][1]}},
                            {'fill': {'color': brews['Set1'][2]}},
                            {'fill': {'color': brews['Set1'][3]}},
                            {'fill': {'color': brews['Set1'][4]}},
                            {'fill': {'color': brews['Set1'][5]}},
                            {'fill': {'color': brews['Set1'][6]}},

                        ],
                        'data_labels': {'percentage': True},
                    })
                    # Insert the chart into the worksheet.
                    worksheet.insert_chart('D2', chart)
                    # Access the XlsxWriter workbook SRQs sheet and worksheet objects from the dataframe.
                    srq_sheet = writer.sheets['SRQs']
                    srq_sheet.set_column('A:A', 12, None)
                    srq_sheet.set_column('C:C', 20, None)
                    srq_sheet.set_column('E:G', 20, None)
                    # Close the Pandas Excel writer and output the Excel file.
                    writer.save()
                # if user is searching for errorcode
                elif len(srq_fields_df_copy.Model.unique()) > 1:
                    srq_count_series = srq_fields_df_copy.groupby(['Model']).size()
                    srq_statistic_df = srq_count_series.to_frame(name = 'size').reset_index().sort_values(['size'], ascending=False)
                    srq_statistic_df.reset_index(drop=True, inplace=True)
                    df_to_export = srq_statistic_df.iloc[0:5]
                    all_model_size_sum = srq_statistic_df.sum()[-1]
                    top5_sum = df_to_export.sum()[-1]
                    others_df = df_to_export.append({'Model': 'Others', 'size': all_model_size_sum - top5_sum}, ignore_index=True)
                    others_df['error_count_sum'] = all_model_size_sum
                    srq_statistic_df_dict = others_df.to_dict(orient='records')
                    search_type = 'errorcode'

                # if user is searching for models
                else:
                    srq_count_series = srq_fields_df_copy.groupby(['ErrorCode']).size()
                    srq_statistic_df = srq_count_series.to_frame(name = 'size').reset_index().sort_values(['size'], ascending=False)
                    srq_statistic_df.reset_index(drop=True, inplace=True)
                    df_to_export = srq_statistic_df.iloc[0:5]
                    all_model_size_sum = srq_statistic_df.sum()[-1]
                    top5_sum = df_to_export.sum()[-1]
                    others_df = df_to_export.append({'ErrorCode': 'Others', 'size': all_model_size_sum - top5_sum}, ignore_index=True)
                    others_df['error_count_sum'] = all_model_size_sum
                    srq_statistic_df_dict = others_df.to_dict(orient='records')
                    search_type = 'model'

                ## prepares the front end
                error_count_sum=len(srq_df)
                analytics = srqs_filter.qs.values('Model','ErrorCode').distinct().annotate(error_count=Count('SRNumber')).order_by('Model','-error_count')
                problem_models_list = srqs_filter.qs.values('Model').distinct().annotate(model_error_count=Count('SRNumber')).order_by('Model')

                ## substitution end
                data_source = 'SRQ'
                ## getting the hostname by socket.gethostname() method
                hostname = socket.gethostname()
                ip_address = socket.gethostbyname(hostname)
                connections.close_all()
                Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='Perform SRQ historical_errorcode search')

                del analytics, ip_address, hostname
                gc.collect()
                if len(srqs_filter.qs) == 0:
                    context = {
                    'filter': tmpsrq_filter,
                    'error_count_sum': error_count_sum,
                    'data_source': "SRQs",
                    'srq_statistic_df_dict': srq_statistic_df_dict,
                    'search_type': search_type,
                    }
                    return render(request,'historical_errorcode.html',context)

                else:
                    context = {
                    'filter': srqs_filter,
                    'error_count_sum': error_count_sum,
                    'data_source': "SRQs",
                    'srq_statistic_df_dict': srq_statistic_df_dict,
                    'search_type': search_type,
                    }
                    return render(request,'historical_errorcode.html',context)

            if request.GET['data_source_type'] == 'Cases':
                del request.GET['data_source_type']
                connections.close_all()
                cases_filter = CasesFilter(request.GET, queryset=Cases.objects.all())
                cases_df = pd.DataFrame(list(cases_filter.qs.values()))

                if len(cases_df) == 0:
                    print('cases df =0')
                    context = {
                    'filter': cases_filter,
                    'data_source': "Cases",
                    'cases_error_count_sum': 0
                    }
                    return render(request,'historical_errorcode.html',context)

                ## handle files
                with pd.ExcelWriter('Historical ErrorCode Summary Data.xlsx') as writer:
                        cases_df.to_excel(writer, sheet_name='Cases',index=False)

                # analytics = cases_filter.qs.values('PredictErrorCode').distinct().annotate(error_count=Count('CaseNumber')).order_by('-error_count')[:6]
                # analytics_result = 0

                data_source = 'Cases'
                error_count_sum=cases_filter.qs.count()

                # prepares the front end
                cases_analytics = cases_filter.qs.filter(PredictErrorCode__isnull=False).values('Model','PredictErrorCode').distinct().annotate(error_count=Count('CaseNumber')).order_by('Model','-error_count')
                cases_problem_models_list = cases_filter.qs.filter(PredictErrorCode__isnull=False).values('Model').distinct().annotate(model_error_count=Count('CaseNumber')).order_by('Model')

                cases_statisticToDisplay = {}
                for i in cases_problem_models_list:
                    cases_statisticToDisplay[i['Model']] = cases_analytics.filter(Model__icontains=i['Model'])[:5]

                cases_a = []
                for i in cases_problem_models_list:
                    cases_a.append({'model': i['Model'], 'statistic': cases_statisticToDisplay[i['Model']], 'error_count_sum': i['model_error_count']})
                cases_a = sorted(cases_a, key=lambda k: k['error_count_sum'], reverse=True)
                d = []
                for i in cases_a:
                    d.append({'Model': i['model'], 'statistic': list(i['statistic'].values('PredictErrorCode', 'error_count')), 'error_count_sum': i['error_count_sum']})
                for i in d:
                    others = i['error_count_sum']
                    for j in (i['statistic']):
                        others -= j['error_count']
                    i['statistic'].append({'PredictErrorCode': 'Others', 'error_count': others})

                ## To be substituted
                cases_chart_data = []
                if request.GET['Model']:
                    for i in cases_a:
                        for j in (i['statistic']):
                            cases_chart_data.append({ 'PredictErrorCode': j['PredictErrorCode'], 'error_count': j['error_count']})
                if request.GET['errorCode']:
                    for i in cases_a:
                        for j in (i['statistic']):
                            cases_chart_data.append({ 'Model': j['Model'], 'error_count': j['error_count']})
                # substitution end

                # handles user data
                ## getting the hostname by socket.gethostname() method
                hostname = socket.gethostname()
                ## getting the IP address using socket.gethostbyname() method
                ip_address = socket.gethostbyname(hostname)
                ## printing the hostname and ip_address
                Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='Perform cases historical_errorcode search')

                context = {
                'cases_analytics': cases_analytics,
                'cases_error_count_sum': error_count_sum,
                'data_source': data_source,
                'cases_statisticToDisplay': cases_statisticToDisplay,
                'cases_a': cases_a,
                'cases_chart_data': cases_chart_data,
                # 'cases_filter': cases_filter,
                'd': d,
                }
                return render(request,'historical_errorcode.html',context)

            if request.GET['data_source_type'] == 'both':
                connections.close_all()
                srqs_filter = SrqsFilter(request.GET, queryset=SRQs.objects.all())
                cases_filter = CasesFilter(request.GET, queryset=Cases.objects.all())
                tmpsrq_filter = TMPSrqsFilter(request.GET, queryset=TMPSRQ.objects.all())

                ## handle qs
                srq_df = pd.DataFrame(list(srqs_filter.qs.values()))
                tmpsrq_df = pd.DataFrame(list(tmpsrq_filter.qs.values()))
                srq_df.append(tmpsrq_df)
                cases_df = pd.DataFrame(list(cases_filter.qs.values()))

                ## catch if there is no such result
                if len(cases_df)+len(srq_df) == 0 :
                    context = {
                    'filter': srqs_filter,
                    'data_source': "both",
                    'error_count_sum': 0,
                    'cases_error_count_sum':0
                    }
                    return render(request,'historical_errorcode.html',context)

                ## not used due to use case
                # srq_df["Manufacturing wk code (yyww)"] = srq_df["SerialNumber"].astype(str).str[7].str.capitalize().map({'U': '18', 'V': '19', 'W':'20'})+srq_df["SerialNumber"].astype(str).str[8:10]
                # srq_df["Week code (yyww)"] = srq_df["CreatedDate"].dt.strftime('%y%V')
                # mapping = pd.DataFrame(list(Defect.objects.all().values()))
                # mapping = mapping[["Code", "Symptom"]].astype(str)
                # mapping.drop_duplicates(subset ="Code", keep='last', inplace = True)
                # mapping.dropna(subset=['Code', 'Symptom'], inplace=True)
                # mapping.reset_index(drop=True, inplace=True)
                # mapping_dict = mapping.set_index('Code').to_dict()['Symptom']
                # srq_df['Details'] = srq_df['ErrorCode'].astype(str).str[0:3].map(mapping_dict)

                ## handle files
                with pd.ExcelWriter('Historical ErrorCode Summary Data.xlsx') as writer:
                        srq_df.to_excel(writer, sheet_name='SRQs',index=False)
                        cases_df.to_excel(writer, sheet_name='Cases',index=False)

                if len(srq_df) != 0:
                    srq_error_df = srq_df.copy()
                    revised_df = srq_error_df[srq_error_df["ReviseErrorCode"].notna()]
                    revised_error = revised_df.loc[(revised_df['ReviseErrorCode'] != revised_df['PredictErrorCode'])]
                    not_revised = srq_error_df[srq_error_df["ReviseErrorCode"].isna()]
                    srq_error_df_to_export_from_filtered = not_revised.loc[(not_revised['ErrorCode'] != not_revised['PredictErrorCode'] )]
                    revised_error = revised_error.append(srq_error_df_to_export_from_filtered)

                    with pd.ExcelWriter('Historical ErrorCode Error Data.xlsx') as writer:
                        revised_error.to_excel(writer, sheet_name='SRQs',index=False)


                ## prepares the front end
                ## Prepares front end with pandas
                srq_fields_df_copy = srq_df.copy()

                ## prepares the front end
                error_count_sum=srqs_filter.qs.count()
                cases_error_count_sum=cases_filter.qs.count()
                ## prepares the front end
                cases_analytics = cases_filter.qs.filter(PredictErrorCode__isnull=False).values('Model','PredictErrorCode').distinct().annotate(error_count=Count('CaseNumber')).order_by('Model','-error_count')
                cases_problem_models_list = cases_filter.qs.filter(PredictErrorCode__isnull=False).values('Model').distinct().annotate(model_error_count=Count('CaseNumber')).order_by('Model')
                cases_statisticToDisplay = {}
                for i in cases_problem_models_list:
                    cases_statisticToDisplay[i['Model']] = cases_analytics.filter(Model__icontains=i['Model'])[:5]

                cases_a = []
                for i in cases_problem_models_list:
                    cases_a.append({'model': i['Model'], 'statistic': cases_statisticToDisplay[i['Model']], 'error_count_sum': i['model_error_count']})
                cases_a = sorted(cases_a, key=lambda k: k['error_count_sum'], reverse=True)
                cases_chart_data = []
                if request.GET['Model']:
                    for i in cases_a:
                        for j in (i['statistic']):
                            cases_chart_data.append({ 'PredictErrorCode': j['PredictErrorCode'], 'error_count': j['error_count']})
                elif request.GET['errorCode']:
                    for i in cases_a:
                        for j in (i['statistic']):
                            cases_chart_data.append({ 'Model': j['Model'], 'error_count': j['error_count']})


                d = []
                for i in cases_a:
                    d.append({'Model': i['model'], 'statistic': list(i['statistic'].values('PredictErrorCode', 'error_count')), 'error_count_sum': i['error_count_sum']})
                for i in d:
                    others = i['error_count_sum']
                    for j in (i['statistic']):
                        others -= j['error_count']
                    i['statistic'].append({'PredictErrorCode': 'Others', 'error_count': others})

                if len(srq_df) != 0:
                # if user is searching for general inf.
                    if request.GET['errorCode'] == "" and request.GET['Model'] == "":
                        srq_count_series = srq_fields_df_copy.groupby(['ErrorCode']).size()
                        srq_statistic_df = srq_count_series.to_frame(name = 'size').reset_index().sort_values(['size'], ascending=False)
                        srq_statistic_df.reset_index(drop=True, inplace=True)
                        final_df_for_cqe = pd.DataFrame(columns = ['ErrorCode', 'size', 'percentage'])
                        size_sum = srq_statistic_df.sum()[-1]
                        temp = srq_statistic_df.head(10)
                        top10_sum = temp.sum()[-1]
                        temp['percentage'] = temp['size'] / size_sum
                        temp = temp.append({'ErrorCode': 'Others', 'size': size_sum-top10_sum, 'percentage': (size_sum-top10_sum)/size_sum  }, ignore_index=True)
                        final_df_for_cqe = final_df_for_cqe.append(temp, ignore_index=True)
                        df_to_export = srq_statistic_df.iloc[0:5]
                        all_model_size_sum = srq_statistic_df.sum()[-1]
                        top5_sum = df_to_export.sum()[-1]
                        others_df = df_to_export.append({'ErrorCode': 'Others', 'size': all_model_size_sum - top5_sum}, ignore_index=True)
                        others_df['error_count_sum'] = all_model_size_sum
                        srq_statistic_df_dict = others_df.to_dict(orient='records')
                        search_type = 'general'
                        writer = pd.ExcelWriter('Historical ErrorCode Summary Data.xlsx', engine='xlsxwriter')
                        srq_df.to_excel(writer, sheet_name='SRQs',index=False)
                        final_df_for_cqe.to_excel(writer, sheet_name="Statistics", index=False)
                        # Access the XlsxWriter workbook and worksheet objects from the dataframe.
                        workbook = writer.book
                        worksheet = writer.sheets['Statistics']
                        worksheet.set_column('A:B', 12, None)
                        # Create a chart object.
                        chart = workbook.add_chart({'type': 'pie'})
                        chart.set_size({'x_scale': 1.5, 'y_scale': 2})
                        percent_fmt = workbook.add_format({'num_format': '0.00%'})
                        worksheet.set_column('C:C', 12, percent_fmt)
                        chart.add_series({
                            'categories': '=Statistics!A2:A12',
                            'values':     '=Statistics!B2:B12',
                            'points': [
                                {'fill': {'color': brews['Set1'][0]}},
                                {'fill': {'color': brews['Set1'][1]}},
                                {'fill': {'color': brews['Set1'][2]}},
                                {'fill': {'color': brews['Set1'][3]}},
                                {'fill': {'color': brews['Set1'][4]}},
                                {'fill': {'color': brews['Set1'][5]}},
                                {'fill': {'color': brews['Set1'][6]}},

                            ],
                            'data_labels': {'percentage': True},
                        })
                        # Insert the chart into the worksheet.
                        worksheet.insert_chart('D2', chart)
                        # Access the XlsxWriter workbook SRQs sheet and worksheet objects from the dataframe.
                        srq_sheet = writer.sheets['SRQs']
                        srq_sheet.set_column('A:A', 12, None)
                        srq_sheet.set_column('C:C', 20, None)
                        srq_sheet.set_column('E:G', 20, None)
                        # Close the Pandas Excel writer and output the Excel file.
                        writer.save()
                    # if user is searching for errorcode
                    elif len(srq_fields_df_copy.Model.unique()) > 1:
                        srq_count_series = srq_fields_df_copy.groupby(['Model']).size()
                        srq_statistic_df = srq_count_series.to_frame(name = 'size').reset_index().sort_values(['size'], ascending=False)
                        srq_statistic_df.reset_index(drop=True, inplace=True)
                        df_to_export = srq_statistic_df.iloc[0:5]
                        all_model_size_sum = srq_statistic_df.sum()[-1]
                        top5_sum = df_to_export.sum()[-1]
                        others_df = df_to_export.append({'Model': 'Others', 'size': all_model_size_sum - top5_sum}, ignore_index=True)
                        others_df['error_count_sum'] = all_model_size_sum
                        srq_statistic_df_dict = others_df.to_dict(orient='records')
                        search_type = 'errorcode'

                    # if user is searching for models
                    else:
                        srq_count_series = srq_fields_df_copy.groupby(['ErrorCode']).size()
                        srq_statistic_df = srq_count_series.to_frame(name = 'size').reset_index().sort_values(['size'], ascending=False)
                        srq_statistic_df.reset_index(drop=True, inplace=True)
                        df_to_export = srq_statistic_df.iloc[0:5]
                        all_model_size_sum = srq_statistic_df.sum()[-1]
                        top5_sum = df_to_export.sum()[-1]
                        others_df = df_to_export.append({'ErrorCode': 'Others', 'size': all_model_size_sum - top5_sum}, ignore_index=True)
                        others_df['error_count_sum'] = all_model_size_sum
                        srq_statistic_df_dict = others_df.to_dict(orient='records')
                        search_type = 'model'

                    data_source = 'both'

                    # handles user data
                    ## getting the hostname by socket.gethostname() method
                    hostname = socket.gethostname()
                    ## getting the IP address using socket.gethostbyname() method
                    ip_address = socket.gethostbyname(hostname)
                    ## printing the hostname and ip_address
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='Perform both historical_errorcode search')

                    context = {
                    # 'filter': srqs_filter,
                    # 'cases_filter': cases_filter,
                    'search_type': search_type,
                    'error_count_sum': error_count_sum,
                    'data_source': data_source,
                    'cases_a': cases_a,
                    'cases_chart_data': cases_chart_data,
                    'd': d,
                    'srq_statistic_df_dict':srq_statistic_df_dict,
                    'cases_error_count_sum': cases_error_count_sum,
                    }
                    return render(request,'historical_errorcode.html',context)

                data_source = 'both'

                # handles user data
                ## getting the hostname by socket.gethostname() method
                hostname = socket.gethostname()
                ## getting the IP address using socket.gethostbyname() method
                ip_address = socket.gethostbyname(hostname)
                ## printing the hostname and ip_address
                Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='Perform both historical_errorcode search')

                context = {
                # 'filter': srqs_filter,
                # 'cases_filter': cases_filter,
                'search_type': search_type,
                'error_count_sum': error_count_sum,
                'data_source': data_source,
                'cases_a': cases_a,
                'cases_chart_data': cases_chart_data,
                'd': d,
                'cases_error_count_sum': cases_error_count_sum,
                }
                return render(request,'historical_errorcode.html',context)



@login_required
def historical_onsite(request):

    # handles user data
    ## getting the hostname by socket.gethostname() method
    hostname = socket.gethostname()
    ## getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)
    ## printing the hostname and ip_address
    connections.close_all()
    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='load historical onsite f2score page')

    # for test purpose, must be closed for production
    queryset = OSR.objects.exclude(F2score='nan').exclude(F2score__isnull=True)
    last_date_with_f2 = queryset.order_by('-Import_Date')[0].Import_Date
    f = OSRDateFilter(request.GET, queryset=queryset)
    if 'start_date' not in request.GET.keys():
        context = {
            'filter': f,
            'last_date_with_f2':last_date_with_f2,
        }
        return render(request, 'historical_onsite.html', context)

    if f.qs.count() < 10:
        # return HttpResponse("There is no enough data within the selected date.")
        context = {
            'filter': f,
            'error_msg': 'There is no enough data within the selected date. Please try with a longer period once again.'
        }
        return render(request, 'historical_onsite.html', context)

    df = pd.DataFrame(list(f.qs.values('F2score', 'Import_Date')))
    df.Import_Date = pd.to_datetime(df.Import_Date)
    df['F2score'] = df['F2score'].astype(float)
    df_2 = df.groupby(df.Import_Date.dt.strftime('%Y-%m')).F2score.agg(['mean'])
    df_2['mean'] = (df_2['mean'] * 100 ).round(2).fillna(0)
    labels = df_2.index.tolist()
    data = df_2['mean'].values.tolist()
    graph_data = '{"labels":'+ str(labels)+ ',\
            "datasets":\
                [{"label":"F2score","data":'+ str(data)+ ',\
            "fill":false,\
            "backgroundColor": "#800080",\
            "borderColor":"#800080"}]'
    context = {
            'filter': f,
            'graph_data': graph_data
    }
    return render(request, 'historical_onsite.html', context)

@login_required
def historical_keyword_result(request):
    connections.close_all()
    srqs_keyword_filter = SrqsKeywordsFilter(request.GET, queryset=SRQs.objects.all())

    # try:
    if request.method == 'GET':
        filter_class = request.GET.getlist('class')
        legend = filter_class
        # handles user data
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP addrex    ss using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='search historical_keyword ')

        allCategory = Keywords.objects.values('Class').distinct()
        keywords_for_query = Keywords.objects.filter(Class__in=filter_class)
        keywords_for_query_json = serializers.serialize('json', keywords_for_query)
        keywords_json =json.loads(keywords_for_query_json)
        if not request.GET._mutable:
                request.GET._mutable = True

        if request.GET['data_source'] == 'Cases':

            del request.GET['data_source']
            del request.GET['class']
            connections.close_all()
            cases_filter = CasesFilter(request.GET, queryset=Cases.objects.all())
            cases_filter_processing = list(cases_filter.qs.values())
            ## provide error messages when there are no data matching search conditions
            if cases_filter_processing == []:
                srqs_keyword_filter = SrqsKeywordsFilter(request.GET, queryset=SRQs.objects.all())
                allCategory = Keywords.objects.values('Class').distinct()
                error_msg = 'There is no data with your search conditions so far.'
                context = {
                    'srqs_keyword_filter': srqs_keyword_filter,
                    'allCategory': allCategory,
                    'error_msg': error_msg,
                }
                return render(request, 'historical_keyword.html',context)


            cases_filter_processing_list = []
            for i in cases_filter_processing:
                cases_filter_processing_list.append({'model': 'text.cases', 'fields': i})
            # srqs_filter_json = serializers.serialize('json', srqs_filter.qs)
            cases_filter_json = json.dumps(cases_filter_processing_list, indent=4, sort_keys=True, default=str)
            cases_json = json.loads(cases_filter_json)
            r = s.get(algorithm_ip + ':4546', json={'json1':keywords_json, 'json3':cases_json})

            # # Handles line chart
            data = json.loads(r.text)
            f = open('phase2_output.json', 'w+')
            f.write(r.text)
            f.close()
            cases_json_result= json.loads(data['json3'])
            lat,lng = [],[]
            for i in cases_json_result:
                lng.append(i['fields']['CreatedDate'])
                lat.append(i['fields']['Class'])
            df = pd.DataFrame([lat, lng]).T
            df['CreatedDate'] = pd.to_datetime(df[1], format='%Y-%m-%d %H:%M:%S')
            df['Class'] = (df[0])
            df['week'] = df['CreatedDate'].dt.strftime('%Y-%V')
            weekly_df = df.groupby(['Class', 'week']).size().rename('counts').reset_index()
            dict_to_draw_line_charts = weekly_df.to_dict('split')
            class_amount = weekly_df['Class'].nunique()
            labels_cases = []
            for i in dict_to_draw_line_charts['data']:
                if i[1] not in labels_cases:
                    labels_cases.append(i[1])
            labels_cases.sort()
            # step = len(labels_cases)
            data_to_draw_cases = []
            for i in legend:
                data_to_draw_cases.append({'label': i, 'data':[] , 'fill': 'false', 'borderColor': ''})
            color = ['red', 'rgb(11,255,12)', 'rgb(255,11,255)', 'rgb(11,11,255)', 'rgb(255,128,0)', 'rgb(22,100,112)']
            for i in range(len(data_to_draw_cases)):
                data_to_draw_cases[i]['borderColor'] = color[i]
            ## make sure all the keywords have statistics
            for i in data_to_draw_cases:
                for j in range(len(labels_cases)):
                    i['data'].append(0)

            for i in dict_to_draw_line_charts['data']:
                for j in data_to_draw_cases:
                    if i[0] == j['label']:
                        j['data'][labels_cases.index(i[1])] = i[2]


        elif request.GET['data_source'] == 'SRQs':
            del request.GET['data_source']
            del request.GET['class']
            connections.close_all()
            srqs_filter = SrqsFilter(request.GET, queryset=SRQs.objects.all())
            tmpsrq_filter = TMPSrqsFilter(request.GET, queryset=TMPSRQ.objects.all())

            tmpsrq_df = list(tmpsrq_filter.qs.values())
            srqs_filter_processing = list(srqs_filter.qs.values())
            srqs_filter_processing.extend(tmpsrq_df)

            if srqs_filter_processing == []:
                srqs_keyword_filter = SrqsKeywordsFilter(request.GET, queryset=SRQs.objects.all())
                allCategory = Keywords.objects.values('Class').distinct()
                error_msg = 'There is no data with your search conditions so far.'
                context = {
                    'srqs_keyword_filter': srqs_keyword_filter,
                    'allCategory': allCategory,
                    'error_msg': error_msg,
                }
                return render(request, 'historical_keyword.html',context)

            srqs_filter_processing_list = []
            for i in srqs_filter_processing:
                srqs_filter_processing_list.append({'model': 'text.srqs', 'fields': i})
            # srqs_filter_json = serializers.serialize('json', srqs_filter.qs)
            srqs_filter_json = json.dumps(srqs_filter_processing_list, indent=4, sort_keys=True, default=str)
            srqs_json = json.loads(srqs_filter_json)
            r = s.get(algorithm_ip + ':4546', json={'json1':keywords_json, 'json2':srqs_json})

            # # Handles line chart
            data = json.loads(r.text)
            f = open('phase2_output.json', 'w+')
            f.write(r.text)
            f.close()
            srqs_json_result= json.loads(data['json2'])
            lat,lng = [],[]
            for i in srqs_json_result:
                lng.append(i['fields']['CreatedDate'])
                lat.append(i['fields']['Class'])
            df = pd.DataFrame([lat, lng]).T
            df['CreatedDate'] = pd.to_datetime(df[1], format='%Y-%m-%d %H:%M:%S')
            df['Class'] = (df[0])
            df['week'] = df['CreatedDate'].dt.strftime('%Y-%V')
            weekly_df = df.groupby(['Class', 'week']).size().rename('counts').reset_index()
            dict_to_draw_line_charts = weekly_df.to_dict('split')
            class_amount = weekly_df['Class'].nunique()

            labels = []
            for i in dict_to_draw_line_charts['data']:
                if i[1] not in labels:
                    labels.append(i[1])
            labels.sort()
            data_to_draw = []
            for i in legend:
                data_to_draw.append({'label': i, 'data':[] , 'fill': 'false', 'borderColor': ''})
            color = ['red', 'rgb(11,255,12)', 'rgb(255,11,255)', 'rgb(11,11,255)', 'rgb(255,128,0)', 'rgb(22,100,112)']
            for i in range(len(data_to_draw)):
                data_to_draw[i]['borderColor'] = color[i]
            for i in data_to_draw:
                for j in range(len(labels)):
                    i['data'].append(0)
            for i in dict_to_draw_line_charts['data']:
                for j in data_to_draw:
                    if i[0] == j['label']:
                        j['data'][labels.index(i[1])] = i[2]

        elif request.GET['data_source'] == 'both':
            del request.GET['data_source']
            del request.GET['class']
            connections.close_all()
            cases_filter = CasesFilter(request.GET, queryset=Cases.objects.all())
            # cases_filter_json = serializers.serialize('json', cases_filter.qs)
            cases_filter_processing = list(cases_filter.qs.values())

            ## provide error messages when there are no data matching search conditions
            if cases_filter_processing == []:
                srqs_keyword_filter = SrqsKeywordsFilter(request.GET, queryset=SRQs.objects.all())
                allCategory = Keywords.objects.values('Class').distinct()
                error_msg = 'There is no data with your search conditions so far.'
                context = {
                    'srqs_keyword_filter': srqs_keyword_filter,
                    'allCategory': allCategory,
                    'error_msg': error_msg,
                }
                return render(request, 'historical_keyword.html',context)

            cases_filter_processing_list = []
            for i in cases_filter_processing:
                cases_filter_processing_list.append({'model': 'text.cases', 'fields': i})
            # srqs_filter_json = serializers.serialize('json', srqs_filter.qs)
            cases_filter_json = json.dumps(cases_filter_processing_list, indent=4, sort_keys=True, default=str)
            cases_json = json.loads(cases_filter_json)
            print('it has finished processing json file')
            srqs_filter = SrqsFilter(request.GET, queryset=SRQs.objects.all())
            tmpsrq_filter = TMPSrqsFilter(request.GET, queryset=TMPSRQ.objects.all())
            tmpsrq_df = list(tmpsrq_filter.qs.values())
            srqs_filter_processing = list(srqs_filter.qs.values())
            srqs_filter_processing.extend(tmpsrq_df)

            ## provide error messages when there are no data matching search conditions
            if srqs_filter_processing == []:
                srqs_keyword_filter = SrqsKeywordsFilter(request.GET, queryset=SRQs.objects.all())
                allCategory = Keywords.objects.values('Class').distinct()
                error_msg = 'There is no data with your search conditions so far.'
                context = {
                    'srqs_keyword_filter': srqs_keyword_filter,
                    'allCategory': allCategory,
                    'error_msg': error_msg,
                }
                return render(request, 'historical_keyword.html',context)

            srqs_filter_processing_list = []
            for i in srqs_filter_processing:
                srqs_filter_processing_list.append({'model': 'text.srqs', 'fields': i})
            # srqs_filter_json = serializers.serialize('json', srqs_filter.qs)
            srqs_filter_json = json.dumps(srqs_filter_processing_list, indent=4, sort_keys=True, default=str)
            srqs_json = json.loads(srqs_filter_json)
            r = s.get(algorithm_ip + ':4546', json={'json1':keywords_json, 'json2':srqs_json, 'json3':cases_json})
            # Handles line chart
            data = json.loads(r.text)
            f = open('phase2_output.json', 'w+')
            f.write(r.text)
            f.close()
            srqs_json_result= json.loads(data['json2'])
            cases_json_result= json.loads(data['json3'])
            lat,lng = [],[]
            for i in srqs_json_result:
                lng.append(i['fields']['CreatedDate'])
                lat.append(i['fields']['Class'])
            df = pd.DataFrame([lat, lng]).T
            df['CreatedDate'] = pd.to_datetime(df[1], format='%Y-%m-%d %H:%M:%S')
            df['Class'] = (df[0])
            df['week'] = df['CreatedDate'].dt.strftime('%Y-%V')
            weekly_df = df.groupby(['Class', 'week']).size().rename('counts').reset_index()
            dict_to_draw_line_charts = weekly_df.to_dict('split')
            labels = []
            for i in dict_to_draw_line_charts['data']:
                if i[1] not in labels:
                    labels.append(i[1])
            labels.sort()
            data_to_draw = []
            for i in legend:
                data_to_draw.append({'label': i, 'data':[] , 'fill': 'false', 'borderColor': ''})
            color = ['red', 'rgb(11,255,12)', 'rgb(255,11,255)', 'rgb(11,11,255)', 'rgb(255,128,0)', 'rgb(22,100,112)']
            for i in range(len(data_to_draw)):
                data_to_draw[i]['borderColor'] = color[i]
            ## make sure all the keywords have statistics
            for i in data_to_draw:
                for j in range(len(labels)):
                    i['data'].append(0)

            for i in dict_to_draw_line_charts['data']:
                for j in data_to_draw:
                    if i[0] == j['label']:
                        j['data'][labels.index(i[1])] = i[2]

            lat,lng = [],[]
            for i in cases_json_result:
                lng.append(i['fields']['CreatedDate'])
                lat.append(i['fields']['Class'])
            df = pd.DataFrame([lat, lng]).T
            df['CreatedDate'] = pd.to_datetime(df[1], format='%Y-%m-%d %H:%M:%S')
            df['Class'] = (df[0])
            df['week'] = df['CreatedDate'].dt.strftime('%Y-%V')
            weekly_df = df.groupby(['Class', 'week']).size().rename('counts').reset_index()
            dict_to_draw_line_charts = weekly_df.to_dict('split')
            class_amount = weekly_df['Class'].nunique()
            labels_cases = []
            for i in dict_to_draw_line_charts['data']:
                if i[1] not in labels_cases:
                    labels_cases.append(i[1])
            labels_cases.sort()
            # step = len(labels_cases)
            data_to_draw_cases = []
            for i in legend:
                data_to_draw_cases.append({'label': i, 'data':[] , 'fill': 'false', 'borderColor': ''})
            color = ['red', 'rgb(11,255,12)', 'rgb(255,11,255)', 'rgb(11,11,255)', 'rgb(255,128,0)', 'rgb(22,100,112)']
            for i in range(len(data_to_draw_cases)):
                data_to_draw_cases[i]['borderColor'] = color[i]
            ## make sure all the keywords have statistics
            for i in data_to_draw_cases:
                for j in range(len(labels_cases)):
                    i['data'].append(0)

            for i in dict_to_draw_line_charts['data']:
                for j in data_to_draw_cases:
                    if i[0] == j['label']:
                        j['data'][labels_cases.index(i[1])] = i[2]


        # To Do: apply Filters

        data = json.loads(r.text)
        f = open('phase2_output.json', 'w+')
        f.write(str(data))
        f.close()
        if 'json2' in data.keys():
            analytics = {}
            srqs_json_result= json.loads(data['json2'])
            if type(srqs_json_result) == list:
                for i in legend:
                    analytics[i] = 0
                for i in srqs_json_result:
                    analytics[i['fields']['Class']] += 1

            analytics_to_display = []
            for key, value in analytics.items():
                analytics_to_display.append({"class":key, "amount":value})
            analytics_to_display_list_cat = []
            analytics_to_display_list_data = []
            for key, value in analytics.items():
                analytics_to_display_list_cat.append(key)
                analytics_to_display_list_data.append(value)
            # for i in legend:
            #     if i not in analytics_to_display_list_cat:
            #         analytics_to_display_list_cat.append(i)
            #         analytics_to_display_list_data.append(0)

        if 'json3' in data.keys():
            cases_json_result= json.loads(data['json3'])
            analytics = {}

            if type(cases_json_result) == list:
                for i in legend:
                    analytics[i] = 0
                for i in cases_json_result:
                    analytics[i['fields']['Class']] += 1

            analytics_to_display_cases = []
            for key, value in analytics.items():
                analytics_to_display_cases.append({"class":key, "amount":value})

            analytics_to_display_list_cat_cases = []
            analytics_to_display_list_data_cases = []
            for key, value in analytics.items():
                analytics_to_display_list_cat_cases.append(key)
                analytics_to_display_list_data_cases.append(value)


        # prepares the excel file

        workbook = xlsxwriter.Workbook("Historical Keyword Summary Data.xlsx")
        if 'json2' in data.keys():
            worksheet1 = workbook.add_worksheet('SRQs')
            # Sheet header, first row
            row_num = 0

            cell_format = workbook.add_format()
            cell_format.set_bold()

            columns = ['SRNumber', 'SRType', 'CreatedDate', 'Model', 'SerialNumber', 'InternalNotes', 'Class']

            for col_num in range(len(columns)):
                worksheet1.write(row_num, col_num, columns[col_num], cell_format)

            # Sheet body, remaining rows

            for i in srqs_json_result:
                list_to_write = [i['fields']['SRNumber'], i['fields']['SRType'], i['fields']['CreatedDate'], i['fields']['Model'], i['fields']['SerialNumber'], i['fields']['InternalNotes'], i['fields']['Class']]
            # rows = srqs_json_result.values_list('SRNumber', 'SRType', 'CreatedDate', 'Model','SerialNumber', 'InternalNotes', 'Class')
            # for row in rows:
                row_num += 1
                for col_num in range(len(list_to_write)):
                    worksheet1.write(row_num, col_num, list_to_write[col_num])
        if 'json3' in data.keys():
            worksheet2 = workbook.add_worksheet('Cases')
            # Sheet header, first row
            row_num = 0

            cell_format = workbook.add_format()
            cell_format.set_bold()

            columns = ['CaseNumber', 'CreatedDate', 'Model', 'SerialNumber', 'Symptom', 'Diagnosis', 'Description',	'Class']

            for col_num in range(len(columns)):
                worksheet2.write(row_num, col_num, columns[col_num], cell_format)

            # Sheet body, remaining rows

            for i in cases_json_result:
                list_to_write = [i['fields']['CaseNumber'], i['fields']['CreatedDate'], i['fields']['Model'], i['fields']['SerialNumber'], i['fields']['Symptom'], i['fields']['Diagnosis'], i['fields']['Description'], i['fields']['Class']]
            # rows = srqs_json_result.values_list('SRNumber', 'SRType', 'CreatedDate', 'Model','SerialNumber', 'InternalNotes', 'Class')
            # for row in rows:
                row_num += 1
                for col_num in range(len(list_to_write)):
                    worksheet2.write(row_num, col_num, list_to_write[col_num])

        worksheet3 = workbook.add_worksheet('Static')

        row_num = 0

        cell_format = workbook.add_format()
        cell_format.set_bold()

        if 'json3' in data.keys() and 'json2' in data.keys():
            columns = ['Class', 'Corresponding SRQ Number ', 'Corresponding Case Number']


            for col_num in range(len(columns)):
                worksheet3.write(row_num, col_num, columns[col_num], cell_format)

        ## TODO
        # Sheet body, remaining rows
            analytics_to_write_to_excel_cases = {}

            if type(cases_json_result) == list:
                for i in cases_json_result:
                    if i['fields']['Class'] not in analytics_to_write_to_excel_cases.keys():
                        analytics_to_write_to_excel_cases[i['fields']['Class']] = [i['fields']['CaseNumber']]
                    else:
                        analytics_to_write_to_excel_cases[i['fields']['Class']].append(i['fields']['CaseNumber'])

            analytics_to_write_to_excel_srqs = {}
            for i in analytics_to_write_to_excel_cases.keys():
                analytics_to_write_to_excel_srqs[i]=[]

            if type(srqs_json_result) == list:
                for i in srqs_json_result:
                    if i['fields']['Class'] not in analytics_to_write_to_excel_srqs.keys():
                        analytics_to_write_to_excel_srqs[i['fields']['Class']] = [i['fields']['SRNumber']]
                    else:
                        analytics_to_write_to_excel_srqs[i['fields']['Class']].append(i['fields']['SRNumber'])


            for key, value in analytics_to_write_to_excel_srqs.items():

                row_num += 1
                worksheet3.write(row_num, 0, str(key))
                worksheet3.write(row_num, 1, str(value).replace('[','').replace(']','').replace('\'',''))

            row_num = 0
            for key, value in analytics_to_write_to_excel_cases.items():
                row_num += 1
                if analytics_to_write_to_excel_srqs.keys() == analytics_to_write_to_excel_cases.keys():
                    worksheet3.write(row_num, 2, str(value).replace('[','').replace(']','').replace('\'',''))

        elif 'json2' in data.keys():
            columns = ['Class', 'Corresponding SRQ Number']


            for col_num in range(len(columns)):
                worksheet3.write(row_num, col_num, columns[col_num], cell_format)

        ## TODO
        # Sheet body, remaining rows

            analytics_to_write_to_excel_srqs = {}
            # for i in analytics_to_write_to_excel_cases.keys():
            #     analytics_to_write_to_excel_srqs[i]=[]

            if type(srqs_json_result) == list:
                for i in srqs_json_result:
                    if i['fields']['Class'] not in analytics_to_write_to_excel_srqs.keys():
                        analytics_to_write_to_excel_srqs[i['fields']['Class']] = [i['fields']['SRNumber']]
                    else:
                        analytics_to_write_to_excel_srqs[i['fields']['Class']].append(i['fields']['SRNumber'])


            for key, value in analytics_to_write_to_excel_srqs.items():

                row_num += 1
                worksheet3.write(row_num, 0, str(key))
                worksheet3.write(row_num, 1, str(value))

            del analytics_to_write_to_excel_srqs

        elif 'json3' in data.keys():
            columns = ['Class', 'Corresponding Case Number']


            for col_num in range(len(columns)):
                worksheet3.write(row_num, col_num, columns[col_num], cell_format)

        ## TODO
        # Sheet body, remaining rows
            analytics_to_write_to_excel_cases = {}

            if type(cases_json_result) == list:
                for i in cases_json_result:
                    if i['fields']['Class'] not in analytics_to_write_to_excel_cases.keys():
                        analytics_to_write_to_excel_cases[i['fields']['Class']] = [i['fields']['CaseNumber']]
                    else:
                        analytics_to_write_to_excel_cases[i['fields']['Class']].append(i['fields']['CaseNumber'])

            row_num = 0
            for key, value in analytics_to_write_to_excel_cases.items():
                row_num += 1
                worksheet3.write(row_num, 2, str(value))

            del analytics_to_write_to_excel_cases

        worksheet4 = workbook.add_worksheet('Rule')

        row_num = 0

        cell_format = workbook.add_format()
        cell_format.set_bold()

        columns = ['Class', 'Rule', 'Action']

        for col_num in range(len(columns)):
            worksheet4.write(row_num, col_num, columns[col_num], cell_format)


        rows = Keywords.objects.all().values_list('Class', 'Rule', 'Action')
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                worksheet4.write(row_num, col_num, row[col_num])


        workbook.close()


        # handles user data
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        connections.close_all()
        Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='load latest keyword page')

        ## Garbage collection
        del df, weekly_df, hostname, ip_address, worksheet4, row_num
        gc.collect()

        if 'json2' in data.keys() and 'json3' in data.keys():

            context = {
                'allCategory': allCategory,
                'srqs_keyword_filter': srqs_keyword_filter,
                'filter_class': filter_class,
                'analytics_to_display': analytics_to_display,
                'analytics_to_display_list_cat': analytics_to_display_list_cat,
                'analytics_to_display_list_data': analytics_to_display_list_data,
                'keywords_for_query_json': keywords_for_query_json,
                'analytics_to_display_cases': analytics_to_display_cases,
                'analytics_to_display_list_cat_cases': analytics_to_display_list_cat_cases,
                'analytics_to_display_list_data_cases': analytics_to_display_list_data_cases,
                'labels': labels,
                'data_to_draw': data_to_draw,
                'labels_cases': labels_cases,
                'data_to_draw_cases': data_to_draw_cases,
                'legend': legend,
            }

        elif 'json3' in data.keys():
            context = {
                'allCategory': allCategory,
                'srqs_keyword_filter': srqs_keyword_filter,
                'filter_class': filter_class,
                'keywords_for_query_json': keywords_for_query_json,
                'analytics_to_display_cases': analytics_to_display_cases,
                'analytics_to_display_list_cat_cases': analytics_to_display_list_cat_cases,
                'analytics_to_display_list_data_cases': analytics_to_display_list_data_cases,
                'labels_cases': labels_cases,
                'data_to_draw_cases': data_to_draw_cases,
                'legend': legend,

            }

        else:
            context = {
                'allCategory': allCategory,
                'srqs_keyword_filter': srqs_keyword_filter,
                'filter_class': filter_class,
                'analytics_to_display': analytics_to_display,
                'analytics_to_display_list_cat': analytics_to_display_list_cat,
                'analytics_to_display_list_data': analytics_to_display_list_data,
                'keywords_for_query_json': keywords_for_query_json,
                'labels': labels,
                'data_to_draw': data_to_draw,
                'legend': legend,

            }

        # Render the HTML template index.html with the data in the context variable
        return render(request, 'historical_keyword.html', context)


    # except:
    #     print('expeption happened.')
    #     logging.exception("str(request.GET)"+" has resulted in errors.")
    #     srqs_keyword_filter = SrqsKeywordsFilter(request.GET, queryset=SRQs.objects.all())
    #     allCategory = Keywords.objects.values('Class').distinct()
    #     error_msg = 'Unknown error happened when trying to draw the charts. You can download the result with "Export Summary Data" button. Please help us to report the search conditions you specified. Much thanks.'
    #     context = {
    #         'srqs_keyword_filter': srqs_keyword_filter,
    #         'allCategory': allCategory,
    #         'error_msg': error_msg,

    #     }
    #     return render(request, 'historical_keyword.html',context)

@login_required
def historical_keyword(request):

    try:
        connections.close_all()
        srqs_keyword_filter = SrqsKeywordsFilter(request.GET, queryset=SRQs.objects.all())
        allCategory = Keywords.objects.values('Class').distinct()
        firstload = 'Please enter the search fields, and press Submit to start the search.'

        context = {
            'srqs_keyword_filter': srqs_keyword_filter,
            'allCategory': allCategory,
            'firstload': firstload,
        }
        return render(request, 'historical_keyword.html',context)

    except:
        print('expeption happened.')
        logging.error("Loading historical error page has come across errors.")
        srqs_keyword_filter = SrqsKeywordsFilter(request.GET, queryset=SRQs.objects.all())
        allCategory = Keywords.objects.values('Class').distinct()
        error_msg = 'Unknown error happened when trying load the page. Please help us to report the conditions, including which page you were and which user you are. Much thanks.'
        context = {
            'srqs_keyword_filter': srqs_keyword_filter,
            'allCategory': allCategory,
            'error_msg': error_msg,

        }
        return render(request, 'historical_keyword.html',context)


class ParseExcel(APIView):
    """Handle the keyword upload function"""

    def post(self, request, format=None):
        # try:
            form = forms.ClassificationSearchForm()
            excel_file = request.FILES['file2upload']
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            # handles user data
            ## getting the hostname by socket.gethostname() method
            hostname = socket.gethostname()
            ## getting the IP address using socket.gethostbyname() method
            ip_address = socket.gethostbyname(hostname)


            # Distinguish which file is it
            # Handles the keyword mapping table
            if "Keywords Mapping Table" in (str(excel_file).split('.')[0] ):
                ## Foolproof
                xl = pd.ExcelFile(excel_file)
                if 'Sheet1' not in xl.sheet_names:
                    error_title = 'Sheet name is incorrect.'


                    context = {
                        'error_msg': 'For Keywords Mapping Table, please check if your file contains a sheet named \'Sheet1\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)
                keyword = xl.parse("Sheet1")
                if all(x in list(keyword.columns) for x in ['Class', 'Rule', 'Action']):
                    connections.close_all()
                    Keywords.objects.all().delete()
                    keyword.dropna(subset=['Class', 'Rule', 'Action'], inplace=True)
                    keyword.drop_duplicates(subset =['Class', 'Rule', 'Action'], keep='last', inplace = True)
                    keyword.reset_index(drop=True, inplace=True)
                    objs = []
                    for i in range(len(keyword['Class'])):
                        objs.append(Keywords(
                                    Class= str(keyword['Class'][i]),
                                    Rule= str(keyword['Rule'][i]),
                                    Action= (str(keyword['Action'][i])),
                        ))
                    connections.close_all()
                    newlyCreatedCases = Keywords.objects.bulk_create(objs)


                    ## printing the hostname and ip_address
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='Upload keywords definition')


                    context = {
                        'upload_success_msg': "You have successfully updated the keyword mapping table",
                        'form': form,
                        }
                    return render(request,'latest_errorcode.html', context)

                else:

                    error_title = 'Some columns are missing.'
                    ## printing the hostname and ip_address
                    connections.close_all()
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='upload keyword definition failed.')


                    context = {
                        'error_msg': 'For update data, please check if your file starts with \"INNOLUX Customer Support Report \", with .xlsx format. The sheet named \"Cases\" should contains columns named \'CaseNumber\', \'Model\', \'CreatedDate\', \'SerialNumber\', \'Symptom\', \'Description\', \'Diagnosis\'',
                        'error_title': error_title,
                    }

                    return render(request, 'error.html', context)
            elif "Defect Code Mapping Table" in (str(excel_file).split('.')[0] ):
                ## Foolproof
                xl = pd.ExcelFile(excel_file)
                if 'Sheet1' not in xl.sheet_names:
                    error_title = 'Sheet name is incorrect.'

                    context = {
                        'error_msg': 'For Defect Code Mapping Table, please check if your file contains a sheet named \'Sheet1\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)
                defect_code = xl.parse("Sheet1")
                if all(x in list(defect_code.columns) for x in ['Code', 'Symptom']):
                    connections.close_all()
                    Defect.objects.all().delete()
                    defect_code.dropna(subset=['Code', 'Symptom'], inplace=True)
                    defect_code.drop_duplicates(subset =['Code', 'Symptom'], keep='last', inplace = True)
                    defect_code.reset_index(drop=True, inplace=True)
                    objs = []
                    for i in range(len(defect_code['Code'])):
                        objs.append(Defect(
                                    Code= str(defect_code['Code'][i]),
                                    Symptom= str(defect_code['Symptom'][i]),
                        ))
                    connections.close_all()
                    newlyCreatedDefect = Defect.objects.bulk_create(objs)


                    ## printing the hostname and ip_address
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='Upload defect code mapping table')


                    context = {
                        'upload_success_msg': "You have successfully updated the defect code mapping table",
                        'form': form,
                        }
                    return render(request,'latest_errorcode.html', context)

                else:
                    error_title = 'Some columns are missing.'

                    connections.close_all()
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='upload defect code mapping table failed.')



                    context = {
                        'error_msg': 'For update defect code mapping table, please check if in "Sheet1", there are two columns named \'Code\', \'Symptom\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)
                    ## printing the hostname and ip_address

            # Handles customer Support Report
            elif "INNOLUX Customer Support Report" in str(excel_file).split('.')[0]:
                ## Foolproof

                xl = pd.ExcelFile(excel_file)
                if not all(x in xl.sheet_names for x in ['Cases', 'SRQs']):
                    error_title = 'Sheet name is incorrect.'

                    context = {
                        'error_msg': 'For INNOLUX Customer Support Report, please check if your file contains sheets named \'Cases\' and \'SRQs\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)
                srq = xl.parse("SRQs")
                srq.dropna(subset=['SRNumber', 'InternalNotes', 'ErrorCode', 'Model', 'CreatedDate', 'SerialNumber'], inplace=True)
                srq.drop_duplicates(subset ="SRNumber", keep='last', inplace = True)
                srq.reset_index(drop=True, inplace=True)

                case = xl.parse("Cases")
                case.dropna(subset=['CaseNumber', 'CreatedDate', 'Model', 'SerialNumber', 'Description'], inplace=True)
                case.drop_duplicates(subset ="CaseNumber", keep='last', inplace = True)
                case.reset_index(drop=True, inplace=True)


                if (all(x in list(case.columns) for x in ['CaseNumber', 'Model', 'CreatedDate', 'SerialNumber', 'Symptom', 'Description', 'Diagnosis'])) and (all(y in list(srq.columns) for y in ['SRNumber', 'Model', 'CreatedDate', 'SerialNumber', 'SRType', 'ErrorCode', 'InternalNotes'])):
                    case = case[['CaseNumber', 'Model', 'CreatedDate', 'SerialNumber', 'Symptom', 'Description', 'Diagnosis']]
                    srq = srq [['SRNumber', 'Model', 'CreatedDate', 'SerialNumber', 'SRType', 'ErrorCode', 'InternalNotes']]
                    cases_dict = case.astype(str).to_dict(orient='records')
                    srqs_dict = srq.astype(str).to_dict(orient='records')
                    cases_json = pd.DataFrame({'model': 'text.cases', 'fields': cases_dict}).to_dict('records')
                    srqs_json = pd.DataFrame({'model': 'text.srqs', 'fields': srqs_dict}).to_dict('records')
                    ## TODO: send request to algorithm phase 1
                    srqs_json = json.dumps(srqs_json,cls=DjangoJSONEncoder)
                    cases_json = json.dumps(cases_json, cls=DjangoJSONEncoder)
                    srqs_json = json.loads(srqs_json)
                    cases_json = json.loads(cases_json)
                    # try:
                    #     r = s.get('http://10.55.14.167:4547', json={"srqs":srqs_json, 'mode':'Pred'}, timeout=None)
                    # except requests.exceptions.RequestException as e:
                    #     print(e)
                    # print(time.strftime('%Y-%m-%d %H:%M:%S'), ' Received SRQs prediction result')
                    r = s.get(algorithm_ip + ':4547', json={"srqs":srqs_json, 'mode':'Pred'})
                    time.sleep(10)
                    t = s.get(algorithm_ip + ':4547/restart', json={'mode':'Restart'}, timeout=None)
                    time.sleep(40)
                    if r.status_code != 200:
                        error_title = 'The algorithm did not answered correctly.'
                        context = {
                            'error_msg': 'Please kindly send us the file you uploaded for debugging. Much thanks.',
                            'error_title': error_title,
                        }
                        return render(request, 'latest_name_error.html', context)
                    srqs_json_raw= json.loads(r.text)
                    srqs_json_result= json.loads(srqs_json_raw['predict_result'])
                    result = {}
                    result['accuracy'] = srqs_json_raw['accuracy']
                    result['date'] = datetime.date.today().strftime("%Y-%m-%d")
                    request.session['result'] = result
                    r = s.get(algorithm_ip + ':4547', json={"cases":cases_json, 'mode':'Pred'})
                    time.sleep(10)
                    t = s.get(algorithm_ip + ':4547/restart', json={'mode':'Restart'}, timeout=None)
                    # try:
                    #     r = s.get('http://10.55.14.167:4547', json={"srqs":cases_json, 'mode':'Pred'}, timeout=None)
                    # except requests.exceptions.RequestException as e:
                    #     print(e)
                    # print(time.strftime('%Y-%m-%d %H:%M:%S'), ' Received Cases prediction result')

                    if r.status_code != 200:
                        error_title = 'The algorithm did not answered correctly.'
                        context = {
                            'error_msg': 'Please kindly send us the file you uploaded for debugging. Much thanks.',
                            'error_title': error_title,
                        }
                        return render(request, 'latest_name_error.html', context)
                    cases_json_raw = json.loads(r.text)
                    cases_json_result=  json.loads(cases_json_raw['predict_result'])

                    connections.close_all()
                    # applying bulk create

                    caseNumberindb_list = set(i.CaseNumber for i in Cases.objects.all())
                    objs = []
                    for idx, i in enumerate(cases_json_result):
                        if str(i['fields']['CaseNumber']) not in caseNumberindb_list:
                            if str(i['fields']['CreatedDate']).isnumeric():
                                objs.append(Cases(
                                    CaseNumber=str(i['fields']['CaseNumber']),
                                    CreatedDate= datetime.datetime.fromtimestamp(i['fields']['CreatedDate']/1000.0),
                                    Model=str(i['fields']['Model']),
                                    SerialNumber=str(i['fields']['SerialNumber']),
                                    Symptom=str(i['fields']['Symptom']),
                                    Diagnosis=str(i['fields']['Diagnosis']),
                                    Description=str(i['fields']['Description']),
                                    PredictErrorCode=str(i['fields']['PredictErrorCode'])
                                ))
                            else:
                                objs.append(Cases(
                                    CaseNumber=str(i['fields']['CaseNumber']),
                                    CreatedDate= parser.parse(str(i['fields']['CreatedDate'])),
                                    Model=str(i['fields']['Model']),
                                    SerialNumber=str(i['fields']['SerialNumber']),
                                    Symptom=str(i['fields']['Symptom']),
                                    Diagnosis=str(i['fields']['Diagnosis']),
                                    Description=str(i['fields']['Description']),
                                    PredictErrorCode=str(i['fields']['PredictErrorCode'])
                                ))

                    connections.close_all()
                    newlyCreatedCases = Cases.objects.bulk_create(objs)
                    SRNumberindb = SRQs.objects.values('SRNumber')
                    SRNumberinTMPSRQ = TMPSRQ.objects.values('SRNumber')
                    SRNumberindb_list = []
                    objs = []
                    for i in SRNumberindb:
                        SRNumberindb_list.append(i['SRNumber'])

                    for i in SRNumberinTMPSRQ:
                        SRNumberindb_list.append(i['SRNumber'])

                    for idx, i in enumerate(srqs_json_result):
                        if str(i['fields']['SRNumber']) not in SRNumberindb_list:
                            if str(i['fields']['CreatedDate']).isnumeric():
                                objs.append(TMPSRQ(
                                    SRNumber= i['fields']['SRNumber'],
                                    SRType= str(i['fields']['SRType']),
                                    CreatedDate= pd.to_datetime(i['fields']['CreatedDate']),
                                    Model= (str(i['fields']['Model']).upper()),
                                    SerialNumber= str(i['fields']['SerialNumber']),
                                    ErrorCode= str(i['fields']['ErrorCode']),
                                    InternalNotes= str(i['fields']['InternalNotes']),
                                    PredictErrorCode=str(i['fields']['PredictErrorCode']),
                                    Train=bool(strtobool(i['fields']['Train']))
                                ))
                            else:
                                objs.append(TMPSRQ(
                                    SRNumber= i['fields']['SRNumber'],
                                    SRType= str(i['fields']['SRType']),
                                    CreatedDate= parser.parse(str(i['fields']['CreatedDate'])),
                                    Model= (str(i['fields']['Model']).upper()),
                                    SerialNumber= str(i['fields']['SerialNumber']),
                                    ErrorCode= str(i['fields']['ErrorCode']),
                                    InternalNotes= str(i['fields']['InternalNotes']),
                                    PredictErrorCode=str(i['fields']['PredictErrorCode']),
                                    Train=bool(strtobool(i['fields']['Train']))
                                ))

                    newlyCreatedSRQs = TMPSRQ.objects.bulk_create(objs)
                    print('finished update db.')

                    srqs_json_result_dumps = json.dumps(srqs_json_result)
                    srq_df = pd.read_json(srqs_json_result_dumps)

                    # srq_fields_df = pd.DataFrame.from_dict(srq_df['fields'], orient='index')
                    srq_fields_df_copy = srq_df.copy()

                    for i in range(len(srq_df['model'])):
                        srq_fields_df_copy.at[i,'Model'] = srq_df.iloc[i]['fields']['Model']
                        srq_fields_df_copy.at[i,'ErrorCode'] = srq_df.iloc[i]['fields']['ErrorCode']

                    srq_count_series = srq_fields_df_copy.groupby(['Model', 'ErrorCode']).size()
                    srq_statistic_df = srq_count_series.to_frame(name = 'size').reset_index().sort_values(['Model','size'], ascending=False)
                    # case_statistic_df = case_statistic_df.groupby(['Model', 'PredictErrorCode']).sum().sort_values(['Model','size'], ascending=False)


                    srq_statistic_df_dict = srq_statistic_df.to_dict(orient='records')

                    problem_models_list = []
                    srq_statistic_to_draw = []
                    for i in srq_statistic_df_dict:
                        if i['Model'] not in problem_models_list:
                            srq_statistic_to_draw.append({'Model': i['Model'], 'statistic': [{'ErrorCode': i['ErrorCode'], 'error_count' :i['size']}], 'error_count_sum': i['size']})
                            problem_models_list.append(i['Model'])
                        else:
                            for j in srq_statistic_to_draw:
                                if j['Model'] == i['Model']:
                                    if len(j['statistic']) < 5:
                                        j['statistic'].append({'ErrorCode': i['ErrorCode'], 'error_count' :i['size']})
                                        j['error_count_sum'] += i['size']
                                    elif len(j['statistic']) == 5:
                                        j['statistic'].append({'ErrorCode': 'Others', 'error_count' :i['size']})
                                        j['error_count_sum'] += i['size']
                                    else:
                                        j['statistic'][5]['error_count'] += i['size']
                                        j['error_count_sum'] += i['size']

                    request.session['srq_statistic_to_draw'] = srq_statistic_to_draw

                    ## Handles Cases json to output graphs
                    cases_json_result_dumps = json.dumps(cases_json_result)
                    case_df = pd.read_json(cases_json_result_dumps)

                    case_fields_df_copy = case_df.copy()

                    for i in range(len(case_df['model'])):
                        case_fields_df_copy.at[i,'Model'] = case_df.iloc[i]['fields']['Model']
                        case_fields_df_copy.at[i,'PredictErrorCode'] = case_df.iloc[i]['fields']['PredictErrorCode']

                    case_count_series = case_fields_df_copy.groupby(['Model', 'PredictErrorCode']).size()
                    case_statistic_df = case_count_series.to_frame(name = 'size').reset_index().sort_values(['Model','size'], ascending=False)
                    # case_statistic_df = case_statistic_df.groupby(['Model', 'PredictErrorCode']).sum().sort_values(['Model','size'], ascending=False)


                    case_statistic_df_dict = case_statistic_df.to_dict(orient='records')

                    problem_models_list = []
                    case_statistic_to_draw = []
                    for i in case_statistic_df_dict:
                        if i['Model'] not in problem_models_list:
                            case_statistic_to_draw.append({'Model': i['Model'], 'statistic': [{'PredictErrorCode': i['PredictErrorCode'], 'error_count' :i['size']}], 'error_count_sum': i['size']})
                            problem_models_list.append(i['Model'])

                        else:
                            for j in case_statistic_to_draw:
                                if j['Model'] == i['Model']:
                                    if len(j['statistic']) < 5:
                                        j['statistic'].append({'PredictErrorCode': i['PredictErrorCode'], 'error_count' :i['size']})
                                        j['error_count_sum'] += i['size']
                                    elif len(j['statistic']) == 5:
                                        j['statistic'].append({'PredictErrorCode': 'Others', 'error_count' :i['size']})
                                        j['error_count_sum'] += i['size']
                                    else:
                                        j['statistic'][5]['error_count'] += i['size']
                                        j['error_count_sum'] += i['size']

                    request.session['case_statistic_to_draw'] = case_statistic_to_draw

                    ## Prepare Latest ErrorCode Summary Data
                    srqs_json_result_list = []
                    for i in srqs_json_result:
                        srqs_json_result_list.append(i['fields'])
                    srq_df = pd.DataFrame.from_records(srqs_json_result_list)

                    cases_json_result_list = []
                    for i in cases_json_result:
                        cases_json_result_list.append(i['fields'])
                    case_df = pd.DataFrame.from_records(cases_json_result_list)

                    with pd.ExcelWriter('Latest ErrorCode Summary Data.xlsx') as writer:
                        srq_df.to_excel(writer, sheet_name='SRQs',index=False)
                        case_df.to_excel(writer, sheet_name='Cases',index=False)

                    ## handles "Latest Error Data"
                    srq_error_df = srq_df.copy()
                    if 'ReviseErrorCode' in srq_error_df.columns:
                        filtered_df = srq_error_df[srq_error_df['ReviseErrorCode'].notnull()]
                        srq_error_df_to_export_from_filtered = filtered_df.loc[(filtered_df['ReviseErrorCode'] != filtered_df['PredictErrorCode'] )]
                        remained_df = srq_error_df[srq_error_df['ReviseErrorCode'].isnull()]
                        srq_error_df_to_export_from_remained = remained_df.loc[(remained_df['ErrorCode'] != remained_df['PredictErrorCode'] )]
                        srq_error_df_to_export_from_filtered.append(srq_error_df_to_export_from_remained)
                    else:
                        srq_error_df_to_export_from_filtered = srq_error_df.loc[(srq_error_df['ErrorCode'] != srq_error_df['PredictErrorCode'] )]
                        srq_error_df_to_export_from_filtered['ReviseErrorCode'] = ""

                    with pd.ExcelWriter('Latest Error Data.xlsx') as writer:
                        srq_error_df_to_export_from_filtered.to_excel(writer, sheet_name='SRQs',index=False)

                    ## handling latest keyword
                    keywords_json = serializers.serialize('json', Keywords.objects.all())
                    keywords_json =json.loads(keywords_json)


                    r = s.get(algorithm_ip + ':4546', json={'json1':keywords_json, 'json2':srqs_json, 'json3': cases_json})
                    logging.info(r.status_code)
                    logging.info(r.headers['content-type'])
                    logging.info(r.text)
                    # json_response = json.dumps(r.text)
                    analytics = {}
                    # with open('phase2_output.json') as json_file:
                    data = json.loads(r.text)
                    srqs_json_result= json.loads(data['json2'])
                    # try:
                    if type(srqs_json_result) == list:
                        for i in srqs_json_result:
                            if i['fields']['Class'] not in analytics.keys():
                                analytics[i['fields']['Class']] = 1
                            else:
                                analytics[i['fields']['Class']] += 1

                    analytics_to_display = []
                    for key, value in analytics.items():
                        analytics_to_display.append({"class":key, "amount":value})

                    analytics_to_display_list_cat = []
                    analytics_to_display_list_data = []
                    for key, value in analytics.items():
                        analytics_to_display_list_cat.append(key)
                        analytics_to_display_list_data.append(value)

                    analytics = {}
                    cases_json_result= json.loads(data['json3'])

                    if type(cases_json_result) == list:
                        for i in cases_json_result:
                            if i['fields']['Class'] not in analytics.keys():
                                analytics[i['fields']['Class']] = 1
                            else:
                                analytics[i['fields']['Class']] += 1

                    analytics_to_display_cases = []
                    for key, value in analytics.items():
                        analytics_to_display_cases.append({"class":key, "amount":value})
                    analytics_to_display_list_cat_cases = []
                    analytics_to_display_list_data_cases = []
                    for key, value in analytics.items():
                        analytics_to_display_list_cat_cases.append(key)
                        analytics_to_display_list_data_cases.append(value)

                    # prepares the excel file

                    workbook = xlsxwriter.Workbook("Latest Keyword Summary Data.xlsx")
                    worksheet1 = workbook.add_worksheet('SRQs')
                    # Sheet header, first row
                    row_num = 0

                    cell_format = workbook.add_format()
                    cell_format.set_bold()

                    columns = ['SRNumber', 'SRType', 'CreatedDate', 'Model', 'SerialNumber', 'InternalNotes', 'Class']

                    for col_num in range(len(columns)):
                        worksheet1.write(row_num, col_num, columns[col_num], cell_format)

                    # Sheet body, remaining rows

                    for i in srqs_json_result:
                        list_to_write = [i['fields']['SRNumber'], i['fields']['SRType'], i['fields']['CreatedDate'], i['fields']['Model'], i['fields']['SerialNumber'], i['fields']['InternalNotes'], i['fields']['Class']]
                    # rows = srqs_json_result.values_list('SRNumber', 'SRType', 'CreatedDate', 'Model','SerialNumber', 'InternalNotes', 'Class')
                    # for row in rows:
                        row_num += 1
                        for col_num in range(len(list_to_write)):
                            worksheet1.write(row_num, col_num, list_to_write[col_num])

                    worksheet2 = workbook.add_worksheet('Cases')
                    # Sheet header, first row
                    row_num = 0

                    cell_format = workbook.add_format()
                    cell_format.set_bold()

                    columns = ['CaseNumber', 'CreatedDate', 'Model', 'SerialNumber', 'Symptom', 'Diagnosis', 'Description',	'Class']

                    for col_num in range(len(columns)):
                        worksheet2.write(row_num, col_num, columns[col_num], cell_format)

                    # Sheet body, remaining rows

                    for i in cases_json_result:
                        list_to_write = [i['fields']['CaseNumber'], i['fields']['CreatedDate'], i['fields']['Model'], i['fields']['SerialNumber'], i['fields']['Symptom'], i['fields']['Diagnosis'], i['fields']['Description'], i['fields']['Class']]
                    # rows = srqs_json_result.values_list('SRNumber', 'SRType', 'CreatedDate', 'Model','SerialNumber', 'InternalNotes', 'Class')
                    # for row in rows:
                        row_num += 1
                        for col_num in range(len(list_to_write)):
                            worksheet2.write(row_num, col_num, list_to_write[col_num])

                    worksheet3 = workbook.add_worksheet('Static')

                    row_num = 0

                    cell_format = workbook.add_format()
                    cell_format.set_bold()

                    columns = ['Class', 'Corresponding SRQ Number ', 'Corresponding Case Number']

                    for col_num in range(len(columns)):
                        worksheet3.write(row_num, col_num, columns[col_num], cell_format)

                    # Sheet body, remaining rows
                ## TODO
                    # Sheet body, remaining rows
                    analytics_to_write_to_excel_cases = {}

                    if type(cases_json_result) == list:
                        for i in cases_json_result:
                            if i['fields']['Class'] not in analytics_to_write_to_excel_cases.keys():
                                analytics_to_write_to_excel_cases[i['fields']['Class']] = [i['fields']['CaseNumber']]
                            else:
                                analytics_to_write_to_excel_cases[i['fields']['Class']].append(i['fields']['CaseNumber'])

                    analytics_to_write_to_excel_srqs = {}
                    for i in analytics_to_write_to_excel_cases.keys():
                        analytics_to_write_to_excel_srqs[i]=[]

                    if type(srqs_json_result) == list:
                        for i in srqs_json_result:
                            if i['fields']['Class'] not in analytics_to_write_to_excel_srqs.keys():
                                analytics_to_write_to_excel_srqs[i['fields']['Class']] = [i['fields']['SRNumber']]
                            else:
                                analytics_to_write_to_excel_srqs[i['fields']['Class']].append(i['fields']['SRNumber'])


                    for key, value in analytics_to_write_to_excel_srqs.items():

                        row_num += 1
                        worksheet3.write(row_num, 0, str(key))
                        worksheet3.write(row_num, 1, str(value).replace('[','').replace(']','').replace('\'',''))

                    row_num = 0
                    for key, value in analytics_to_write_to_excel_cases.items():
                        row_num += 1
                        if analytics_to_write_to_excel_srqs.keys() == analytics_to_write_to_excel_cases.keys():
                            worksheet3.write(row_num, 2, str(value).replace('[','').replace(']','').replace('\'',''))


                    worksheet4 = workbook.add_worksheet('Rule')

                    row_num = 0

                    cell_format = workbook.add_format()
                    cell_format.set_bold()

                    columns = ['Class', 'Rule', 'Action']

                    for col_num in range(len(columns)):
                        worksheet4.write(row_num, col_num, columns[col_num], cell_format)


                    rows = Keywords.objects.all().values_list('Class', 'Rule', 'Action')
                    for row in rows:
                        row_num += 1
                        for col_num in range(len(row)):
                            worksheet4.write(row_num, col_num, row[col_num])


                    workbook.close()

                    # Handles line chart
                    srqs_json_result= json.loads(data['json2'])
                    cases_json_result= json.loads(data['json3'])
                    lat,lng = [],[]
                    for i in srqs_json_result:
                        lng.append(i['fields']['CreatedDate'])
                        lat.append(i['fields']['Class'])
                    df = pd.DataFrame([lat, lng]).T
                    df['CreatedDate'] = pd.to_datetime(df[1], format='%Y-%m-%d %H:%M:%S')
                    df['Class'] = (df[0])
                    df['week'] = df['CreatedDate'].dt.strftime('%Y-%V')
                    weekly_df = df.groupby(['Class', 'week']).size().rename('counts').reset_index()
                    dict_to_draw_line_charts = weekly_df.to_dict('split')
                    legend = list(weekly_df.Class.unique())
                    labels = []
                    for i in dict_to_draw_line_charts['data']:
                        if i[1] not in labels:
                            labels.append(i[1])
                    labels.sort()
                    data_to_draw = []
                    for i in legend:
                        data_to_draw.append({'label': i, 'data':[] , 'fill': 'false', 'borderColor': ''})
                    color = ['red', 'rgb(11,255,12)', 'rgb(255,11,255)', 'rgb(11,11,255)', 'rgb(255,128,0)', 'rgb(22,100,112)']
                    for i in range(len(data_to_draw)):
                        data_to_draw[i]['borderColor'] = color[i]
                    ## make sure all the keywords have statistics
                    for i in data_to_draw:
                        for j in range(len(labels)):
                            i['data'].append(0)

                    for i in dict_to_draw_line_charts['data']:
                        for j in data_to_draw:
                            if i[0] == j['label']:
                                j['data'][labels.index(i[1])] = i[2]


                    lat,lng = [],[]
                    for i in cases_json_result:
                        lng.append(i['fields']['CreatedDate'])
                        lat.append(i['fields']['Class'])
                    df = pd.DataFrame([lat, lng]).T
                    df['CreatedDate'] = pd.to_datetime(df[1], format='%Y-%m-%d %H:%M:%S')
                    df['Class'] = (df[0])
                    df['week'] = df['CreatedDate'].dt.strftime('%Y-%V')
                    weekly_df = df.groupby(['Class', 'week']).size().rename('counts').reset_index()
                    dict_to_draw_line_charts = weekly_df.to_dict('split')
                    class_amount = weekly_df['Class'].nunique()
                    legend = list(weekly_df.Class.unique())
                    labels_cases = []
                    for i in dict_to_draw_line_charts['data']:
                        if i[1] not in labels_cases:
                            labels_cases.append(i[1])
                    labels_cases.sort()
                    # step = len(labels_cases)
                    data_to_draw_cases = []
                    for i in legend:
                        data_to_draw_cases.append({'label': i, 'data':[] , 'fill': 'false', 'borderColor': ''})
                    color = ['red', 'rgb(11,255,12)', 'rgb(255,11,255)', 'rgb(11,11,255)', 'rgb(255,128,0)', 'rgb(22,100,112)']
                    for i in range(len(data_to_draw_cases)):
                        data_to_draw_cases[i]['borderColor'] = color[i]
                    ## make sure all the keywords have statistics
                    for i in data_to_draw_cases:
                        for j in range(len(labels_cases)):
                            i['data'].append(0)

                    for i in dict_to_draw_line_charts['data']:
                        for j in data_to_draw_cases:
                            if i[0] == j['label']:
                                j['data'][labels_cases.index(i[1])] = i[2]

                    request.session['analytics_to_display_list_cat'] = analytics_to_display_list_cat
                    request.session['analytics_to_display_list_data_cases'] = analytics_to_display_list_data_cases
                    request.session['analytics_to_display_list_cat_cases'] = analytics_to_display_list_cat_cases
                    request.session['analytics_to_display_cases'] = analytics_to_display_cases
                    request.session['labels_cases'] = labels_cases
                    request.session['data_to_draw_cases'] = data_to_draw_cases
                    request.session['analytics_to_display_list_data'] = analytics_to_display_list_data
                    request.session['analytics_to_display'] = analytics_to_display
                    request.session['labels'] = labels
                    request.session['data_to_draw'] = data_to_draw

                    ## printing the hostname and ip_address
                    connections.close_all()
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='upload new data to the database')

                    context = {
                        'upload_success_msg': "You have successfully updated the data",
                        'd': case_statistic_to_draw,
                        'c': srq_statistic_to_draw,
                        'result':result,
                        }
                    return render(request,'latest_errorcode.html', context)


                else:

                    error_title = 'Some column is missing.'

                    context = {
                        'error_msg': 'The sheet named \"Cases\" should contains columns named \'CaseNumber\', \'Model\', \'CreatedDate\', \'SerialNumber\', \'Symptom\', \'Description\', \'Diagnosis\'. Sheet named\'SRQs\' should contains \'SRNumber\', \'Model\', \'CreatedDate\', \'SerialNumber\', \'SRType\', \'ErrorCode\', \'InternalNotes\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)

            elif "Latest Error Data" in str(excel_file).split('.')[0]:
                xl = pd.ExcelFile(excel_file)
                if not all(x in xl.sheet_names for x in ['SRQs',]):
                    error_title = 'Sheet name is incorrect.'

                    context = {
                        'error_msg': 'For Update Revise Data, please check if your file contains sheets named \'SRQs\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)
                srq = xl.parse("SRQs")
                if (all(y in list(srq.columns) for y in ['SRNumber', 'SRType', 'CreatedDate', 'Model', 'SerialNumber','ErrorCode', 'InternalNotes', 'ReviseErrorCode', 'PredictErrorCode'])):
                    srq.dropna(subset=['ReviseErrorCode',], inplace=True)
                    srq = srq [['SRNumber', 'SRType', 'CreatedDate', 'Model', 'SerialNumber','ErrorCode', 'InternalNotes', 'ReviseErrorCode', 'PredictErrorCode']]
                    srqs_dict = srq.to_dict(orient='records')
                    srqs_json = pd.DataFrame({'model': 'text.srqs', 'fields': srqs_dict}).to_dict('records')
                    ## send request to algorithm phase 1
                    srqs_json = json.dumps(srqs_json,cls=DjangoJSONEncoder)
                    srqs_json = json.loads(srqs_json)
                    # r = requests.get('http://10.55.14.167:4547', json={"srqs":srqs_json, 'mode':'Pred'})
                    r = s.get(algorithm_ip + ':4547', json={"srqs":srqs_json, 'mode':'Pred'})
                    time.sleep(60)
                    t = s.get(algorithm_ip + ':4547/restart', json={'mode':'Restart'}, timeout=None)
                    time.sleep(60)
                    srqs_json_raw= json.loads(r.text)
                    srqs_json_result= json.loads(srqs_json_raw['predict_result'])
                    result = {}
                    result['accuracy'] = srqs_json_raw['accuracy']
                    result['date'] = datetime.date.today().strftime("%Y-%m-%d")

                    connections.close_all()
                    for idx, i in enumerate(srqs_json_result):
                        if i['model'] == 'text.srqs':
                            if TMPSRQ.objects.filter(SRNumber=str(i['fields']['SRNumber'])):
                                TMPSRQ.objects.filter(SRNumber=str(i['fields']['SRNumber'])).update(
                                    PredictErrorCode=str(i['fields']['PredictErrorCode']),
                                    ReviseErrorCode=str(i['fields']['ReviseErrorCode']),
                                    Train=bool(strtobool(i['fields']['Train']))
                                    )
                            elif SRQs.objects.filter(SRNumber=str(i['fields']['SRNumber'])):
                                SRQs.objects.filter(SRNumber=str(i['fields']['SRNumber'])).update(
                                    PredictErrorCode=str(i['fields']['PredictErrorCode']),
                                    ReviseErrorCode=str(i['fields']['ReviseErrorCode']),
                                    Train=bool(strtobool(i['fields']['Train'])))

                    ## printing the hostname and ip_address
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='upload revise data')
                    context = {
                    'upload_success_msg': "You have successfully updated the data",

                    }
                    return render(request,'latest_errorcode.html', context)

                else:

                    error_title = 'Some column is missing.'

                    context = {
                        'error_msg': 'For Update Revise Data, the sheet named \"SRQs\" should contains columns named \'SRNumber\', \'ReviseErrorCode\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)


            elif "combo parts list" in (str(excel_file).split('.')[0] ):
                ## Foolproof
                xl = pd.ExcelFile(excel_file)
                if 'Sheet1' not in xl.sheet_names:
                    error_title = 'Sheet name is incorrect.'

                    context = {
                        'error_msg': 'For combo parts list, please check if your file contains a sheet named \'Sheet1\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)
                combo_parts_list = xl.parse("Sheet1")

                if all(x in list(combo_parts_list.columns) for x in ['Vizio_Model','INX_Model','Parts','Combo_Function']):
                    connections.close_all()
                    ComboPartsList.objects.all().delete()
                    combo_parts_list.dropna(subset=['Vizio_Model','INX_Model','Parts','Combo_Function'], inplace=True)
                    combo_parts_list.drop_duplicates(keep='last', inplace = True)
                    combo_parts_list.reset_index(drop=True, inplace=True)
                    objs = []
                    for i in range(len(combo_parts_list['Vizio_Model'])):
                        objs.append(ComboPartsList(
                                    Vizio_Model= str(combo_parts_list['Vizio_Model'][i]),
                                    INX_Model= str(combo_parts_list['INX_Model'][i]),
                                    Parts= str(combo_parts_list['Parts'][i]),
                                    Combo_Function= str(combo_parts_list['Combo_Function'][i]),
                        ))
                    connections.close_all()
                    newlyCreatedDefect = ComboPartsList.objects.bulk_create(objs)

                    ## printing the hostname and ip_address
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='combo_parts_list update')


                    context = {
                        'upload_success_msg': "You have successfully updated the combo_parts_list table",
                        'form': form,
                        }
                    return render(request,'osr_maintain.html', context)

            elif "OSR_special_usage_rule" in (str(excel_file).split('.')[0] ):
                ## Foolproof
                xl = pd.ExcelFile(excel_file)
                if 'SRQs' not in xl.sheet_names:
                    error_title = 'Sheet name is incorrect.'

                    context = {
                        'error_msg': 'For OSR_special_usage_rule, please check if your file contains a sheet named \'SRQs\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)

                OSR_special_usage_rule = xl.parse("SRQs")

                if all(x in list(OSR_special_usage_rule.columns) for x in ['SRType','Created_Date',	'Closed_Date','Model','ErrorCode','Parts_delete','Parts_added',	'Remark']):
                    connections.close_all()
                    SpecialUsageRule.objects.all().delete()
                    OSR_special_usage_rule.dropna(subset=['SRType','Created_Date','Model','ErrorCode'], inplace=True)
                    OSR_special_usage_rule.drop_duplicates(keep='last', inplace = True)
                    OSR_special_usage_rule.reset_index(drop=True, inplace=True)
                    objs = []
                    for i in range(len(OSR_special_usage_rule['SRType'])):
                        if pd.isna(OSR_special_usage_rule.iloc[i]['Closed_Date']):
                            if pd.isna(OSR_special_usage_rule.iloc[i]['Parts_added']):
                                objs.append(SpecialUsageRule(
                                            SRType= str(OSR_special_usage_rule['SRType'][i]),
                                            Created_Date= OSR_special_usage_rule.iloc[i]['Created_Date'].strftime("%Y-%m-%d"),
                                            Model= str(OSR_special_usage_rule['Model'][i]),
                                            ErrorCode= str(OSR_special_usage_rule['ErrorCode'][i]),
                                            Parts_delete= OSR_special_usage_rule['Parts_delete'][i],
                                            Remark= str(OSR_special_usage_rule['Remark'][i]),
                                ))
                            else:
                                objs.append(SpecialUsageRule(
                                            SRType= str(OSR_special_usage_rule['SRType'][i]),
                                            Created_Date= OSR_special_usage_rule.iloc[i]['Created_Date'].strftime("%Y-%m-%d"),
                                            Model= str(OSR_special_usage_rule['Model'][i]),
                                            ErrorCode= str(OSR_special_usage_rule['ErrorCode'][i]),
                                            Parts_delete= OSR_special_usage_rule['Parts_delete'][i],
                                            Parts_added= OSR_special_usage_rule['Parts_added'][i],
                                            Remark= str(OSR_special_usage_rule['Remark'][i]),
                                ))
                        else:
                            if pd.isna(OSR_special_usage_rule.iloc[i]['Parts added']):
                                objs.append(SpecialUsageRule(
                                        SRType= str(OSR_special_usage_rule['SRType'][i]),
                                        Created_Date= OSR_special_usage_rule.iloc[i]['CreatedDate'].strftime("%Y-%m-%d"),
                                        Closed_Date= OSR_special_usage_rule.iloc[i]['Closed Date'].strftime("%Y-%m-%d"),
                                        Model= str(OSR_special_usage_rule['Model'][i]),
                                        ErrorCode= str(OSR_special_usage_rule['ErrorCode'][i]),
                                        Parts_delete= OSR_special_usage_rule['Parts delete'][i],
                                        Remark= str(OSR_special_usage_rule['Remark'][i]),
                            ))
                            else:
                                objs.append(SpecialUsageRule(
                                        SRType= str(OSR_special_usage_rule['SRType'][i]),
                                        Created_Date= OSR_special_usage_rule.iloc[i]['CreatedDate'].strftime("%Y-%m-%d"),
                                        Closed_Date= OSR_special_usage_rule.iloc[i]['Closed Date'].strftime("%Y-%m-%d"),
                                        Model= str(OSR_special_usage_rule['Model'][i]),
                                        ErrorCode= str(OSR_special_usage_rule['ErrorCode'][i]),
                                        Parts_delete= OSR_special_usage_rule['Parts delete'][i],
                                        Parts_added= OSR_special_usage_rule['Parts added'][i],
                                        Remark= str(OSR_special_usage_rule['Remark'][i]),
                            ))
                    connections.close_all()
                    newlyCreatedDefect = SpecialUsageRule.objects.bulk_create(objs)

                    ## printing the hostname and ip_address
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='OSR_special_usage_rule update')


                    context = {
                        'upload_success_msg': "You have successfully updated the OSR_special_usage_rule table",
                        'form': form,
                        }
                    return render(request,'osr_maintain.html', context)


                else:
                    error_title = 'Some columns are missing.'

                    connections.close_all()
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='upload OSR_special_usage_rule table failed.')



                    context = {
                        'error_msg': 'For update OSR_special_usage_rule table, please check if in "SRQs", there are 8 columns named \'SRType\',	\'Created_Date\',	\'Closed_Date\',\'Model\',\'ErrorCode\',\'Parts_delete\',\'Parts_added\',	\'Remark\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)

            elif "parts price" in (str(excel_file).split('.')[0] ):
                ## Foolproof
                xl = pd.ExcelFile(excel_file)
                if 'Sheet1' not in xl.sheet_names:
                    error_title = 'Sheet name is incorrect.'

                    context = {
                        'error_msg': 'For parts price, please check if your file contains a sheet named \'Sheet1\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)

                parts_price = xl.parse("Sheet1")

                if all(x in list(parts_price.columns) for x in ['TV_Model','Part_Description','Part_Price']):
                    connections.close_all()
                    PartsPrice.objects.all().delete()
                    parts_price.dropna(subset=['TV_Model','Part_Description','Part_Price'], inplace=True)
                    parts_price.drop_duplicates(keep='last', inplace = True)
                    parts_price.reset_index(drop=True, inplace=True)
                    objs = []
                    for i in range(len(parts_price['TV_Model'])):
                        objs.append(PartsPrice(
                                        TV_Model= str(parts_price['TV_Model'][i]),
                                        Part_Description= str(parts_price['Part_Description'][i]),
                                        Part_Price= float(parts_price['Part_Price'][i]),
                        ))

                    connections.close_all()
                    newlyCreatedDefect = PartsPrice.objects.bulk_create(objs)

                    ## printing the hostname and ip_address
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='parts price')


                    context = {
                        'upload_success_msg': "You have successfully updated the parts price table",
                        'form': form,
                        }
                    return render(request,'osr_maintain.html', context)


                else:
                    error_title = 'Some columns are missing.'

                    connections.close_all()
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='upload parts price table failed.')



                    context = {
                        'error_msg': 'For update parts price table, please check if in "Sheet1", there are 3 columns named \'TV Model\',\'Part Description\',\'Part Price (USD)\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)

            elif "OSR_part_number" in (str(excel_file).split('.')[0] ):
                ## Foolproof
                xl = pd.ExcelFile(excel_file)
                if 'Sheet1' not in xl.sheet_names:
                    error_title = 'Sheet name is incorrect.'

                    context = {
                        'error_msg': 'For OSR_part_number mapping table, please check if your file contains a sheet named \'Sheet1\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)
                osr_part_number = xl.parse("Sheet1")

                if all(x in list(osr_part_number.columns) for x in ['MODEL','CHILD_PRODUCT_ID','PART_DESCRIPTION','CHILD_DESCRIPTION', 'Tconless']):
                    connections.close_all()
                    OsrPartNumber.objects.all().delete()
                    osr_part_number.dropna(subset=['MODEL','CHILD_PRODUCT_ID','PART_DESCRIPTION','CHILD_DESCRIPTION'], inplace=True)
                    osr_part_number.drop_duplicates(keep='last', inplace = True)
                    osr_part_number.reset_index(drop=True, inplace=True)
                    objs = []
                    for i in range(len(osr_part_number['CHILD_DESCRIPTION'])):
                        objs.append(OsrPartNumber(
                                    MODEL= str(osr_part_number['MODEL'][i]),
                                    CHILD_PRODUCT_ID= str(osr_part_number['CHILD_PRODUCT_ID'][i]),
                                    PART_DESCRIPTION= str(osr_part_number['PART_DESCRIPTION'][i]),
                                    CHILD_DESCRIPTION= str(osr_part_number['CHILD_DESCRIPTION'][i]),
                                    TCONLESS= str(osr_part_number['Tconless'][i]),
                        ))
                    connections.close_all()
                    newlyCreatedDefect = OsrPartNumber.objects.bulk_create(objs)

                    ## printing the hostname and ip_address
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='combo_parts_list update')


                    context = {
                        'upload_success_msg': "You have successfully updated the OSR_part_number mapping table",
                        'form': form,
                        }
                    return render(request,'osr_maintain.html', context)

            elif "ITI OSR parts usage" in (str(excel_file).split('.')[0] ):
                ## Foolproof
                xl = pd.ExcelFile(excel_file)
                if 'Sheet1' not in xl.sheet_names:
                    error_title = 'Sheet name is incorrect.'

                    context = {
                        'error_msg': 'For ITI OSR parts usage, please check if your file contains a sheet named \'Sheet1\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)

                iti_osr_parts_usage = xl.parse("Sheet1")

                if all(x in list(iti_osr_parts_usage.columns) for x in ['Reference_No', 'substatus', 'model', 'serial', 'problemDesc', 'Parts', 'PartReplaced']):
                    iti_osr_parts_usage.dropna(subset=['Reference_No', 'substatus', 'model', 'serial', 'problemDesc', 'Parts', 'PartReplaced'], inplace=True)
                    iti_osr_parts_usage.drop_duplicates(keep='last', inplace = True)
                    iti_osr_parts_usage.reset_index(drop=True, inplace=True)
                    tech_data = iti_osr_parts_usage.astype(str).to_dict(orient="records")
                    val_data = pd.DataFrame(list(OSR.objects.filter(
                        Q(Sent_Parts='nan'), ~Q(Predict_Sent_Parts='nan')
                    ).values('OSRNumber', 'TV_Model', 'Import_Date', 'ErrorCode','Predict_Train_Parts', 'Predict_Sent_Parts', 'Threshold_result'))).astype(str).to_dict(orient="records")
                    combo = pd.DataFrame(list(ComboPartsList.objects.all().values('Vizio_Model', 'INX_Model', 'Parts', 'Combo_Function'))).astype(str).to_dict(orient="records")
                    specAdj = pd.DataFrame(list(SpecialUsageRule.objects.all().values("SRType", "Created_Date", "Closed_Date", "Model", "ErrorCode", "Parts_delete", "Parts_added", "Remark")))
                    mask = specAdj.applymap(lambda x: x == '')
                    cols = specAdj.columns[(mask).any()]
                    for col in specAdj[cols]:
                        specAdj.loc[mask[col], col] = 'nan'
                    specAdj = specAdj.astype(str).to_dict(orient="records")
                    r = s.get(algorithm_ip + ':4548', json={"tech_data":tech_data, "val_data": val_data, "combo": combo, 'specAdj':specAdj, 'mode':'Val'})
                    t = s.get(algorithm_ip + ':4548/restart', json={'mode':'Restart'}, timeout=None)
                    # r = s.get('http://127.0.0.1:8001', json={"tech_data":tech_data, "val_data": val_data, "combo": combo, 'specAdj':specAdj, 'mode':'Val'})
                    df = pd.DataFrame(json.loads(r.text)['result'])
                    if df.empty:
                        context = {
                        'upload_success_msg': "You have successfully updated the ITI OSR parts usage",
                        'form': form,
                        }
                        return render(request,'osr_maintain.html', context)

                    df = df.replace(np.nan, 'nan')
                    connections.close_all()
                    for i in range(len(df['OSRNumber'])):
                        OSR.objects.filter(OSRNumber=str(df['OSRNumber'][i])) \
                            .update(Predict_Sent_Parts=str(df['Predict_Sent_Parts'][i]), \
                            Sent_Parts=str(df['Sent_Parts'][i]), Train_Parts=str(df['Train_Parts'][i]), F2score=str(df['F2score'][i]), \
                            OverSent_Parts=str(df['OverSent_Parts'][i]), UnderSent_Parts=str(df['UnderSent_Parts'][i]))

                    ## printing the hostname and ip_address
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='ITI OSR parts usage uploaded.')
                    context = {
                        'upload_success_msg': "You have successfully updated the ITI OSR parts usage",
                        'form': form,
                        }
                    return render(request,'osr_maintain.html', context)


                else:
                    error_title = 'Some columns are missing.'

                    connections.close_all()
                    Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='upload ITI OSR parts usage failed.')

                    context = {
                        'error_msg': 'For update ITI OSR parts usage, please check if in "Sheet1", there are 7 columns named \'Reference_No\', \'substatus\', \'model\', \'serial\', \'problemDesc\', \'Parts\', \'PartReplaced\'',
                        'error_title': error_title,
                    }

                    return render(request, 'latest_name_error.html', context)

            # In case the file is not following the name convention

            else:
                logging.error('ilegal file name')
                context = {
                    'upload_success_msg': " ",
                    'form': form,
                }

                return render(request,'latest_name_error.html', context)

        # except:
        #     logging.error('It bumps into an error when reading the file')
        #     context = {}
        #     return render(request,'latest_name_error.html', context)


@login_required
def export_xls(request):
    try:
        file = open('Latest ErrorCode Summary Data.xlsx', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream' #設定頭資訊，告訴瀏覽器這是個檔案
        response['Content-Disposition'] = 'attachment;filename="Latest ErrorCode Summary Data.xlsx"'
        return response


    except:
        return HttpResponse('An error occurred during preparing the excel file. Please note the search conditions and notify system administrator. Much thanks.')

@login_required
def export_error(request):
    try:
        file = open('Latest Error Data.xlsx', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream' #設定頭資訊，告訴瀏覽器這是個檔案
        response['Content-Disposition'] = 'attachment;filename="Latest Error Data.xlsx"'
        return response


    except:
        return HttpResponse('An error occurred during preparing the excel file. Please note the search conditions and notify system administrator. Much thanks.')

@login_required
def export_latest_keyword_summary_data(request):
    try:
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        connections.close_all()
        Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='load export_latest_keyword_summary_data')

        file = open('Latest Keyword Summary Data.xlsx', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream' #設定頭資訊，告訴瀏覽器這是個檔案
        response['Content-Disposition'] = 'attachment;filename="Latest_Keyword_Summary Data.xlsx"'
        return response

    except:
        return HttpResponse('An error occurred during preparing the excel file. Please note the search conditions and notify system administrator. Much thanks.')



@login_required
def export_onsite_error_data(request):

    try:
        # handles user data
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        connections.close_all()
        Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='load export_onsite_error_data')

        file = open('Latest_Onsite_Error Data.xlsx', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream' #設定頭資訊，告訴瀏覽器這是個檔案
        response['Content-Disposition'] = 'attachment;filename="Latest_Onsite_Error Data.xlsx"'
        return response
    except:
        return HttpResponse('An error occurred during preparing the excel file. Please note the search conditions and notify system administrator. Much thanks.')

@login_required
def export_onsite_summary_data(request):

    try:
        # handles user data
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        connections.close_all()
        Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='load export_onsite_summary_data')

        file = open('Latest_Onsite_Summary Data.xlsx', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream' #設定頭資訊，告訴瀏覽器這是個檔案
        response['Content-Disposition'] = 'attachment;filename="Latest_Onsite_Summary Data.xlsx"'
        return response
    except:
        return HttpResponse('An error occurred during preparing the excel file. Please note the search conditions and notify system administrator. Much thanks.')

@login_required
# This is for get the Export Summary Data btn on Historical ErrorCode page
def export_historical_error_data(request):

    try:
        # handles user data
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        connections.close_all()
        Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='load export_historical_error_data')


        file = open('Historical ErrorCode Summary Data.xlsx', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream' #設定頭資訊，告訴瀏覽器這是個檔案
        response['Content-Disposition'] = 'attachment;filename="Historical ErrorCode Summary Data.xlsx"'
        return response
    except:
        return HttpResponse('An error occurred during preparing the excel file. Please note the search conditions and notify system administrator. Much thanks.')

@login_required
# This is for get the Export Summary Data btn on Historical ErrorCode page
def export_historical_errorcode_error_data(request):

    try:
        # handles user data
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        connections.close_all()
        Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='load historical_errorcode_error_data')


        file = open('Historical ErrorCode Error Data.xlsx', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream' #設定頭資訊，告訴瀏覽器這是個檔案
        response['Content-Disposition'] = 'attachment;filename="Historical ErrorCode Error Data.xlsx"'
        return response
    except:
        return HttpResponse('An error occurred during preparing the excel file. Please note the search conditions and notify system administrator. Much thanks.')


@login_required
def export_historical_keyword(request):

    try:
        # handles user data
        ## getting the hostname by socket.gethostname() method
        hostname = socket.gethostname()
        ## getting the IP address using socket.gethostbyname() method
        ip_address = socket.gethostbyname(hostname)
        ## printing the hostname and ip_address
        connections.close_all()
        Logfiles.objects.create(hostname=hostname, ip_address=ip_address, action='load export_historical_keyword')

        file = open('Historical Keyword Summary Data.xlsx', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream' #設定頭資訊，告訴瀏覽器這是個檔案
        response['Content-Disposition'] = 'attachment;filename="Historical Keyword Summary Data.xlsx"'
        return response
    except:
        return HttpResponse('An error occurred during preparing the excel file. Please note the search conditions and notify system administrator. Much thanks.')

@login_required
def user_manual(request):
    # try:
        context = {

        }

        return render(request, 'usermanual.html', context)
    # except:
    #     return HttpResponse('An error occurred during loading the user manual. Please notify system administrator. Much thanks.')


@login_required
# @permission_required('text.add_cases')
def cqe_configuration(request):

    try:
        context = {

        }
        return render(request, 'cqe_configuration.html', context)
    except:
        print('oops')

def login_view(request):
    messages = ''
    if request.method == 'POST':
        name = request.POST['userID'].strip()
        password = request.POST['password']
        userInfo = CheckAD(userId=name, password=password)
        if userInfo['ID'] is not None:
            name = json.loads(userInfo['Properties'])
            employee_id = name['employeeid'][0]
            first_name = name['displayname'][0].split('.')[0].title()
            m = re.search('\.(.+?) ', name['displayname'][0])
            if m:
                last_name = m.group(1).title()
            user = User.objects.filter(username=employee_id)
            password = "fC%/`D]8!a9V$!E4"
            email = name['mail'][0]
            request.session['user'] = userInfo
            if not user:
                user = User.objects.create(username=employee_id, password=password, first_name=first_name, last_name=last_name, email=email)
                user.save()
                auth_login(request, user)
                return redirect('/crpd/create_account')

            else:
                user = User.objects.get(username=employee_id)
                auth_login(request, user)
                return redirect('/crpd/user_manual')
        else:
            message = '您輸入的帳號密碼有誤，請重試。'
            context = {
                'message': message,
            }
            return render(request, "login.html", context)
        # request.session['user'] = {'displayname': ['shouping.liang 梁守平'], 'adspath': ['LDAP://CMINLLDAP.LOCAL/CN=shouping.liang,OU=8Q5G0500,OU=8Q500500,OU=TNN,DC=cminl,DC=oa'], 'name': ['shouping.liang'], 'cn': ['shouping.liang'], 'mail': ['shouping.liang@innolux.com'], 'department': ['8Q5G2501'], 'employeeid': ['20001547']}
        # user = authenticate(username=name, password="^'.tb+8n9eQPtx$p")
        # if user is not None:
        #     auth_login(request, user)
        #     return redirect('/home')
    else:
        form = forms.PostForm()
        context = {
            'form': form,
        }


        return render(request, "login.html", context)

def logout_view(request):
    auth_logout(request)
    return redirect('login')


def create_account(request):
    if 'user' not in request.session.keys():
        return redirect('login')

    form = forms.Auth_applicationForm()
    userInfo = json.loads(request.session['user']['Properties'])
    # userInfo = json.loads(request.session['user'])
    employee_id = userInfo['employeeid'][0]
    employee_name = userInfo['displayname'][0].split()[1]

    context = {
        'form': form,
        'userInfo':userInfo,
        'employee_name': employee_name,
        'employee_id':employee_id,
    }

    if request.method == 'POST':
        form = forms.Auth_applicationForm(request.POST)
        if form.is_valid():
            form.save()
            bill_nr = Auth_application.objects.all().order_by('-id')[0].id
            useraccount = 'api_smartpush'
            apikey = '9AE29D27-02F2-016A-11AF-01C9907ABB28'
            chatsn = '132202'
            content = '收到新的RMA權限申請，請登入系統審批http://10.55.52.126:8000/crpd/approval/'+str(bill_nr)
            # mapppost_content(useraccount,apikey,chatsn,content)
        return render(request, 'success.html', context)

    return render(request, 'create_account.html', context)


def approval(request, id):
    application = get_object_or_404(Auth_application, id=id)
    if application.current_status == '2' or application.current_status == '3':
        title = '該案件已經審核完畢，無法重新審核。倘有需要，可請提案人再次申請。'
        context = {
            'title': title,
        }
        return render(request, 'success.html', context)
    if request.method == 'GET':
        form = forms.Auth_approvalForm()

        context = {
            'application': application,
            'form': form,
        }
        return render(request, 'approval.html', context)

    else:
        form = forms.Auth_approvalForm(request.POST)
        if form.is_valid():
            form.save()
            approval = request.POST.get('approval')
            if approval == '0':
                Auth_application.objects.filter(id=id).update(current_status=2)
                employee_id = application.employee_id
                permission = Permission.objects.get(pk=29)
                User.objects.get(username=employee_id).user_permissions.add(permission)
                title = '審核成功，該使用者已可新增知識法則'
                context = {
                    'title': title,
                }
                return render(request, 'success.html', context)

            elif approval == '1':
                Auth_application.objects.filter(id=id).update(current_status=3)
                title = '該筆申請已經拒絕，謝謝您在百忙之中進行審批。'
                context = {
                        'title': title,
                    }
                return render(request, 'success.html', context)

        else:
            return HttpResponse(form.errors)

def osr_dashboard(request):
    """
    Display required inf on the dashboard and prepares the excel file for upload.
    """
    queryset = OSR.objects.all()

    if 'start_date' not in request.GET.keys():
        last_month_last_day = datetime.datetime.utcnow().replace(day=1) - datetime.timedelta(days=1)
        last_month_first_day = last_month_last_day.replace(day=1)
        osr_date_filter = OSRDateFilter(request.GET, queryset=queryset)
        last_month_osr = queryset.filter(
            Q(Import_Date__gte=last_month_first_day) ,Q(Import_Date__lte=last_month_last_day)
        )
        last_month_osr_amount = last_month_osr.count()
        if last_month_osr_amount == 0:
            context = {
            'filter': osr_date_filter,
            'card_title': 'There is no enough data to show last month\'s performance.'
            }

            return render(request, 'osr_dashboard.html', context)

        ## Display last month's data
        last_month_only_oversent = last_month_osr.filter(
            ~Q(OverSent_Parts='nan'), Q(UnderSent_Parts='nan'), ~Q(Predict_Sent_Parts='nan')
        ).count()
        last_month_only_undersent = last_month_osr.filter(
            Q(OverSent_Parts='nan'), ~Q(UnderSent_Parts='nan'), ~Q(Predict_Sent_Parts='nan')
        ).count()
        last_month_both_undersent_oversent = last_month_osr.filter(
            ~Q(OverSent_Parts='nan'), ~Q(UnderSent_Parts='nan'), ~Q(Predict_Sent_Parts='nan')
        ).count()

        last_month_not_analyzable = last_month_osr.filter(Predict_Sent_Parts='nan').count()
        last_month_both_correct = last_month_osr.filter(F2score='1.0').count()
        last_month_others = last_month_osr_amount - last_month_only_oversent - last_month_only_undersent - last_month_both_undersent_oversent\
            -last_month_not_analyzable - last_month_both_correct

        ## Only for 24 Jun 2021 Demo purpose
        last_month_osr_amount -= last_month_others
        last_month_others = 0
        ## End of demo purpose

        request.session['last_month_osr_amount'] = last_month_osr_amount
        request.session['last_month_only_oversent'] = last_month_only_oversent
        request.session['last_month_only_undersent'] = last_month_only_undersent
        request.session['last_month_both_correct'] = last_month_both_correct
        request.session['last_month_both_undersent_oversent'] = last_month_both_undersent_oversent
        request.session['last_month_others'] = last_month_others
        last_month_only_undersent_and_last_month_both_undersent_oversent = last_month_only_undersent + last_month_both_undersent_oversent
        context = {
            'filter': osr_date_filter,
            'last_month_only_oversent': last_month_only_oversent,
            'last_month_osr_amount':last_month_osr_amount,
            'last_month_only_undersent':last_month_only_undersent_and_last_month_both_undersent_oversent,
            'last_month_not_analyzable': last_month_not_analyzable,
            'last_month_both_correct':last_month_both_correct,
            'card_title': 'Last Month\'s Performance',
            'last_month_others':last_month_others,
            }

        return render(request, 'osr_dashboard.html', context)

    ## For query
    else:
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        osr_date_filter = OSRDateFilter(request.GET, queryset=queryset)
        last_month_osr = osr_date_filter.qs
        last_month_osr_amount = last_month_osr.count()
        last_month_only_oversent = last_month_osr.filter(
            ~Q(OverSent_Parts='nan'), Q(UnderSent_Parts='nan'), ~Q(Predict_Sent_Parts='nan')
        ).count()
        last_month_only_undersent = last_month_osr.filter(
            Q(OverSent_Parts='nan'), ~Q(UnderSent_Parts='nan'), ~Q(Predict_Sent_Parts='nan')
        ).count()
        last_month_both_undersent_oversent = last_month_osr.filter(
            ~Q(OverSent_Parts='nan'), ~Q(UnderSent_Parts='nan'), ~Q(Predict_Sent_Parts='nan')
        ).count()
        last_month_not_analyzable = last_month_osr.filter(Predict_Sent_Parts='nan').count()
        last_month_both_correct = last_month_osr.filter(F2score='1.0').count()
        last_month_others = last_month_osr_amount - last_month_only_oversent - last_month_only_undersent - last_month_both_undersent_oversent\
            -last_month_not_analyzable - last_month_both_correct
        last_month_only_undersent_and_last_month_both_undersent_oversent = last_month_only_undersent + last_month_both_undersent_oversent

        ## Only for 24 Jun 2021 Demo purpose
        last_month_osr_amount -= last_month_others
        last_month_others = 0
        ## End of demo purpose

        request.session['last_month_osr_amount'] = last_month_osr_amount
        request.session['last_month_only_oversent'] = last_month_only_oversent
        request.session['last_month_only_undersent'] = last_month_only_undersent
        request.session['last_month_both_correct'] = last_month_both_correct
        request.session['last_month_both_undersent_oversent'] = last_month_both_undersent_oversent
        request.session['last_month_others'] = last_month_others
        context = {
            'filter': osr_date_filter,
            'last_month_only_oversent': last_month_only_oversent,
            'last_month_osr_amount':last_month_osr_amount,
            'last_month_both_undersent_oversent':last_month_both_undersent_oversent,
            'last_month_only_undersent':last_month_only_undersent_and_last_month_both_undersent_oversent,
            'last_month_not_analyzable': last_month_not_analyzable,
            'last_month_both_correct':last_month_both_correct,
            'last_month_others':last_month_others,
            }

        return render(request, 'osr_dashboard.html', context)



def osr_search(request):
    """
    Display required inf on the dashboard and prepares the excel file for upload.
    """
    osr_list = OSR.objects.all()
    osr_filter = _OSRFilter(request.GET, queryset=osr_list)
    # df = pd.DataFrame({"PredictPart1" : {"OSS3327128" : ["WIFI", "Power"],
    # "OSS3325037" : ["Power"], "OSS3322106" : ["MotherBoard", "Mouse"]},
    # "IssuedDate" : dict(zip(["OSS3327128","OSS3325037","OSS3322106"],
    # ['2020-12-01','2020-12-02','2020-12-03']))})
    # df['PredictPart1'].apply(lambda x: pd.Series(x)).stack().reset_index(level=1, drop=True).to_frame('PredictPart1').join(df[['IssuedDate']], how='left')

    if request.GET.get('osr_no', '') == '':
        context = {
                'filter': osr_filter,
                }


        return render(request, 'osr_search.html', context)

    query_osr = list(request.GET['osr_no'].split(" "))
    request.session['query_osr'] = query_osr
    query_result = OSR.objects.filter(OSRNumber__in=query_osr)
    for i in query_result:
        i.Sent_Parts = list(i.Sent_Parts.split(","))
        i.Predict_Sent_Parts = list(i.Predict_Sent_Parts.split(","))
    context = {
        'filter': osr_filter,
        'query_result': query_result,
        }


    return render(request, 'osr_search.html', context)

def osr_material_graph(request):
    """
    docstring
    """
    form = forms.OSRSearchForm()

    context = {
        'form':form,
        }


    return render(request, 'osr_material_graph.html', context)

def osr_value_graph(request):
    """
    docstring
    """
    if 'start_date' not in request.GET.keys():
        osr_list = OSR.objects.all()
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
        all_models_list = list()
        for i in all_models_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_models_list:
                                        all_models_list.append(k)
        context = {
            'filter': osr_filter,
            'all_models_list':all_models_list,
            }


        return render(request, 'osr_value_graph.html', context)

    request.session['start_date'] = request.GET['start_date']
    request.session['end_date'] = request.GET['end_date']
    request.session['machine_model'] = request.GET.getlist('machine_model')
    machine_model = request.GET.getlist('machine_model')
    osr_list = OSR.objects.filter(
        ~Q(Predict_Sent_Parts__isnull=True), ~Q(Sent_Parts__isnull=True), ~Q(Predict_Sent_Parts='nan'), ~Q(Sent_Parts='nan')
        )
    osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
    query_result = osr_filter.qs.filter(TV_Model__in=machine_model)
    all_parts_predict_queryset = query_result.values_list('Predict_Sent_Parts')
    all_parts_predict_dict = dict()
    for i in all_parts_predict_queryset:
        if (i[0] is not None) and (i[0] != 'nan'):
            for j in i:
                    for k in j.split(','):
                            if k not in all_parts_predict_dict.keys():
                                    all_parts_predict_dict[k] = 1
                            else:
                                all_parts_predict_dict[k] += 1
    all_parts_sent_queryset = query_result.values_list('Sent_Parts')
    all_parts_sent_dict = dict()
    for i in all_parts_sent_queryset:
        if (i[0] is not None) and (i[0] != 'nan'):
            for j in i:
                    for k in j.split(','):
                            if k not in all_parts_sent_dict.keys():
                                    all_parts_sent_dict[k] = 1
                            else:
                                all_parts_sent_dict[k] += 1
    price = PartsPrice.objects.filter(TV_Model__in=machine_model).values_list('Part_Description','Part_Price')
    price_dict = dict()
    for i in price:
        price_dict[i[0]] = float(i[1])

    for i in all_parts_predict_dict.keys():
        if i in price_dict.keys():
                all_parts_predict_dict[i] *= price_dict[i]
        else:
                all_parts_predict_dict[i] *= 0

    for i in all_parts_sent_dict.keys():
        if i in price_dict.keys():
                all_parts_sent_dict[i] *= price_dict[i] * -1
        else:
                all_parts_sent_dict[i] *= 0

    graph_data = list()
    for i in all_parts_predict_dict.keys():
        if i in all_parts_sent_dict.keys():
            graph_data.append({"age": i, "female": all_parts_predict_dict[i], "male": all_parts_sent_dict[i]})

    predict_total = 0
    for i in all_parts_predict_dict.values():
        predict_total += i
    sent_total = 0
    for i in all_parts_sent_dict.values():
        sent_total += i

    context = {
            'filter': osr_filter,
            'graph_data': graph_data,
            'predict_total': predict_total,
            'sent_total': sent_total,
            'machine_model':machine_model,
    }


    return render(request, 'osr_value_graph.html', context)



def osr_distribution(request):
    """
    docstring
    """
    if 'start_date' not in request.GET.keys():
        osr_list = OSR.objects.exclude(Sent_Parts__isnull=True)
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
        all_models_list = list()
        for i in all_models_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_models_list:
                                        all_models_list.append(k)

        all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
        all_parts_list = list()
        for i in all_parts_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_parts_list:
                                        all_parts_list.append(k)
        context = {
            'filter': osr_filter,
            'all_models_list':all_models_list,
            'all_parts_list':all_parts_list,
            }


        return render(request, 'osr_distribution.html', context)


    if len(request.GET.getlist('part_name')) == 1 and len(request.GET.getlist('machine_model')) == 1:
        osr_list = OSR.objects.exclude(Sent_Parts__isnull=True)
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
        all_models_list = list()
        for i in all_models_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_models_list:
                                        all_models_list.append(k)

        all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
        all_parts_list = list()
        for i in all_parts_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_parts_list:
                                        all_parts_list.append(k)
        context = {
            'filter': osr_filter,
            'all_models_list':all_models_list,
            'all_parts_list':all_parts_list,
            'error_msg': 'The search is ilegal. Scenarios are:',
            }


        return render(request, 'osr_distribution.html', context)


    if len(request.GET.getlist('part_name')) > 1 and len(request.GET.getlist('machine_model')) > 1 or len(request.GET.getlist('part_name')) == 1 and len(request.GET.getlist('machine_model')) > 1 or len(request.GET.getlist('part_name')) > 1 and len(request.GET.getlist('machine_model')) == 1 :

        osr_list = OSR.objects.exclude(Sent_Parts='nan').exclude(Predict_Sent_Parts='nan')
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        machine_model = request.GET.getlist('machine_model')
        part_name = request.GET.getlist('part_name')
        request.session['part_name'] = part_name
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        request.session['machine_model'] = machine_model
        statistic = {}
        for i in machine_model:
            statistic[i] = 0
        for i in osr_filter.qs:
            if i.TV_Model in machine_model:
                for j in i.Sent_Parts.split(','):
                    if j in part_name:
                        statistic[i.TV_Model] += 1
        graph_data = []
        part_name_display = ' ,'.join([str(elem) for elem in part_name])
        for i in statistic.keys():
            graph_data.append({"country": str(i) + ',' + str(part_name_display), "litres": statistic[i]})

        statistic_predict = {}
        for i in machine_model:
            statistic_predict[i] = 0
        for i in osr_filter.qs:
            if i.TV_Model in machine_model:
                for j in i.Predict_Sent_Parts.split(','):
                    if j in part_name:
                        statistic_predict[i.TV_Model] += 1
        graph_data_predict = []
        for i in statistic_predict.keys():
            graph_data_predict.append({"country": str(i) + ',' + str(part_name_display), "litres": statistic_predict[i]})
        context = {
            'osr_filter':osr_filter,
            'graph_data': graph_data,
            'search_type':'both',
            'machine_model': machine_model,
            'part_name':part_name,
            'graph_data_predict': graph_data_predict
            }
        return render(request, 'osr_distribution.html', context)

    if 'part_name' in request.GET.keys():

        osr_list = OSR.objects.exclude(Sent_Parts='nan').exclude(Predict_Sent_Parts='nan')
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        part_name = request.GET.getlist('part_name')
        request.session['part_name'] = part_name
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        if 'machine_model' in request.session.keys():
            del request.session['machine_model']
        machine_model = list()
        all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
        for i in all_models_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in machine_model:
                                        machine_model.append(k)
        statistic = {}
        for i in machine_model:
            statistic[i] = 0
        for i in osr_filter.qs:
            if i.TV_Model in machine_model:
                for j in i.Sent_Parts.split(','):
                    if j in part_name:
                        statistic[i.TV_Model] += 1
        graph_data = []
        part_name_display = ' ,'.join([str(elem) for elem in part_name])
        for i in statistic.keys():
            graph_data.append({"country": str(i) + ',' + str(part_name_display), "litres": statistic[i]})

        statistic_predict = {}
        for i in machine_model:
            statistic_predict[i] = 0
        for i in osr_filter.qs:
            if i.TV_Model in machine_model:
                for j in i.Predict_Sent_Parts.split(','):
                    if j in part_name:
                        statistic_predict[i.TV_Model] += 1
        graph_data_predict = []
        for i in statistic_predict.keys():
            graph_data_predict.append({"country": str(i) + ',' + str(part_name_display), "litres": statistic_predict[i]})

        context = {
            'osr_filter':osr_filter,
            'graph_data': graph_data,
            'search_type':'part_only',
            'machine_model': machine_model,
            'part_name':part_name,
            'graph_data_predict': graph_data_predict
            }
        return render(request, 'osr_distribution.html', context)

    ## scenario 1: one machine_model, all parts
    if 'machine_model' in request.GET.keys():

        osr_list = OSR.objects.exclude(Sent_Parts='nan').exclude(Predict_Sent_Parts='nan')
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        machine_model = request.GET.getlist('machine_model')
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        request.session['machine_model'] = machine_model

        if 'part_name' in request.session.keys():
            del request.session['part_name']

        all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
        all_parts_list = list()
        for i in all_parts_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_parts_list:
                                        all_parts_list.append(k)
        statistic = {}
        for i in all_parts_list:
            statistic[i] = 0
        for i in osr_filter.qs:
            if i.TV_Model in machine_model:
                for j in i.Sent_Parts.split(','):
                    if j in all_parts_list:
                        statistic[j] += 1
        graph_data = []
        part_name_display = ' ,'.join([str(elem) for elem in all_parts_list])
        for i in statistic.keys():
            graph_data.append({"country": str(machine_model[0]) + ',' + str(i), "litres": statistic[i]})

        statistic_predict = {}
        for i in all_parts_list:
            statistic_predict[i] = 0
        for i in osr_filter.qs:
            if i.TV_Model in machine_model:
                for j in i.Predict_Sent_Parts.split(','):
                    if j in all_parts_list:
                        statistic_predict[j] += 1
        graph_data_predict = []
        for i in statistic_predict.keys():
            graph_data_predict.append({"country": str(machine_model[0]) + ',' + str(i), "litres": statistic_predict[i]})

        context = {
            'osr_filter':osr_filter,
            'graph_data': graph_data,
            'search_type':'machine_model_only',
            'machine_model': machine_model,
            'part_name':part_name_display,
            'graph_data_predict': graph_data_predict
            }
        return render(request, 'osr_distribution.html', context)


def osr_unusual(request):
    """
    docstring
    """
    if 'start_date' not in request.GET.keys():
        osr_list = OSR.objects.filter(
            ~Q(Sent_Parts='nan'), ~Q(Sent_Parts__isnull=True)
            )
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)

        all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
        all_parts_list = list()
        for i in all_parts_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_parts_list:
                                        all_parts_list.append(k)

        all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
        all_models_list = list()
        for i in all_models_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_models_list:
                                        all_models_list.append(k)
        context = {
            'filter':osr_filter,
            'all_parts_list': all_parts_list,
            'all_models_list': all_models_list,
            }


        return render(request, 'osr_unusual.html', context)


    ## scenario 1: both selected
    if len(request.GET.getlist('part_name')) > 1 and len(request.GET.getlist('machine_model')) > 1:
        request.session['part_name'] = request.GET.getlist('part_name')
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        request.session['machine_model'] = request.GET.getlist('machine_model')
        osr_list = OSR.objects.filter(
            ~Q(Sent_Parts='nan'), Q(Sent_Parts__isnull=False)
            )
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        models_list = request.GET.getlist('machine_model')
        parts_list = request.GET.getlist('part_name')
        query_result = osr_filter.qs.filter(TV_Model__in=models_list)
        if query_result.count() == 0:
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)
            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'There is no data with your search conditions so far.',
                }
            return render(request, 'osr_unusual.html',context)
        df = pd.DataFrame(list(query_result.values()))
        df.Import_Date = pd.to_datetime(df.Import_Date)
        df['month'] = df.Import_Date.dt.strftime('%y-%m')
        df2 = df[['month', 'TV_Model', 'Sent_Parts']].copy(deep=True)
        for i in parts_list:
            df2[str(i)] = df2.Sent_Parts.str.count(str(i))
        # Todo: Get the sum of each part
        agg_way = dict()
        for i in parts_list:
            agg_way[i] = 'sum'

        month_stat = df2.groupby(['month', 'TV_Model']).agg(agg_way).reset_index()
        parts_percent_list = ['month', 'TV_Model']
        for i in parts_list:
            parts_percent_list.append(str(i)+' ')
            month_stat[str(i)+' '] = (month_stat[i] /
                month_stat[i].sum()) * 100
        month_stat = month_stat.fillna(0)
        stat = month_stat[parts_percent_list].to_dict('records')

        graph_list = []
        time = []
        series_dict = dict()
        for i in stat:
            if  i['month'] not in time:
                time.append(i['month'])
                for j in i.keys():
                    if j == 'month':
                        graph_list.append({'month': i['month']})
                    elif j == 'TV_Model':
                        continue
                    else:
                        graph_list[-1][j + '-' + i['TV_Model']] = i[j]
                        if j not in series_dict.keys():
                            series_dict[j] = [j + '-' + i['TV_Model']]
                        else:
                            if j + '-' + i['TV_Model'] not in series_dict[j]:
                                series_dict[j].append(j + '-' + i['TV_Model'])
            else:
                for j in i.keys():
                    if j == 'month':
                        continue
                    elif j == 'TV_Model':
                        continue
                    else:
                        graph_list[-1][j + '-' + i['TV_Model']] = i[j]
                        if j not in series_dict.keys():
                            series_dict[j] = [j + '-' + i['TV_Model']]
                        else:
                            if j + '-' + i['TV_Model'] not in series_dict[j]:
                                series_dict[j].append(j + '-' + i['TV_Model'])


        # week data
        df['week'] = df.Import_Date.dt.strftime('%y-%V')
        df3 = df[['week','TV_Model', 'Sent_Parts']]

        for i in parts_list:
            df3[str(i)] = df3.Sent_Parts.str.count(str(i))

        # Todo: Get the sum of each part
        week_stat = df3.groupby(['week', 'TV_Model']).agg(agg_way).reset_index()
        parts_percent_list = ['week', 'TV_Model']
        for i in parts_list:
            parts_percent_list.append(str(i)+' ')
            week_stat[str(i)+' '] = (week_stat[i] /
                week_stat[i].sum()) * 100
        week_stat = week_stat.fillna(0)
        stat = week_stat[parts_percent_list].to_dict('records')

        graph_list_week = []
        time_week = []
        for i in stat:
            if  i['week'] not in time_week:
                time_week.append(i['week'])
                for j in i.keys():
                    if j == 'week':
                        graph_list_week.append({'week': i['week']})
                    elif j == 'TV_Model':
                        continue
                    else:
                        graph_list_week[-1][j + '-' + i['TV_Model']] = i[j]
            else:
                for j in i.keys():
                    if j == 'week':
                        continue
                    elif j == 'TV_Model':
                        continue
                    else:
                        graph_list_week[-1][j + '-' + i['TV_Model']] = i[j]

        context = {
        'filter':osr_filter,
        'search_type': 'both',
        'graph_list':graph_list,
        'all_parts_list':parts_list,
        'graph_list_week':graph_list_week,
        'models_list': models_list,
        'series_dict': series_dict
        }
        return render(request, 'osr_unusual.html', context)

    ## catch ilegal search
    if len(request.GET.getlist('part_name')) == 1 and len(request.GET.getlist('machine_model')) == 1 or len(request.GET.getlist('part_name')) > 1 and len(request.GET.getlist('machine_model')) == 1 or len(request.GET.getlist('part_name')) == 1 and len(request.GET.getlist('machine_model')) > 1:
        osr_list = OSR.objects.filter(
            ~Q(Sent_Parts='nan'), ~Q(Sent_Parts__isnull=True)
            )
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)

        all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
        all_parts_list = list()
        for i in all_parts_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_parts_list:
                                        all_parts_list.append(k)

        all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
        all_models_list = list()
        for i in all_models_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_models_list:
                                        all_models_list.append(k)

        context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'The search scenario is ilegal. Choices are (1)select only one machine model, (2)select only one part name, or (3)select multiple machine models(>1) and part names(>1) at the same time. \
                    Please refer to UI design document.',
                }
        return render(request, 'osr_unusual.html',context)

    ##  scenario 3: part selected
    if 'machine_model' not in request.GET.keys() and request.GET['part_name']:
        request.session['part_name'] = request.GET['part_name']
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        if 'machine_model' in request.session.keys():
            del request.session['machine_model']
        osr_list = OSR.objects.filter(
            ~Q(Sent_Parts='nan'), Q(Sent_Parts__isnull=False)
            )
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        query_result = osr_filter.qs.filter(Sent_Parts__icontains=request.GET['part_name'])
        if query_result.count() == 0:
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)
            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'There is no data with your search conditions so far.',
                }
            return render(request, 'osr_unusual.html',context)
        models_queryset = query_result.values_list('TV_Model').distinct()
        models_list = list()
        for i in models_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in models_list:
                                        models_list.append(str(k))
        df = pd.DataFrame(list(query_result.values()))
        df.Import_Date = pd.to_datetime(df.Import_Date)
        df['month'] = df.Import_Date.dt.strftime('%y-%m')
        df_stat = df[['month', 'TV_Model']]
        month_model_sum_df = df_stat.groupby(['month','TV_Model']).size().reset_index(name='month_model_sum')
        model_sum_df = df_stat.groupby(['TV_Model']).size().reset_index(name='model_sum')
        out = (month_model_sum_df.merge(model_sum_df, left_on='TV_Model', right_on='TV_Model').reindex(columns=['month', 'TV_Model', 'model_sum', 'month_model_sum']))
        out['percentage'] = out['month_model_sum'].div(out['model_sum'].values,axis=0)
        graph_df_dict = out[['month', 'TV_Model', 'percentage']].to_dict('records')
        # calculate each part's stat
        graph_list = []
        time = []
        for i in graph_df_dict:
            if  i['month'] not in time:
                time.append(i['month'])
                graph_list.append({'month': i['month'], i['TV_Model']: "{:.4f}".format(i['percentage'])})
            else:
                for j in graph_list:
                    if j['month'] == i['month']:
                        j[i['TV_Model']] = "{:.4f}".format(i['percentage'])

        df['week'] = df.Import_Date.dt.strftime('%y-%V')
        df_stat_week = df[['week', 'TV_Model']]
        week_model_sum_df = df_stat_week.groupby(['week','TV_Model']).size().reset_index(name='week_model_sum')
        week_out = (week_model_sum_df.merge(model_sum_df, left_on='TV_Model', right_on='TV_Model').reindex(columns=['week', 'TV_Model', 'model_sum', 'week_model_sum']))
        week_out['percentage'] = week_out['week_model_sum'].div(week_out['model_sum'].values,axis=0)
        graph_df_dict_week = week_out[['week', 'TV_Model', 'percentage']].to_dict('records')
        # calculate each part's stat
        graph_list_week = []
        time_week = []
        for i in graph_df_dict_week:
            if  i['week'] not in time_week:
                time_week.append(i['week'])
                graph_list_week.append({'week': i['week'], i['TV_Model']: "{:.4f}".format(i['percentage'])})
            else:
                for j in graph_list_week:
                    if j['week'] == i['week']:
                        j[i['TV_Model']] = "{:.4f}".format(i['percentage'])


        context = {
        'filter':osr_filter,
        'search_type': 'part_only',
        'graph_list':graph_list,
        'models_list':models_list,
        'graph_list_week':graph_list_week
        }
        return render(request, 'osr_unusual.html', context)

    ## scenario 2: machine selected
    if 'part_name' not in request.GET.keys() and request.GET['machine_model']:

        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        request.session['machine_model'] = request.GET['machine_model']
        if 'part_name' in request.session.keys():
            del request.session['part_name']

        osr_list = OSR.objects.filter(
            ~Q(Sent_Parts='nan'), Q(Sent_Parts__isnull=False)
            )
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        query_result = osr_filter.qs.filter(TV_Model__icontains=request.GET['machine_model'])
        if query_result.count() == 0:
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)
            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'There is no data with your search conditions so far.',
                }
            return render(request, 'osr_unusual.html',context)
        df = pd.DataFrame(list(query_result.values()))
        df.Import_Date = pd.to_datetime(df.Import_Date)
        df['month'] = df.Import_Date.dt.strftime('%y-%m')
        df2 = df[['month', 'Sent_Parts']]
        all_parts_queryset = query_result.values_list('Sent_Parts').distinct()
        all_parts_list = list()
        for i in all_parts_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_parts_list:
                                        all_parts_list.append(k)
        for i in all_parts_list:
            df2[str(i)] = df2.Sent_Parts.str.count(str(i))

        agg_way = dict()
        for i in all_parts_list:
            agg_way[i] = 'sum'

        month_stat = df2.groupby(['month']).agg(agg_way).reset_index()

        all_parts_percent_list = ['month']
        for i in all_parts_list:
            all_parts_percent_list.append(str(i)+' ')
            month_stat[str(i)+' '] = (month_stat[i] /
                month_stat[i].sum()) * 100
        graph_list = month_stat[all_parts_percent_list].to_dict('records')


        # total = df2.sum()
        # total.name = 'Total'
        # month_stat = month_stat.append(total.transpose())
        # month_stat[all_parts_list] = month_stat[all_parts_list].div(total[all_parts_list],axis=0)
        # all_parts_list.append('month')
        # graph_list = month_stat[all_parts_list].to_dict('records')
        # week data
        df['week'] = df.Import_Date.dt.strftime('%y-%V')
        df3 = df[['week', 'Sent_Parts']]
        for i in all_parts_list:
            df3[str(i)] = df3.Sent_Parts.str.count(str(i))

        week_stat = df3.groupby(['week']).agg(agg_way).reset_index()
        all_parts_percent_list_week = ['week']
        for i in all_parts_list:
            all_parts_percent_list_week.append(str(i)+' ')
            week_stat[str(i)+' '] = (week_stat[i] /
                week_stat[i].sum()) * 100
        graph_list_week = week_stat[all_parts_percent_list_week].to_dict('records')


        context = {
        'filter':osr_filter,
        'search_type': 'machine_model_only',
        'graph_list':graph_list,
        'all_parts_list':all_parts_list,
        'graph_list_week':graph_list_week
        }
        return render(request, 'osr_unusual.html', context)



    else:
        osr_list = OSR.objects.filter(
            ~Q(Sent_Parts='nan'), Q(Sent_Parts__isnull=False)
            )
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'Your search condition does not follow the search logic defined before.',
                }
        return render(request, 'osr_unusual.html',context)


def count_parts (row):
    return len(row['Sent_Parts'].split(','))


def osr_usage(request):
    """
    docstring
    """
    if 'start_date' not in request.GET.keys():
        osr_list = OSR.objects.filter(
            ~Q(Sent_Parts='nan'), ~Q(Sent_Parts__isnull=True)
            )
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)

        all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
        all_parts_list = list()
        for i in all_parts_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_parts_list:
                                        all_parts_list.append(k)

        all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
        all_models_list = list()
        for i in all_models_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_models_list:
                                        all_models_list.append(k)
        context = {
            'filter':osr_filter,
            'all_parts_list': all_parts_list,
            'all_models_list': all_models_list,
            }


        return render(request, 'osr_usage.html', context)

    ## scenario 1: both selected
    if len(request.GET.getlist('part_name')) > 1 and len(request.GET.getlist('machine_model')) > 1:
        request.session['part_name'] = request.GET.getlist('part_name')
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        request.session['machine_model'] = request.GET.getlist('machine_model')
        osr_list = OSR.objects.filter(
            ~Q(Sent_Parts='nan'), Q(Sent_Parts__isnull=False)
            )
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        models_list = request.GET.getlist('machine_model')
        parts_list = request.GET.getlist('part_name')
        query_result = osr_filter.qs.filter(TV_Model__in=models_list)
        if query_result.count() == 0:
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)
            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'There is no data with your search conditions so far.',
                }
            return render(request, 'osr_usage.html',context)

        df = pd.DataFrame(list(query_result.values()))
        df.Import_Date = pd.to_datetime(df.Import_Date)
        df['month'] = df.Import_Date.dt.strftime('%y-%m')
        df2 = df[['month', 'TV_Model', 'Sent_Parts']].copy(deep=True)
        for i in parts_list:
            df2[str(i)] = df2.Sent_Parts.str.count(str(i))
        # Get the sum of each month and TV_Model

        df2['total'] = df2.apply (lambda row: count_parts(row), axis=1)
        stat_df = df2.groupby(['month', 'TV_Model']).agg({'total':'sum'}).reset_index()

        # Get the stat ready
        agg_way = dict()
        for i in parts_list:
            agg_way[i] = 'sum'

        month_stat = df2.groupby(['month', 'TV_Model']).agg(agg_way).reset_index()
        month_stat['total'] = stat_df['total']
        month_stat[parts_list] = month_stat[parts_list].div(month_stat['total'].values,axis=0)
        output_cols = ['month', 'TV_Model'] + parts_list
        stat = month_stat[output_cols].to_dict('records')

        graph_list = []
        time = []
        series_dict = dict()
        for i in stat:
            if  i['month'] not in time:
                time.append(i['month'])
                for j in i.keys():
                    if j == 'month':
                        graph_list.append({'month': i['month']})
                    elif j == 'TV_Model':
                        continue
                    else:
                        graph_list[-1][j + '-' + i['TV_Model']] = i[j]
                        if j not in series_dict.keys():
                            series_dict[j] = [j + '-' + i['TV_Model']]
                        else:
                            if j + '-' + i['TV_Model'] not in series_dict[j]:
                                series_dict[j].append(j + '-' + i['TV_Model'])
            else:
                for j in i.keys():
                    if j == 'month':
                        continue
                    elif j == 'TV_Model':
                        continue
                    else:
                        graph_list[-1][j + '-' + i['TV_Model']] = i[j]
                        if j not in series_dict.keys():
                            series_dict[j] = [j + '-' + i['TV_Model']]
                        else:
                            if j + '-' + i['TV_Model'] not in series_dict[j]:
                                series_dict[j].append(j + '-' + i['TV_Model'])

        print(series_dict)
        # week data
        df['week'] = df.Import_Date.dt.strftime('%y-%V')
        df3 = df[['week','TV_Model', 'Sent_Parts']]

        for i in parts_list:
            df3[str(i)] = df3.Sent_Parts.str.count(str(i))

        df3['total'] = df3.apply (lambda row: count_parts(row), axis=1)
        total_week_df = df3.groupby(['week', 'TV_Model']).agg({'total': 'sum'}).reset_index()
        week_stat = df3.groupby(['week', 'TV_Model']).agg(agg_way).reset_index()

        week_stat['total'] = total_week_df['total']
        week_stat[parts_list] = week_stat[parts_list].div(week_stat['total'].values,axis=0)
        output_cols_wk = ['week', 'TV_Model'] + parts_list
        stat_wk = week_stat[output_cols_wk]
        stat_wk = stat_wk.to_dict('records')
        graph_list_week = []
        time_week = []
        for i in stat_wk:
            if  i['week'] not in time_week:
                time_week.append(i['week'])
                for j in i.keys():
                    if j == 'week':
                        graph_list_week.append({'week': i['week']})
                    elif j == 'TV_Model':
                        continue
                    else:
                        graph_list_week[-1][j + '-' + i['TV_Model']] = i[j]

            else:
                for j in i.keys():
                    if j == 'week':
                        continue
                    elif j == 'TV_Model':
                        continue
                    else:
                        graph_list_week[-1][j + '-' + i['TV_Model']] = i[j]


        context = {
        'filter':osr_filter,
        'search_type': 'both',
        'graph_list':graph_list,
        'all_parts_list':parts_list,
        'graph_list_week':graph_list_week,
        'models_list': models_list,
        'series_dict': series_dict
        }
        return render(request, 'osr_usage.html', context)

    ## catch ilegal search
    elif len(request.GET.getlist('part_name')) >= 1 and len(request.GET.getlist('machine_model')) == 1 or len(request.GET.getlist('part_name')) == 1 and len(request.GET.getlist('machine_model')) >= 1 :
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)
            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'The search scenario is ilegal. Choices are (1)select only one machine model, (2)select only one part name, or (3)select multiple machine models(>1) and part names(>1) at the same time. \
                    Please refer to UI design document.',
                }
            return render(request, 'osr_usage.html',context)

    ##  scenario 3: part selected
    if 'machine_model' not in request.GET.keys() and request.GET['part_name']:
        request.session['part_name'] = request.GET['part_name']
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        if 'machine_model' in request.session.keys():
            del request.session['machine_model']
        osr_list = OSR.objects.filter(
            ~Q(Sent_Parts='nan'), Q(Sent_Parts__isnull=False)
            )
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        query_result = osr_filter.qs
        if query_result.count() == 0:
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)
            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'There is no data with your search conditions so far.',
                }
            return render(request, 'osr_usage.html',context)
        models_queryset = query_result.values_list('TV_Model').distinct()
        models_list = list()
        for i in models_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in models_list:
                                        models_list.append(str(k))
        df = pd.DataFrame(list(query_result.values()))
        df.Import_Date = pd.to_datetime(df.Import_Date)
        df['parts_count'] = df.apply (lambda row: count_parts(row), axis=1)
        df['contains_searched_part'] = df['Sent_Parts'].str.contains(request.GET['part_name'])
        # df['contains_search_part'] = df.Sent_Parts.str.count(str(i))
        df['month'] = df.Import_Date.dt.strftime('%y-%m')
        df_stat = df[['month', 'TV_Model', 'parts_count', 'contains_searched_part']]
        # month_model_sum = df_stat.groupby(['month','TV_Model']).agg({'parts_count':'sum'}).reset_index().to_dict('records')
        month_model_sum_df = df_stat.groupby(['month','TV_Model']).agg({'parts_count':'sum'}).reset_index()
        month_model_contains_count_df = df_stat.groupby(['month','TV_Model']).agg({'contains_searched_part':'sum'}).reset_index()
        month_model_sum_df['contains_searched_part'] = month_model_contains_count_df['contains_searched_part']
        month_model_sum_df['percentage'] = month_model_sum_df['contains_searched_part'] / month_model_sum_df['parts_count']
        graph_df_dict = month_model_sum_df[['month', 'TV_Model', 'percentage']].to_dict('records')
        # calculate each part's stat
        graph_list = []
        time = []
        for i in graph_df_dict:
            if  i['month'] not in time:
                time.append(i['month'])
                graph_list.append({'month': i['month'], i['TV_Model']: "{:.4f}".format(i['percentage'])})
            else:
                graph_list[-1][i['TV_Model']] = "{:.4f}".format(i['percentage'])

        df['week'] = df.Import_Date.dt.strftime('%y-%V')
        df_stat_week = df[['week', 'TV_Model', 'parts_count', 'contains_searched_part']]
        week_model_sum_df = df_stat_week.groupby(['week','TV_Model']).agg({'parts_count':'sum'}).reset_index()
        week_model_contains_count_df = df_stat_week.groupby(['week','TV_Model']).agg({'contains_searched_part':'sum'}).reset_index()
        week_model_sum_df['contains_searched_part'] = week_model_contains_count_df['contains_searched_part']
        week_model_sum_df['percentage'] = week_model_sum_df['contains_searched_part'] / week_model_sum_df['parts_count']
        graph_df_dict_week = week_model_sum_df[['week', 'TV_Model', 'percentage']].to_dict('records')
        # calculate each part's stat
        graph_list_week = []
        time_week = []
        for i in graph_df_dict_week:
            if  i['week'] not in time_week:
                time_week.append(i['week'])
                graph_list_week.append({'week': i['week'], i['TV_Model']: "{:.4f}".format(i['percentage'])})
            else:
                graph_list_week[-1][i['TV_Model']] = "{:.4f}".format(i['percentage'])

        context = {
        'filter':osr_filter,
        'search_type': 'part_only',
        'graph_list':graph_list,
        'models_list':models_list,
        'graph_list_week':graph_list_week
        }
        return render(request, 'osr_usage.html', context)

    ## scenario 2: machine selected
    if 'part_name' not in request.GET.keys() and request.GET['machine_model']:
        request.session['machine_model'] = request.GET['machine_model']
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        if 'part_name' in request.session.keys():
            del request.session['part_name']
        osr_list = OSR.objects.filter(
            ~Q(Sent_Parts='nan'), Q(Sent_Parts__isnull=False)
            )
        osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
        query_result = osr_filter.qs.filter(TV_Model__icontains=request.GET['machine_model'])
        if query_result.count() == 0:
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)
            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'There is no data with your search conditions so far.',
                }
            return render(request, 'osr_usage.html',context)
        df = pd.DataFrame(list(query_result.values()))
        df.Import_Date = pd.to_datetime(df.Import_Date)
        df['month'] = df.Import_Date.dt.strftime('%y-%m')
        df2 = df[['month', 'Sent_Parts']]
        all_parts_queryset = query_result.values_list('Sent_Parts').distinct()
        all_parts_list = list()
        for i in all_parts_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_parts_list:
                                        all_parts_list.append(k)
        for i in all_parts_list:
            df2[str(i)] = df2.Sent_Parts.str.count(str(i))

        agg_way = dict()
        for i in all_parts_list:
            agg_way[i] = 'sum'

        month_stat = df2.groupby(['month']).agg(agg_way).reset_index()
        month_stat['total'] = month_stat.sum(axis=1)
        month_stat[all_parts_list] = month_stat[all_parts_list].div(month_stat['total'].values,axis=0)
        all_parts_list.append('month')
        graph_list = month_stat[all_parts_list].to_dict('records')
        # week data
        df['week'] = df.Import_Date.dt.strftime('%y-%V')
        df3 = df[['week', 'Sent_Parts']]
        for i in all_parts_list:
            df3[str(i)] = df3.Sent_Parts.str.count(str(i))

        week_stat = df3.groupby(['week']).agg(agg_way).reset_index()
        week_stat['total'] = week_stat.sum(axis=1)
        all_parts_list = all_parts_list[:-1]
        week_stat[all_parts_list] = week_stat[all_parts_list].div(week_stat['total'].values,axis=0)
        all_parts_list.append('week')
        graph_list_week = week_stat[all_parts_list].to_dict('records')
        all_parts_list = all_parts_list[:-1]

        context = {
        'filter':osr_filter,
        'search_type': 'machine_model_only',
        'graph_list':graph_list,
        'all_parts_list':all_parts_list,
        'graph_list_week':graph_list_week
        }
        return render(request, 'osr_usage.html', context)



def osr_trend(request):
    """
    docstring
    """
    osr_list = OSR.objects.all()
    osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
    all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
    all_parts_list = list()
    for i in all_parts_queryset:
        if (i[0] is not None) and (i[0] != 'nan'):
            for j in i:
                    for k in j.split(','):
                            if k not in all_parts_list:
                                    all_parts_list.append(k)

    all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
    all_models_list = list()
    for i in all_models_queryset:
        if (i[0] is not None) and (i[0] != 'nan'):
            for j in i:
                    for k in j.split(','):
                            if k not in all_models_list:
                                    all_models_list.append(k)
    context = {
        'filter':osr_filter,
        'all_parts_list': all_parts_list,
        'all_models_list': all_models_list,
        }
    return render(request, 'osr_trend.html', context)

def osr_trend_result(request):
    """
    docstring
    """
    osr_list = OSR.objects.exclude(Sent_Parts='nan')
    osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
    ## nothing was selected
    if 'part_name' not in request.GET.keys() and 'machine_model' not in request.GET.keys():
        return redirect(osr_trend)

    ## scenario 1: both selected
    if len(request.GET.getlist('part_name')) > 1 and len(request.GET.getlist('machine_model')) > 1:
        models_list = request.GET.getlist('machine_model')
        parts_list = request.GET.getlist('part_name')
        request.session['part_name'] = parts_list
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        request.session['machine_model'] = models_list

        my_filter_qs = Q()
        for part in parts_list:
                    my_filter_qs = my_filter_qs | Q(Sent_Parts__icontains=part)
        query_result = osr_filter.qs.filter(TV_Model__in=models_list).filter(my_filter_qs)
        if query_result.count() == 0:
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)
            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'There is no data with your search conditions so far.',
                }
            return render(request, 'osr_trend.html',context)

        df = pd.DataFrame(list(query_result.values()))
        df.Import_Date = pd.to_datetime(df.Import_Date)
        df['month'] = df.Import_Date.dt.strftime('%y-%m')
        df2 = df[['month', 'TV_Model', 'Sent_Parts']]

        for i in parts_list:
            df2[str(i)] = df2.Sent_Parts.str.count(str(i))

        stat = df2.groupby(['month', 'TV_Model']).agg('sum').reset_index().to_dict('records')
        graph_list = []
        time = []
        series_dict = dict()
        for i in stat:
            for j in i.keys():
                    if j != 'month' and j != 'TV_Model':
                        if  i['month'] not in time:
                            time.append(i['month'])
                            graph_list.append({'month': i['month'], j + '-' + i['TV_Model'] : i[j]})
                            if j not in series_dict.keys():
                                series_dict[j] = [j + '-' + i['TV_Model']]
                            else:
                                if j + '-' + i['TV_Model'] not in series_dict[j]:
                                    series_dict[j].append(j + '-' + i['TV_Model'])
                        else:
                            graph_list[-1].update({j + '-' + i['TV_Model']  : i[j]})
                            if j not in series_dict.keys():
                                series_dict[j] = [j + '-' + i['TV_Model']]
                            else:
                                if j + '-' + i['TV_Model'] not in series_dict[j]:
                                    series_dict[j].append(j + '-' + i['TV_Model'])

        series_dict_total_length = 0
        for i in series_dict.values():
            series_dict_total_length += len(i)
        if series_dict_total_length > 30:
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)

            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'Ilegal Search Condition: Too many options selected.( > 30 items)',
                }
            return render(request, 'osr_trend.html',context)

        # week data
        df['week'] = df.Import_Date.dt.strftime('%y-%V')
        df3 = df[['week','TV_Model', 'Sent_Parts']]

        for i in parts_list:
            df3[str(i)] = df3.Sent_Parts.str.count(str(i))

        stat_week = df3.groupby(['week', 'TV_Model']).agg('sum').reset_index().to_dict('records')
        graph_list_week = []
        time_week = []
        for i in stat_week:
            for j in i.keys():
                    if j != 'week' and j != 'TV_Model':
                        if  i['week'] not in time_week:
                            time_week.append(i['week'])
                            graph_list_week.append({'week': i['week'], j + '-' + i['TV_Model'] : i[j]})
                        else:
                            graph_list_week[-1].update({j + '-' + i['TV_Model']  : i[j]})

        # for i in stat_week:
        #     if  i['week'] not in time_week:
        #         time_week.append(i['week'])
        #         for j in i.keys():
        #             if j != 'week' and j != 'TV_Model':
        #                 graph_list_week.append({'week': i['week'], j + '-' + i['TV_Model'] : i[j]})
        #     else:
        #         for j in i.keys():
        #             if j != 'week' and j != 'TV_Model':
        #                 graph_list_week[-1][j + '-' + i['TV_Model']]  = i[j]

        context = {
        'filter':osr_filter,
        'search_type': 'both',
        'graph_list':graph_list,
        'all_parts_list':parts_list,
        'graph_list_week':graph_list_week,
        'models_list': models_list,
        'series_dict': series_dict
        }
        return render(request, 'osr_trend.html', context)

    ## catch ilegal search
    elif len(request.GET.getlist('part_name')) > 1 and len(request.GET.getlist('machine_model')) == 1 or len(request.GET.getlist('part_name')) == 1 and len(request.GET.getlist('machine_model')) > 1 :
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)
            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'The search scenario is ilegal. Choices are (1)select only one machine model, (2)select only one part name, or (3)select multiple machine models(>1) and part names(>1) at the same time. \
                    Please refer to UI design document.',
                }
            return render(request, 'osr_trend.html',context)
    ##  scenario 3: part selected
    if 'machine_model' not in request.GET.keys() and request.GET['part_name']:
        request.session['part_name'] = request.GET['part_name']
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        if 'machine_model' in request.session.keys():
            del request.session['machine_model']
        query_result = osr_filter.qs.filter(Sent_Parts__icontains=request.GET['part_name'])

        if query_result.count() == 0:
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)
            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'There is no data with your search conditions so far.',
                }
            return render(request, 'osr_trend.html',context)

        models_queryset = query_result.values_list('TV_Model').distinct()
        models_list = list()
        for i in models_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in models_list:
                                        models_list.append(str(k))
        df = pd.DataFrame(list(query_result.values()))
        df.Import_Date = pd.to_datetime(df.Import_Date)
        df_month_dict = df.groupby([df.Import_Date.dt.strftime('%y-%m'),'TV_Model'])['Sent_Parts'].count().to_frame().to_dict()
        graph_list = []
        time = []
        for i in df_month_dict['Sent_Parts'].keys():
            if  i[0] not in time:
                time.append(i[0])
                graph_list.append({'month': i[0], i[1]: df_month_dict['Sent_Parts'][i]})
            else:
                graph_list[-1][i[1]] = df_month_dict['Sent_Parts'][i]

        df_week_dict = df.groupby([df.Import_Date.dt.strftime('%y-%V'),'TV_Model'])['Sent_Parts'].count().to_frame().to_dict()
        graph_list_week = []
        time_week = []
        for i in df_week_dict['Sent_Parts'].keys():
            if  i[0] not in time_week:
                time_week.append(i[0])
                graph_list_week.append({'week': i[0], i[1]: df_week_dict['Sent_Parts'][i]})
            else:
                graph_list_week[-1][i[1]] = df_week_dict['Sent_Parts'][i]



        context = {
        'filter':osr_filter,
        'search_type': 'part_only',
        'graph_list':graph_list,
        'models_list':models_list,
        'graph_list_week':graph_list_week
        }
        return render(request, 'osr_trend.html', context)

    ## scenario 2: machine selected
    if 'part_name' not in request.GET.keys() and request.GET['machine_model']:
        request.session['machine_model'] = request.GET['machine_model']
        request.session['start_date'] = request.GET['start_date']
        request.session['end_date'] = request.GET['end_date']
        if 'part_name' in request.session.keys():
            del request.session['part_name']
        query_result = osr_filter.qs.filter(TV_Model__icontains=request.GET['machine_model'])
        if query_result.count() == 0:
            osr_list = OSR.objects.exclude(Sent_Parts='nan')
            osr_filter = OSRDateFilter(request.GET, queryset=osr_list)
            all_parts_queryset = osr_list.values_list('Sent_Parts').distinct()
            all_parts_list = list()
            for i in all_parts_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_parts_list:
                                            all_parts_list.append(k)

            all_models_queryset = OSR.objects.all().values_list('TV_Model').distinct()
            all_models_list = list()
            for i in all_models_queryset:
                if (i[0] is not None) and (i[0] != 'nan'):
                    for j in i:
                            for k in j.split(','):
                                    if k not in all_models_list:
                                            all_models_list.append(k)
            context = {
                'filter':osr_filter,
                'all_parts_list': all_parts_list,
                'all_models_list': all_models_list,
                'error_msg': 'There is no data with your search conditions so far.',
                }
            return render(request, 'osr_trend.html',context)

        df = pd.DataFrame(list(query_result.values()))
        df.Import_Date = pd.to_datetime(df.Import_Date)
        df['month'] = df.Import_Date.dt.strftime('%y-%m')
        df2 = df[['month', 'Sent_Parts']]
        all_parts_queryset = query_result.values_list('Sent_Parts').distinct()
        all_parts_list = list()
        for i in all_parts_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in all_parts_list:
                                        all_parts_list.append(k)
        for i in all_parts_list:
            df2[str(i)] = df2.Sent_Parts.str.count(str(i))

        agg_way = dict()
        for i in all_parts_list:
            agg_way[i] = 'sum'

        graph_list = df2.groupby(['month']).agg(agg_way).reset_index().to_dict('records')
        # week data
        df['week'] = df.Import_Date.dt.strftime('%y-%V')
        df3 = df[['week', 'Sent_Parts']]

        for i in all_parts_list:
            df3[str(i)] = df3.Sent_Parts.str.count(str(i))

        graph_list_week = df3.groupby(['week']).agg(agg_way).reset_index().to_dict('records')

        context = {
        'filter':osr_filter,
        'search_type': 'machine_model_only',
        'graph_list':graph_list,
        'all_parts_list':all_parts_list,
        'graph_list_week':graph_list_week
        }
        return render(request, 'osr_trend.html', context)



    ## else:
    context = {
        'filter':osr_filter,
        'search_type': 'both'
        }

    return render(request, 'osr_trend.html', context)

def osr_maintain(request):
    """
    docstring
    """
    form = forms.OSRSearchForm()

    context = {
        'form':form,
        }


    return render(request, 'osr_maintain.html', context)

def osr_trend_multiple_select_week(request, jet):

    chart = [{
      "year": "Week1",
      "europe": 2.5,
      "namerica": 2.5,
      "asia": 2.1,
      "lamerica": 1.2,
      "meast": 0.2,
      "africa": 0.1
    }, {
      "year": "Week2",
      "europe": 2.6,
      "namerica": 2.7,
      "asia": 2.2,
      "lamerica": 1.3,
      "meast": 0.3,
      "africa": 0.1
    }, {
      "year": "Week3",
      "europe": 2.8,
      "namerica": 2.9,
      "asia": 2.4,
      "lamerica": 1.4,
      "meast": 0.3,
      "africa": 0.1
    }, {
      "year": "Week4",
      "europe": 2.8,
      "namerica": 2.9,
      "asia": 2.4,
      "lamerica": 1.4,
      "meast": 0.3,
      "africa": 0.1
    }, {
      "year": "Week5",
      "europe": 2.8,
      "namerica": 2.9,
      "asia": 2.4,
      "lamerica": 1.4,
      "meast": 0.3,
      "africa": 0.1
    }, {
      "year": "Week6",
      "europe": 2.8,
      "namerica": 2.9,
      "asia": 2.4,
      "lamerica": 1.4,
      "meast": 0.3,
      "africa": 0.1
    }, {
      "year": "Week7",
      "europe": 2.8,
      "namerica": 2.9,
      "asia": 2.4,
      "lamerica": 1.4,
      "meast": 0.3,
      "africa": 0.1
    }, {
      "year": "Week8",
      "europe": 2.8,
      "namerica": 2.9,
      "asia": 2.4,
      "lamerica": 1.4,
      "meast": 0.3,
      "africa": 0.1
    }, {
      "year": "Week9",
      "europe": 2.8,
      "namerica": 2.9,
      "asia": 2.4,
      "lamerica": 1.4,
      "meast": 0.3,
      "africa": 0.1
    }, {
      "year": "Week10",
      "europe": 2.8,
      "namerica": 2.9,
      "asia": 2.4,
      "lamerica": 1.4,
      "meast": 0.3,
      "africa": 0.1
    }, {
      "year": "Week11",
      "europe": 2.8,
      "namerica": 2.9,
      "asia": 2.4,
      "lamerica": 1.4,
      "meast": 0.3,
      "africa": 0.1
    }, {
      "year": "Week12",
      "europe": 2.8,
      "namerica": 2.9,
      "asia": 2.4,
      "lamerica": 1.4,
      "meast": 0.3,
      "africa": 0.1
    }]

    return JsonResponse(chart, safe=False)

def osr_usage_multiple_select_week(request, jet):
    chart = ''
    return JsonResponse(chart, safe=False)

def export_latest_defect_mapping_table_xlsx(request):
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df = pd.DataFrame(list(Defect.objects.all().values()))
            df.to_excel(writer, sheet_name="Sheet1", index=False)
            writer.save()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="Defect Code Mapping Table.xlsx"'
            return response

def export_latest_special_usage_rule_xlsx(request):
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df = pd.DataFrame(list(SpecialUsageRule.objects.all().values('SRType',	'Created_Date',	'Closed_Date','Model','ErrorCode','Parts_delete','Parts_added',	'Remark')))
            df.to_excel(writer, sheet_name="SRQs", index=False)
            writer.save()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="OSR_special_usage_rule.xlsx"'
            return response

def export_latest_combo_parts_list_xlsx(request):
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df = pd.DataFrame(list(ComboPartsList.objects.all().values('Vizio_Model', 'INX_Model', 'Parts', 'Combo_Function')))
            df.to_excel(writer, sheet_name="Sheet1", index=False)
            writer.save()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="combo parts list.xlsx"'
            return response

def export_latest_parts_price_xlsx(request):
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df = pd.DataFrame(list(PartsPrice.objects.all().values('TV_Model', 'Part_Description', 'Part_Price')))
            df.to_excel(writer, sheet_name="Sheet1", index=False)
            writer.save()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="parts price.xlsx"'
            return response

def export_osr_part_number_xlsx(request):
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df = pd.DataFrame(list(OsrPartNumber.objects.all().values('MODEL', 'CHILD_PRODUCT_ID', 'PART_DESCRIPTION','CHILD_DESCRIPTION','TCONLESS')))
            df.to_excel(writer, sheet_name="Sheet1", index=False)
            writer.save()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="OSR_part_number.xlsx"'
            return response


def export_osr_search_result(request):
    query_osr = request.session['query_osr']
    query_result = OSR.objects.filter(OSRNumber__in=query_osr)
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df = pd.DataFrame(list(query_result.values('OSRNumber', 'TV_Model', 'TV_SerialNo','Import_Date','ProblemDesc','ErrorCode',\
                'Sent_Parts','Predict_Sent_Parts')))
            df['Predict_Sent_Parts'] = df.Predict_Sent_Parts.apply(lambda x: x.split(','))
            df['Sent_Parts'] = df.Sent_Parts.apply(lambda x: x.split(','))
            df2 = df['Predict_Sent_Parts'].apply(lambda x: pd.Series(x)).stack().reset_index(level=1, drop=True).to_frame('Predict_Sent_Parts').join(df[['OSRNumber', 'TV_Model', 'TV_SerialNo','Import_Date','ProblemDesc','ErrorCode',\
                'Sent_Parts']], how='left')
            df2.reset_index(inplace=True)
            df3 = df['Sent_Parts'].apply(lambda x: pd.Series(x)).stack().reset_index(level=1, drop=True).to_frame('Sent_Parts').join(df2[['OSRNumber', 'TV_Model', 'TV_SerialNo','Import_Date','ProblemDesc','ErrorCode',\
                'Predict_Sent_Parts']], how='left')
            df3.reset_index(inplace=True)
            df4 = df3[['Sent_Parts','OSRNumber', 'TV_Model', 'TV_SerialNo','Import_Date','ProblemDesc','ErrorCode']]
            df4['Predict_Sent_Parts'] = ''
            df5 = df2[['Predict_Sent_Parts','OSRNumber', 'TV_Model', 'TV_SerialNo','Import_Date','ProblemDesc','ErrorCode']]
            df5['Sent_Parts'] = ''
            df6 = df4.append(df5)
            # df3.index += 1
            df6 = df6.sort_values(by=['OSRNumber'])
            df6.reset_index(inplace=True)
            df6.index += 1
            df6.columns = ['index','ITI parts usage','OSR no.','TV Model','TV SERIALNO','Date Ordered',	'ProblemDesc','Error code',	'Predict_parts']
            df6.to_excel(writer, sheet_name="Sheet1", index=True, index_label='Item', columns=['OSR no.', 'Date Ordered','TV Model','TV SERIALNO', 'ProblemDesc','Error code', 'Predict_parts', 'ITI parts usage'])
            worksheet = writer.sheets["Sheet1"]
            for idx, col in enumerate(df6):  # loop through all columns
                worksheet.set_column(idx, idx, 20)  # set column width
            writer.save()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="OSR Search Result.xlsx"'
            return response

def export_osr_dashboard_search_result(request):
    query_start_date = request.session['start_date']
    query_end_date = request.session['end_date']
    query_result = OSR.objects.filter(
        Q(Import_Date__gte=query_start_date), Q(Import_Date__lte=query_end_date)
        )
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df = pd.DataFrame(list(query_result.values('Work_Order', 'OSRNumber', 'TV_Model', 'TV_SerialNo','Import_Date','ProblemDesc',\
                'Sent_Parts','Predict_Sent_Parts','F2score','OverSent_Parts','UnderSent_Parts')))
            df.rename(columns = {'Sent_Parts' : 'Actual_used Parts'}, inplace = True)
            df.to_excel(writer, sheet_name="Sheet1", index=False)
            worksheet = writer.sheets["Sheet1"]

            for idx, col in enumerate(df):  # loop through all columns
                worksheet.set_column(idx, idx, 20)  # set column width
            workbook  = writer.book
            worksheet2 = workbook.add_worksheet()
            calculation = query_result.filter(~Q(F2score='nan'), ~Q(F2score__isnull=True)).aggregate(Avg('F2score')).get('F2score__avg')
            headers = ['總共件數','多寄件數','少寄件數','同時多/少寄件數','正確件數','等待驗證','平均F2score']
            data = [request.session['last_month_osr_amount'] ,request.session['last_month_only_oversent'], request.session['last_month_only_undersent'], \
                request.session['last_month_both_undersent_oversent'], request.session['last_month_both_correct'], request.session['last_month_others']\
                    ,calculation]
            for i in range(len(headers)):
                worksheet2.write(0, i, headers[i])
                worksheet2.write(1, i, data[i])
            writer.save()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="OSR Search Result.xlsx"'
            return response

def export_osr_dashboard_last_month_result(request):
    queryset = OSR.objects.all()
    last_month_last_day = datetime.datetime.utcnow().replace(day=1) - datetime.timedelta(days=1)
    last_month_first_day = last_month_last_day.replace(day=1)
    query_result = queryset.filter(
        Q(Import_Date__gte=last_month_first_day), Q(Import_Date__lte=last_month_last_day)
        )
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df = pd.DataFrame(list(query_result.values('Work_Order', 'OSRNumber', 'TV_Model', 'TV_SerialNo','Import_Date','ProblemDesc',\
                'Sent_Parts','Predict_Sent_Parts','F2score','OverSent_Parts','UnderSent_Parts')))
            df.rename(columns = {'Sent_Parts' : 'Actual_used Parts'}, inplace = True)
            df.to_excel(writer, sheet_name="Sheet1", index=False)
            worksheet = writer.sheets["Sheet1"]

            for idx, col in enumerate(df):  # loop through all columns
                worksheet.set_column(idx, idx, 20)  # set column width
            workbook  = writer.book
            worksheet2 = workbook.add_worksheet()
            calculation = query_result.filter(~Q(F2score='nan'), ~Q(F2score__isnull=True)).aggregate(Avg('F2score')).get('F2score__avg')
            headers = ['總共件數','多寄件數','少寄件數','同時多/少寄件數','正確件數','等待驗證','平均F2score']
            data = [request.session['last_month_osr_amount'] ,request.session['last_month_only_oversent'], request.session['last_month_only_undersent'], \
                request.session['last_month_both_undersent_oversent'], request.session['last_month_both_correct'], request.session['last_month_others']\
                    ,calculation]
            for i in range(len(headers)):
                worksheet2.write(0, i, headers[i])
                worksheet2.write(1, i, data[i])
            writer.save()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="OSR Search Result.xlsx"'
            return response

def cal_parts_sum(map_dict, row):
    sum = 0
    try:
        for i in row.Predict_Sent_Parts:
            if row.TV_Model in map_dict.keys():
                if i in map_dict[row.TV_Model].keys():
                    sum +=  map_dict[row.TV_Model][i]
        return sum
    except:
        return 0

def export_osr_value_graph_search_result(request):
    query_start_date = request.session['start_date']
    query_end_date = request.session['end_date']
    machine_model = request.session['machine_model']

    query_result = OSR.objects.filter(
        Q(Import_Date__gte=query_start_date), Q(Import_Date__lte=query_end_date), Q(TV_Model__in=machine_model),\
        ~Q(Predict_Sent_Parts__isnull=True), ~Q(Sent_Parts__isnull=True), ~Q(Predict_Sent_Parts='nan'), ~Q(Sent_Parts='nan')
        )
    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df = pd.DataFrame(list(query_result.values('OSRNumber', 'TV_Model', 'TV_SerialNo','Import_Date','ProblemDesc',\
                'Predict_Sent_Parts')))
            df['Predict_Sent_Parts'] = df.Predict_Sent_Parts.apply(lambda x: x.split(','))
            price_df_dict = pd.DataFrame(list(PartsPrice.objects.filter(TV_Model__in=machine_model).values())).to_dict('records')
            price_df_dict1 = dict()
            models_list = list()
            for i in price_df_dict:
                if i['TV_Model'] not in models_list:
                    models_list.append(i['TV_Model'])
                    price_df_dict1[i['TV_Model']] = dict()
                    price_df_dict1[i['TV_Model']][i['Part_Description']] = float(i['Part_Price'])
                else:
                    price_df_dict1[i['TV_Model']][i['Part_Description']] = float(i['Part_Price'])
            try:
                df['Part_Price'] = df.apply(lambda row: cal_parts_sum(price_df_dict1, row), axis=1)
            except Exception as e:
                context = {
                    'error_msg': 'Did you provide a full list of part price yet? There are some parts\' price missing.',
                    }
                return render(request, 'osr_value_graph.html',context)
            df.columns = ['OSR #','TV Model','TV SERIALNO','Date Issued','ProblemDesc', 'Part_Description', 'Part_Price']
            df[['OSR #','TV Model','TV SERIALNO','Date Issued','ProblemDesc','Part_Description', 'Part_Price']].to_excel(writer, sheet_name="Sheet1", index=False)
            worksheet = writer.sheets["Sheet1"]

            for idx, col in enumerate(df):  # loop through all columns
                worksheet.set_column(idx, idx, 20)  # set column width
            writer.save()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="OSR Search Result.xlsx"'
            return response

def export_osr_trend_search_result(request):
    query_start_date = request.session['start_date']
    query_end_date = request.session['end_date']
    if 'machine_model' in request.session.keys() and 'part_name' in request.session.keys():
        machine_model = request.session['machine_model']
        part_name = request.session['part_name']
        my_filter_qs = Q()
        for part in part_name:
                    my_filter_qs = my_filter_qs | Q(Sent_Parts__icontains=part)
        query_result = OSR.objects.filter(
            Q(Import_Date__gte=query_start_date), Q(Import_Date__lte=query_end_date), Q(TV_Model__in=machine_model)
            ).filter(my_filter_qs)

    elif 'machine_model' in request.session.keys():
        machine_model = request.session['machine_model']
        query_result = OSR.objects.filter(
            Q(Import_Date__gte=query_start_date), Q(Import_Date__lte=query_end_date), Q(TV_Model=machine_model)
            )
        all_parts_queryset = query_result.values_list('Sent_Parts').distinct()
        part_name = list()
        for i in all_parts_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in part_name:
                                        part_name.append(k)
    elif 'part_name' in request.session.keys():
        part_name = request.session['part_name']
        query_result = OSR.objects.filter(
            Q(Import_Date__gte=query_start_date), Q(Import_Date__lte=query_end_date), Q(Sent_Parts__icontains=part_name)
            )
        part_name = [part_name]

    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df = pd.DataFrame(list(query_result.values('Work_Order','OSRNumber','Import_Date', 'TV_Model', 'TV_SerialNo','Sent_Parts')))
            df['Sent_Parts'] = df.Sent_Parts.apply(lambda x: x.split(','))
            df2 = df['Sent_Parts'].apply(lambda x: pd.Series(x)).stack().reset_index(level=1, drop=True).to_frame('Sent_Part1').join(df[['Work_Order','OSRNumber','Import_Date', 'TV_Model', 'TV_SerialNo']], how='left')
            df3 = df2[df2['Sent_Part1'].isin(part_name)]
            df3 = df3.rename(columns={"Sent_Part1": "Part_Description", "Work_Order": "Work Order #","OSRNumber":"OSR #","TV_Model":"TV Model",\
                "TV_SerialNo": "TV SERIALNO","Import_Date": "Import Date"})
            df3[['Work Order #','OSR #','Import Date','TV Model','TV SERIALNO','Part_Description']].to_excel(writer, sheet_name="Sheet1", index=False)
            worksheet = writer.sheets["Sheet1"]
            for idx, col in enumerate(df3):  # loop through all columns
                worksheet.set_column(idx, idx, 20)  # set column width
            writer.save()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="OSR Search Result.xlsx"'
            return response

def export_osr_distribution_search_result(request):
    query_start_date = request.session['start_date']
    query_end_date = request.session['end_date']
    if 'machine_model' in request.session.keys() and 'part_name' in request.session.keys():
        machine_model = request.session['machine_model']
        part_name = request.session['part_name']
        my_filter_qs = Q()
        for part in part_name:
                    my_filter_qs = my_filter_qs | Q(Sent_Parts__icontains=part)
        query_result = OSR.objects.filter(
            Q(Import_Date__gte=query_start_date), Q(Import_Date__lte=query_end_date), Q(TV_Model__in=machine_model)
            ).filter(my_filter_qs)

    elif 'machine_model' in request.session.keys():
        machine_model = request.session['machine_model']
        query_result = OSR.objects.filter(
            Q(Import_Date__gte=query_start_date), Q(Import_Date__lte=query_end_date), Q(TV_Model__in=machine_model)
            )
        all_parts_queryset = query_result.values_list('Sent_Parts').distinct()
        part_name = list()
        for i in all_parts_queryset:
            if (i[0] is not None) and (i[0] != 'nan'):
                for j in i:
                        for k in j.split(','):
                                if k not in part_name:
                                        part_name.append(k)
    elif 'part_name' in request.session.keys():
        part_name = request.session['part_name'][0]
        query_result = OSR.objects.filter(
            Q(Import_Date__gte=query_start_date), Q(Import_Date__lte=query_end_date), Q(Sent_Parts__icontains=part_name)
            )
        if type(part_name) != list:
            part_name = [part_name]

    with BytesIO() as b:
        with pd.ExcelWriter(b, engine='xlsxwriter') as writer:
            df = pd.DataFrame(list(query_result.values('Work_Order','OSRNumber','Import_Date', 'TV_Model', 'TV_SerialNo','Predict_Sent_Parts',\
            'Sent_Parts', 'ErrorCode', 'ProblemDesc')))
            df['Predict_Sent_Parts'] = df.Predict_Sent_Parts.apply(lambda x: x.split(','))
            df2 = df['Predict_Sent_Parts'].apply(lambda x: pd.Series(x)).stack().reset_index(level=1, drop=True).to_frame('Predict_Sent_Parts1').join(df[['Work_Order','OSRNumber','Import_Date', 'TV_Model', 'TV_SerialNo', 'Sent_Parts', 'ErrorCode', 'ProblemDesc']], how='left')
            df3 = df2[df2['Predict_Sent_Parts1'].isin(part_name)].reset_index()
            df3 = df3.rename(columns={"Predict_Sent_Parts1": "Part Description (Pre-dict)", "Work_Order": "Work Order #","OSRNumber":"OSR #","TV_Model":"TV Model",\
                "TV_SerialNo": "TV SERIALNO", "Sent_Parts": "OSR Vendor parts usage of description", "Import_Date": "Import Date"})
            df3[['Work Order #','OSR #','TV Model','TV SERIALNO','Part Description (Pre-dict)', 'OSR Vendor parts usage of description', 'Import Date',\
                'ErrorCode', 'ProblemDesc']].to_excel(writer, sheet_name="Sheet1", index=False)
            worksheet = writer.sheets["Sheet1"]

            for idx, col in enumerate(df3):  # loop through all columns
                worksheet.set_column(idx, idx, 20)  # set column width
            writer.save()
            response = HttpResponse(b.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="OSR Search Result.xlsx"'
            return response

@login_required
def download_pdf(request):
    with open('./mysite/static/text/高效能終端市場資訊預測系統說明書.pdf','rb') as fh:
        content = FileWrapper(fh)
        response = HttpResponse(content, content_type='application/pdf')
        response['Content-Length'] = os.path.getsize('./mysite/static/text/高效能終端市場資訊預測系統說明書.pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % '高效能終端市場資訊預測系統說明書.pdf'
        return response
