from django.apps import AppConfig


class FinanceAndAccountingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Finance_and_Accounting'
    def ready(self):
        import Finance_and_Accounting.signals


