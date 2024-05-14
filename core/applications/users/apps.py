# core/applications/users/apps.py

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.applications.users"

    def ready(self):
        # Import signals here
        from django.contrib.auth.signals import user_logged_in
        from django.dispatch import receiver

        from .models import User

        @receiver(user_logged_in, sender=User)
        def create_account_on_login(sender, user, request, **kwargs):
            # Your signal handler code here
            pass
