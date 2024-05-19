from django.apps import AppConfig


class FrontConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.front' #detalle importante, si metemos las app en una carpeta, le hemos de añadir el 'app.' al name
