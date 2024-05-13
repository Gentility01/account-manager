from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import User, Account

@receiver(user_logged_in, sender=User)
def create_account_on_login(sender, user, request, **kwargs):
    # Check the type of user and create an Account instance if it doesn't exist
    if hasattr(user, 'administrator'):
        if not hasattr(user.administrator, 'account'):
            Account.objects.create(owner=user)
    elif hasattr(user, 'customer_support_representative'):
        if not hasattr(user.customer_support_representative, 'account'):
            Account.objects.create(owner=user)
    elif hasattr(user, 'content_manager'):
        if not hasattr(user.content_manager, 'account'):
            Account.objects.create(owner=user)
    elif hasattr(user, 'marketing_and_sales'):
        if not hasattr(user.marketing_and_sales, 'account'):
            Account.objects.create(owner=user)
    elif hasattr(user, 'accountant'):
        if not hasattr(user.accountant, 'account'):
            Account.objects.create(owner=user)
    elif hasattr(user, 'help_desk_technical_support'):
        if not hasattr(user.help_desk_technical_support, 'account'):
            Account.objects.create(owner=user)
    elif hasattr(user, 'live_chat_support'):
        if not hasattr(user.live_chat_support, 'account'):
            Account.objects.create(owner=user)
    elif hasattr(user, 'affiliate_partner'):
        if not hasattr(user.affiliate_partner, 'account'):
            Account.objects.create(owner=user)
    elif hasattr(user, 'digital_goods_distribution'):
        if not hasattr(user.digital_goods_distribution, 'account'):
            Account.objects.create(owner=user)

    # Add similar checks for other user types (e.g., ContentManager, MarketingAndSales, etc.)
