from django.apps import AppConfig

# No arquivo apps.py do seu aplicativo
from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import main.signals  # Certifique-se de que os sinais sejam importados
