from requests import request
import schedule
import time
from .jobs import schedule_api
from .mailfetch import case_email11_add
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run scheduled tasks'
    def handle(self, *args, **options):
        def scheduled_function():
            # Call the management command or function you want to run
            schedule_api()
            case_email11_add(request)

        # Schedule the function to run every 60 seconds
        schedule.every(5).seconds.do(scheduled_function)

        while True:
            schedule.run_pending()
            time.sleep(1)