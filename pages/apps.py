from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    
class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals  # Import signals to ensure they are loaded
