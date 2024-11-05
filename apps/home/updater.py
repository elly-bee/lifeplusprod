import schedule
import time
from jobs import schedule_api, case_mail_add

def scheduled_function():
    # Call the management command or function you want to run
    schedule_api()
    case_mail_add()

# Schedule the function to run every 60 seconds
schedule.every(15).seconds.do(scheduled_function)

while True:
    schedule.run_pending()
    time.sleep(1)