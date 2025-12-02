from django.apps import AppConfig


class RecordsConfig(AppConfig):
    """Конфигурация приложения учёта ЭЭГ."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "records"
    verbose_name = "Учёт ЭЭГ"
