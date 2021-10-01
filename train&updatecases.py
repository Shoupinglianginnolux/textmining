import json, time
import django
import datetime
import os
import glob
import requests
from dateutil import parser
from dateutil.relativedelta import relativedelta
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from text.models import Cases, SRQs, TMPSRQ, Training
from distutils.util import strtobool
import pandas as pd

django.db.connections.close_all()
Training.objects.create(Ongoing=True)
print('Program started.')

temp_count = TMPSRQ.objects.all().count()
if temp_count < 3000:
    print("\nTmp SRQ is less than 3000 items. Program ends.")
else:
    print("\nThis is for the sake of last Saturday did not successfully train the algorithm. Do remember to recover this to less than 3000 to train.")
    tmp_srq = TMPSRQ.objects.all()
    tmp_srq_list = []
    for i in tmp_srq:
        tmp_srq_list.append(SRQs(
        SRNumber = i.SRNumber,
        SRType = i.SRType,
        CreatedDate	= i.CreatedDate,
        Model = i.Model,
        SerialNumber = i.SerialNumber,
        ErrorCode = i.ErrorCode,
        InternalNotes = i.InternalNotes,
        PredictErrorCode = i.PredictErrorCode,
        ReviseErrorCode = i.ReviseErrorCode,
        Train = i.Train,
        ))
    django.db.connections.close_all()
    print('finished disconnecting.')
    newlyCreatedSRQs = SRQs.objects.bulk_create(tmp_srq_list)
    tmp_srq.delete()
    print('\nFinished moving TmpSRQ')
    latest_record_date = SRQs.objects.all().order_by('-CreatedDate')[0].CreatedDate
    df = pd.DataFrame(list(SRQs.objects.filter(Train=True, CreatedDate__gt=latest_record_date+relativedelta(months=-18)).values('SRNumber', 'Model', 'ErrorCode', 'CreatedDate', 'InternalNotes','ReviseErrorCode', 'Train')))
    srqs_dict = df.astype(str).to_dict(orient='records')
    srqs_json = pd.DataFrame({'model': 'text.srqs', 'fields': srqs_dict}).to_dict('records')
    srqs_json = json.dumps(srqs_json, ensure_ascii=False)
    srqs_json = json.loads(srqs_json)
    print('\nFinished preparing training srqs data')
    json_sent = {'json':srqs_json, 'mode':'Train'}
    with open('json_sent.txt', 'w') as outfile:
        json.dump(json_sent, outfile)
    t = requests.get('http://127.0.0.1:4547/restart', json={'mode':'Restart'}, timeout=None)
    time.sleep(30)
    r = requests.get('http://127.0.0.1:4547', json=json_sent)
    t = requests.get('http://127.0.0.1:4547/restart', json={'mode':'Restart'}, timeout=None)
    srqs_json_result = json.loads(r.text)
    with open('srqs_json_result.txt', 'w') as outfile:
        json.dump(srqs_json_result, outfile)
    srqs_json_result = json.loads(srqs_json_result['predict_result'])
    django.db.connections.close_all()
    for idx, i in enumerate(srqs_json_result):
        if i['model'] == 'text.srqs':
            obj,created = SRQs.objects.update_or_create(
                SRNumber=str(i['fields']['SRNumber']),
                    defaults = {
                    'PredictErrorCode':str(i['fields']['PredictErrorCode']),
                    'Train':bool(strtobool(i['fields']['Train']))
                    })
    print('\nFinished updating srqs data')
    df = pd.DataFrame(list(Cases.objects.filter(CreatedDate__gt=datetime.datetime.today()+relativedelta(months=-6)).values('CaseNumber', 'Model', 'Description', 'CreatedDate')))
    cases_dict = df.astype(str).to_dict(orient='records')
    cases_json = pd.DataFrame({'model': 'text.cases', 'fields': cases_dict}).to_dict('records')
    cases_json = json.dumps(cases_json, ensure_ascii=False)
    cases_json = json.loads(cases_json)
    print('\nFinished preparing predict cases data')
    time.sleep(30)
    r = requests.get('http://127.0.0.1:4547', json={'json':cases_json, 'mode':'Pred'})
    t = requests.get('http://127.0.0.1:4547/restart', json={'mode':'Restart'}, timeout=None)
    cases_json_result = json.loads(r.text)
    cases_json_result = json.loads(cases_json_result['predict_result'])
    django.db.connections.close_all()
    for idx, i in enumerate(cases_json_result):
        if i['model'] == 'text.cases':
            obj,created = Cases.objects.update_or_create(
                CaseNumber=str(i['fields']['CaseNumber']),
                defaults = {
                    'PredictErrorCode':str(i['fields']['PredictErrorCode'] )})
    print('\nFinished updating cases data')

django.db.connections.close_all()
_ = Training.objects.all().order_by('-id')[0]
_.Ongoing=False
_.EndTime = datetime.datetime.now()
_.save()