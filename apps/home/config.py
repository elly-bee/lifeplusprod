# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os
from django.apps import AppConfig
from django.db.models.signals import post_migrate


class MyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.home'
    label = 'apps_home'


    def ready(self):
        # This function will be called when Django starts
        from .updater import scheduled_function  # Import your custom scheduler module here.
        
        if os.environ.get('RUN_MAIN', None) != 'true':
            return
        
        # Start the scheduler when the application is ready
        scheduled_function.start()

def start_scheduler_handler(sender, **kwargs):
    from .updater import scheduled_function  # Import your custom scheduler module here.

    if os.environ.get('RUN_MAIN', None) == 'true':
        scheduled_function.start_scheduler()

post_migrate.connect(start_scheduler_handler)

    



