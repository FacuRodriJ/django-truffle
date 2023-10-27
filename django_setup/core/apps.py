from django.apps import AppConfig
from django.db import OperationalError


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # Crear un superusuario al ejecutar el servidor
    def ready(self):
        from django.contrib.auth.models import User
        try:
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser('admin', 'admin@localhost', 'admin')
        except OperationalError:
            pass

