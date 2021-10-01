import datetime
from time import sleep

import sys
import os

PACKAGE_PARENT = '...'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from mysite.manage import manage

rest_seconds = 60  # sleep for one hour, so the task won't be called few times per hour
while True:
    if datetime.datetime.now().minute == 8:
        manage()
    sleep(rest_seconds)