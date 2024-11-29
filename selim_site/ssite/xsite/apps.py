from django.apps import AppConfig


class XsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xsite'

class YourAppNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xsite'

    def ready(self):
        import xsite.signals




