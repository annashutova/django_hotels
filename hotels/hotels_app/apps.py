from django.apps import AppConfig


class HotelsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotels_app'

    def ready(self):
        import hotels_app.signals
