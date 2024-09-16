# pack/apps.py

from django.apps import AppConfig

class PackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pack'

    def ready(self):
        import pack.signals  # Ensure the signals are loaded
