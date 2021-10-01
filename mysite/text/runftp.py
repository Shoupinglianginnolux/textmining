from text import ftp
import logging

def run_ftp():
    try:
        print('The ftp has ended correctly.')
        return('I don\'t know....')

    except:
        print('An error occured.')

logging.basicConfig(filename='run_ftp.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
logging.debug('Starting to grab the file.')

ans = run_ftp()
print(ans)