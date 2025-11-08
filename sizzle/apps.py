from django.apps import AppConfig


class SizzleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sizzle'
    verbose_name = 'Sizzle Daily Check-in'
    
    def ready(self):
        import sizzle.signals