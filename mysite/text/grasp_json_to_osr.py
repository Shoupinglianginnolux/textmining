from ftplib import FTP
import os
import logging
import pandas as pd
import json
# from text.models import foo
from django.db import connections
import re
import requests


from requests.adapters import HTTPAdapter
from datetime import datetime
from .models  import OSR

logging.basicConfig(filename='ftp.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.debug('Starting to grab the file.')


host = 'ftp.avatekusa.com'
port = 21
usr = 'AvatekINNOLUX'
pwd = '#Inn0905#'
target_dir = 'INX_OSR  PART SHIPPED REPORT'
target_filename = 'INX OSR PART SHIPPED REPORT 01252021-2000.csv'


cwd = os.getcwd()
abs_file_path = os.path.join(cwd, 'ftp/'+ target_filename)
print(abs_file_path)

algorithm_url = '127.0.0.1:8001'

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))

print('Starting to grab the file.')
# ftp = FTP()
# try:
#     ftp.connect(host, port)
# except:
#     logging.error('Connection failed.')
#     print ('Connection failed.')

# try:
#     ftp.login(usr, pwd)
# except:
#     logging.error('Logging failed.')
#     print ('Logging failed.')

# ftp.dir()
# ftp.cwd(target_dir)

# def grabFile(filename):
#     localfile = open(abs_file_path, 'wb')
#     ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
#     ftp.quit()
#     localfile.close()



# try:
#     grabFile(target_filename)
#     print('Finished saving ' + target_filename + ' in ' + abs_file_path)
#     logging.debug('Finished saving ' + target_filename + 'in ' + cwd)
# except:
#     logging.error('Downloading failed.')
#     print ('Downloading failed.')


# xl = pd.ExcelFile(abs_file_path)
# messageB = xl.parse("Sheet1")
# if all(x in list(messageB.columns) for x in ['Work Order #','OSR #','TV Model','TV SerialNo','SKU',	'POP Date','ProblemDesc','Tech Name','Tech Address1','Tech Address2','Tech City','Tech State','Tech ZipCode','Tech Phone','Import Date']):
#     predict_data =messageB.astype(str).to_dict(orient='records')
#     base_data = OSR.objects.exclude(Train_Parts__isnull=True) \
#                 .filter(POP_Date__gte=(datetime.now().replace(day=1)- datetime.timedelta(years=3))) \
#                 .values('OSR #', 'TV Model', 'ProblemDesc', 'Train_Parts')
#     base_data_dict = pd.DataFrame(list(base_data)).to_dict(orient='records')
#     combo_parts_dict = pd.DataFrame(list(bar.objects.all())).to_dict(orient='records')
    # r = s.get('http://'+algorithm_url, json={"base_data":base_data_dict, 'predict_data':predict_data, 'combo':combo_parts_dict, 'mode':'Pred'}, timeout=None)
try:
    # r = s.get('http://'+algorithm_url, json={'mode':'Pred'}, timeout=None)
    # _ = json.loads(r.text)['result']
    df = pd.read_json("complete_result_20210218.json", orient='records')
    df['Import_Date'] = pd.to_datetime(df['Import_Date'])
    df = df.where(pd.notnull(df), None)
    df.reset_index(drop=True, inplace=True)
    objs = []
    for i in range(len(df['OSRNumber'])):
        if df['F2score'][i] is None:
            objs.append(OSR(
                    OSRNumber=str(df['OSRNumber'][i]),
                    TV_Model= (str(df['TV_Model'][i])),
                    TV_SerialNo= (str(df['TV_SerialNo'][i])),
                    Work_Order=(str(df['Work_Order'][i])),
                    Import_Date= df['Import_Date'][i].strftime("%Y-%m-%d"),
                    ProblemDesc=str(df['ProblemDesc'][i]),
                    Train_Parts=str(df['Train_Parts'][i]),
                    Sent_Parts=str(df['Sent_Parts'][i]),
                    Predict_Train_Parts=str(df['Predict_Train_Parts'][i]),
                    Predict_Sent_Parts=str(df['Predict_Sent_Parts'][i]),
                    Similar_OSRNumber=str(df['Similar_OSRNumber'][i]),
                    OverSent_Parts=str(df['OverSent_Parts'][i]),
                    UnderSent_Parts=str(df['UnderSent_Parts'][i]),
                    Threshold_result=str(df['Threshold_result'][i]),
                    ))
        else:
            objs.append(OSR(
                    OSRNumber=str(df['OSRNumber'][i]),
                    TV_Model= (str(df['TV_Model'][i])),
                    TV_SerialNo= (str(df['TV_SerialNo'][i])),
                    Work_Order=(str(df['Work_Order'][i])),
                    Import_Date= df['Import_Date'][i].strftime("%Y-%m-%d"),
                    ProblemDesc=str(df['ProblemDesc'][i]),
                    Train_Parts=str(df['Train_Parts'][i]),
                    Sent_Parts=str(df['Sent_Parts'][i]),
                    Predict_Train_Parts=str(df['Predict_Train_Parts'][i]),
                    Predict_Sent_Parts=str(df['Predict_Sent_Parts'][i]),
                    F2score=df['F2score'][i],
                    Similar_OSRNumber=str(df['Similar_OSRNumber'][i]),
                    OverSent_Parts=str(df['OverSent_Parts'][i]),
                    UnderSent_Parts=str(df['UnderSent_Parts'][i]),
                    Threshold_result=str(df['Threshold_result'][i]),
                    ))

except:
    print ('The file does not follow the naming convention. Process terminated.')

## Save back to DB
connections.close_all()
newlyCreatedFoos = OSR.objects.bulk_create(objs)

## Prepares the Message C.xlsx
# result_df = pd.DataFrame(_)
# result_for_excel_df = result_df[['Work Order #','OSR','TV MODEL','TV_SERIALNO',"SKU","POP Date",\
#     "ProblemDesc","Tech Name","Tech Address1", "Tech Address2", "Tech City", "Tech State", "Tech ZipCode", \
#     "Tech Phone", "Part Number-1", "Part Description-1", "Part Number-2", "Part Description-2", "Part Number-3" ,\
#     "Part Description-3", "Part Number-4", "Part Description-4", "Part Number-5", "Part Description-5", "Part Number-6", \
#     "Part Description-6", "Outbound Tracking", "Return Tracking", "Ship Date", "Note", "Predict_TrainParts"]]
# MessageC_filename = re.sub(r'\b\w{1}\b', 'C', target_filename) #INX OSR PART SHIPPED REPORT 01252021-2000.csv
# result_for_excel_df.to_excel(MessageC_filename, index=False)

# MessageC_filename = 'Test.xls'

# os.rename(str(cwd)+'/'+'INX OSR PART SHIPPED REPORT 12162020-2000.csv', MessageC_filename)

# ## Send the file back to FTP
# try:
#     ftp.connect(host, port)
# except:
#     logging.error('Connection failed.')
#     print ('Connection failed.')

# try:
#     ftp.login(usr, pwd)
# except:
#     logging.error('Logging failed.')
#     print ('Logging failed.')


# ftp.dir()
# ftp.cwd(target_dir)

# file = open(MessageC_filename,'rb')         # file to send
# ftp.storbinary('STOR' + MessageC_filename, file)     # send the file
# file.close()                                # close file and FTP
# ftp.quit()

# print('The Excel file has been successfully sent')





