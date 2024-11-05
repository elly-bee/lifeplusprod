import schedule
import time

def task():
    print('everything')

schedule.every(5).seconds.do(task)

while True:
    schedule.run_pending()
    time.sleep(1)