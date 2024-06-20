from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .models import Account, User


@receiver(user_logged_in, sender=User)
def create_account_login(sender, user, request, **kwargs):
    user_types = [
        "administrator",
        "customer_support_representative",
        "content_manager",
        "marketing_and_sales",
        "accountant",
        "help_desk_technical_support",
        "live_chat_support",
        "affiliate_partner",
        "digital_goods_distribution",
    ]

    for user_type in user_types:
        if hasattr(user, user_type) and not hasattr(
            getattr(user, user_type),
            "account",
        ):
            Account.objects.create(owner=user)
            break
