from django.apps import AppConfig

class PersistenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'litethinking.infrastructure.persistence'
    label = 'persistence'
    verbose_name = 'Persistencia'
    
    def ready(self):
        import litethinking.infrastructure.persistence.admin

