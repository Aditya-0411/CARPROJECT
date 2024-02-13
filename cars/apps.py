from django.apps import AppConfig


class CarsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cars"

class MessagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messages"
