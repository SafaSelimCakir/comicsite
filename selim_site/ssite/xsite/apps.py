from django.apps import AppConfig


class xsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xsite'

    def ready(self):
        import xsite.signals

