from ftplib import FTP
import os, glob
import logging
import pandas as pd
import json
# from text.models import foo
from django.db import connections
from django.db.models import Q
from functools import wraps
import requests
import time

from requests.adapters import HTTPAdapter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from text.models  import OSR, ComboPartsList, OsrPartNumber, SRQs, TMPSRQ

logging.basicConfig(filename='ftp.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.debug('Starting to grab the file.')

algorithm_ip = 'http://10.55.14.206'

host = 'ftp.avatekusa.com'
port = 21
usr = 'AvatekINNOLUX'
pwd = '#Inn0905#'
target_dir = '/INX_OSR IMPORT REPORT/C/INBOX/'
complete_dir = '/INX_OSR IMPORT REPORT/C/COMPLETE/'
predicted_msg_dir = '/INX_OSR IMPORT REPORT/D/INBOX/'
## Dev Env
# local_file_dir = 'D:\\D\\djangovue\\rma\\ftp\\'
# local_file_D_dir = 'D:\\D\\djangovue\\rma\\mysite\\text\\'
## Prod Env
local_file_dir = 'D:\\rma\\ftp\\'
local_file_D_dir = 'D:\\rma\\mysite\\text\\'

cwd = os.getcwd()

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))

print('Starting to grab the file.')
ftp = FTP()
ftp.connect(host, port)
ftp.login(usr, pwd)
ftp.dir()
ftp.cwd(target_dir)

def grabFile():
    target_filename = sorted(ftp.nlst(), key=lambda x: ftp.voidcmd(f"MDTM {x}"))[-1]
    abs_file_path = os.path.join(local_file_dir, target_filename)
    localfile = open(abs_file_path, 'wb+')
    ftp.retrbinary('RETR ' + target_filename, localfile.write, 1024)
    ftp.rename(target_dir + target_filename, complete_dir + target_filename)
    ftp.quit()
    print('Finished saving ' + target_filename + ' in ' + abs_file_path)
    logging.debug('Finished saving ' + target_filename + 'in ' + cwd)
    localfile.close()
    return abs_file_path

file_to_proceed = grabFile()
xl = pd.ExcelFile(file_to_proceed)
print('Starting to handle the dataframe...')

messageB = xl.parse("INX_OSR IMPORT MESSAGE C")
if all(x in list(messageB.columns) for x in ['Work Order #', 'OSR #', 'TV MODEL', 'TV SERIALNO', 'SKU', 'POP Date', 'ProblemDesc', 'Tech Name', 'Tech Address1', 'Tech Address2', 'Tech City', 'Tech State', 'Tech Phone', 'Part Number-1', 'Part Description-1', 'Part Number-2', 'Part Description-2', 'Part Number-3', 'Part Description-3', 'Part Number-4', 'Part Description-4', 'Part Number-5', 'Part Description-5', 'Part Number-6', 'Part Description-6','Note', 'Import Date']):
    messageB_fillna_with_none = messageB.where(pd.notnull(messageB), None)
    predict_data =  messageB_fillna_with_none.astype(str).to_dict(orient='records')
    base_data = OSR.objects.exclude(Train_Parts__isnull=True) \
                .filter(Import_Date__gte=(datetime.now().replace(day=1)- relativedelta(years=3))) \
                .values('OSRNumber', 'TV_Model', 'ProblemDesc', 'Train_Parts')
    base_data_dict = pd.DataFrame(list(base_data)).astype(str).to_dict(orient='records')
    combo_parts_dict = pd.DataFrame(list(ComboPartsList.objects.all().values('Vizio_Model','INX_Model','Parts','Combo_Function'))).astype(str).to_dict(orient='records')
    part_number_df = pd.DataFrame(list(OsrPartNumber.objects.all().values('MODEL','CHILD_PRODUCT_ID','PART_DESCRIPTION','CHILD_DESCRIPTION', 'TCONLESS')))
    # part_number_df.rename(columns={'Model': 'MODEL', 'Tconless': 'TCONLESS'}, inplace=True)
    part_number_dict = part_number_df.astype(str).to_dict(orient='records')
    t = s.get(algorithm_ip + ':4548/restart', json={'mode':'Restart'}, timeout=None)
    time.sleep(30)
    # r = s.get(algorithm_ip + ':4548', json={"base_data":base_data_dict, 'predict_data':predict_data, 'combo':combo_parts_dict, 'mode':'Pred'}, timeout=None)
    r = s.get(algorithm_ip + ':4548', json={"base_data":base_data_dict, 'predict_data':predict_data, 'combo':combo_parts_dict, 'part_number': part_number_dict, 'mode':'Pred'}, timeout=None)

    print(r.status_code)
    t = s.get(algorithm_ip + ':4548/restart', json={'mode':'Restart'}, timeout=None)
    _ = json.loads(r.text)['result']
    existing_osr_nr = list(OSR.objects.all().values_list('OSRNumber'))
    existing_osr_nr_list = list()
    for i in existing_osr_nr:
        existing_osr_nr_list.append(i[0])
    objs = []
    for i in _:
        if i['OSRNumber'] not in existing_osr_nr_list:
            objs.append(OSR(
                    Work_Order = str(i['Work_Order']),
                    OSRNumber = str(i['OSRNumber']),
                    TV_Model = str(i['TV_Model']),
                    TV_SerialNo = str(i['TV_SerialNo']),
                    Import_Date = str(i['Import_Date']),
                    ProblemDesc = str(i['ProblemDesc']),
                    Predict_Train_Parts = str(i['Predict_Train_Parts']),
                    Similar_OSRNumber = str(i['Similar_OSRNumber']),
                    Predict_Sent_Parts = str(i['Predict_Sent_Parts']),
                    Threshold_result = str(i['Threshold_result'])
                    ))
else:
    print('Data Format does not follow the convention.')
## Save back to DB
connections.close_all()
newlyCreatedOSRs = OSR.objects.bulk_create(objs)
OSR.objects.filter(
    Q(OverSent_Parts__isnull=True) | Q(OverSent_Parts='None')).update(OverSent_Parts='nan')
OSR.objects.filter(
    Q(UnderSent_Parts__isnull=True) | Q(UnderSent_Parts='None')).update(UnderSent_Parts='nan')
OSR.objects.filter(
    Q(Sent_Parts__isnull=True) | Q(Sent_Parts='None')).update(Sent_Parts='nan')
OSR.objects.filter(
    Q(Predict_Sent_Parts__isnull=True) | Q(Predict_Sent_Parts='None')).update(Predict_Sent_Parts='nan')
# ## Prepares the Message C.xlsx
result_df = pd.DataFrame(_)
result_for_excel_df = result_df[['Work_Order','OSRNumber','TV_Model','TV_SerialNo',"SKU","POP Date",\
    "Tech Name","Tech Address1", "Tech Address2", "Tech City", "Tech State", "Tech ZipCode", \
    "Tech Phone", "Part Number-1", "Part Description-1", "Part Number-2", "Part Description-2", "Part Number-3" ,\
    "Part Description-3", "Part Number-4", "Part Description-4", "Part Number-5", "Part Description-5", "Part Number-6", \
    "Part Description-6", "Outbound Tracking", "Return Tracking", "Ship Date", "Note"]]
result_for_excel_df_new = result_for_excel_df.rename(columns={'Work_Order': 'Work Order #', 'OSRNumber': 'OSR #', 'TV_Model': 'TV MODEL', 'TV_SerialNo':'TV SERIALNO'})
# result_for_excel_df_new.to_excel(filie_to_proceed,"INX_OSR IMPORT MESSAGE C", columns=['Work Order #', 'OSR #', 'TV MODEL', 'TV SERIALNO', 'SKU', 'POP Date', 'ProblemDesc', 'Tech Name', 'Tech Address1', 'Tech Address2', 'Tech City', 'Tech State', 'Tech ZipCode', 'Tech Phone', 'Part Number-1', 'Part Description-1', 'Part Number-2', 'Part Description-2', 'Part Number-3', 'Part Description-3', 'Part Number-4', 'Part Description-4', 'Part Number-5', 'Part Description-5', 'Part Number-6', 'Part Description-6', 'Note'], index=False)
result_for_excel_df_new.to_excel(file_to_proceed,"INX_OSR IMPORT MESSAGE C", columns=['Work Order #', 'OSR #', 'TV MODEL', 'TV SERIALNO',\
    'Tech Name','Tech Address1', 'Tech Address2', 'Tech City','Tech State','Tech ZipCode','Tech Phone', \
    'Part Number-1', 'Part Description-1','Part Number-2',  'Part Description-2', 'Part Number-3','Part Description-3',\
    'Part Number-4', 'Part Description-4', 'Part Number-5','Part Description-5',  'Part Number-6','Part Description-6', \
    'Outbound Tracking', 'Return Tracking', 'Ship Date', 'Note'], index=False)

## Send the file back to FTP
print('sleep for 120 seconds...')
time.sleep(120)
ftp.connect(host, port)
ftp.login(usr, pwd)
ftp.dir()
ftp.cwd(predicted_msg_dir)
list_of_files = glob.glob(local_file_dir +'*.xlsx')
latest_file = max(list_of_files, key=os.path.getctime)
file_name = os.path.basename(latest_file)
msg_D_file_name = file_name.replace('MESSAGE C', 'MESSAGE D')
print('sending '+ msg_D_file_name + ' back....')
file = open(latest_file,'rb')         # file to send
ftp.storbinary('STOR ' + msg_D_file_name, file)     # send the file
file.close()                                # close file and FTP
ftp.quit()
print('The Excel file has been successfully sent')
a = OSR.objects.filter(
        Q(ErrorCode='nan') | Q(ErrorCode__isnull=True))
for i in a:
    if SRQs.objects.filter(SRNumber=str(i.OSRNumber)).count() > 0:
        i.ErrorCode = SRQs.objects.filter(SRNumber=str(i.OSRNumber))[0].ErrorCode
        i.save()
for i in a:
    if TMPSRQ.objects.filter(SRNumber=str(i.OSRNumber)).count() > 0:
        i.ErrorCode = TMPSRQ.objects.filter(SRNumber=str(i.OSRNumber))[0].ErrorCode
        i.save()
print('Finished updating the ErrorCode')








