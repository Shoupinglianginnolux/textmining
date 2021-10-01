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

algorithm_url = '10.55.14.167:4548'

# s = requests.Session()
# s.mount('http://', HTTPAdapter(max_retries=3))
# s.mount('https://', HTTPAdapter(max_retries=3))

def run_ftp():
    print('Starting to grab the file.')
    ftp = FTP()
    try:
        ftp.connect(host, port)
    except:
        logging.error('Connection failed.')
        print ('Connection failed.')

    try:
        ftp.login(usr, pwd)
    except:
        logging.error('Logging failed.')
        print ('Logging failed.')


    ftp.dir()
    ftp.cwd(target_dir)

    MessageC_filename = 'Test.xls'


    def sendFile(filename):
        try:
            ftp.connect(host, port)
        except:
            logging.error('Connection failed.')
            print ('Connection failed.')

        try:
            ftp.login(usr, pwd)
        except:
            logging.error('Logging failed.')
            print ('Logging failed.')


        ftp.dir()
        ftp.cwd(target_dir)

        file = open(MessageC_filename,'rb')         # file to send
        ftp.storbinary(MessageC_filename, file)     # send the file
        file.close()                                # close file and FTP
        ftp.quit()

        print('The Excel file has been successfully sent')

    sendFile(MessageC_filename)




for i in _:
    if i['OSRNumber'] in existing_osr_nr_list:
        OSR.objects.filter(OSRNumber=str(i['OSRNumber'])).update(
                    Predict_Train_Parts = str(i['Predict_Train_Parts']),
                    Similar_OSRNumber = str(i['Similar_OSRNumber']),
                    Predict_Sent_Parts = str(i['Predict_Sent_Parts']),
                    Threshold_result = str(i['Threshold_result'])
                    )

for i in range(len(df['OSRNumber'])):
                        OSR.objects.filter(OSRNumber=str(df['OSRNumber'][i])) \
                            .update(Predict_Sent_Parts=str(df['Predict_Sent_Parts'][i]), \
                            Sent_Parts=str(df['Sent_Parts'][i]), Train_Parts=str(df['Train_Parts'][i]), F2score=str(df['F2score'][i]), \
                            OverSent_Parts=str(df['OverSent_Parts'][i]), UnderSent_Parts=str(df['UnderSent_Parts'][i]))