import os
import schedule
import time

def repeat():
    os.system("python Operation.py")

schedule.every(24).hours.do(repeat)

repeat()
while(1):
    schedule.run_pending()
    time.sleep(60)

