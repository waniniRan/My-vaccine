from django.apps import AppConfig


class SysadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Sysadmin'

def ready(self):
    #import signals 
    pass