from django.apps import AppConfig


class InventoryAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory_app'
    verbose_name = "Inventory App"

    def ready(self):
        import inventory_app.signals
