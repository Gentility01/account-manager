from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import (
    Administrator, CustomerSupportRepresentative, User,
    ContentManager, MarketingAndSales,
    Accountant, HelpDeskTechnicalSupport, 
    LiveChatSupport, AffiliatePartner, DigitalGoodsDistribution, Account
)

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.site.login = login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser", "pk"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )



@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ['user', 'department']

@admin.register(CustomerSupportRepresentative)
class CustomerSupportRepresentativeAdmin(admin.ModelAdmin):
    list_display = ['user', 'department']

@admin.register(ContentManager)
class ContentManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'expertise_area']

@admin.register(MarketingAndSales)
class MarketingAndSalesAdmin(admin.ModelAdmin):
    list_display = ['user', 'marketing_strategy']

@admin.register(Accountant)
class AccountantAdmin(admin.ModelAdmin):
    list_display = ['user', 'financial_software_used']

@admin.register(HelpDeskTechnicalSupport)
class HelpDeskTechnicalSupportAdmin(admin.ModelAdmin):
    list_display = ['user', 'technical_skills']

@admin.register(LiveChatSupport)
class LiveChatSupportAdmin(admin.ModelAdmin):
    list_display = ['user', 'languages_spoken']

@admin.register(AffiliatePartner)
class AffiliatePartnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'affiliate_code']

@admin.register(DigitalGoodsDistribution)
class DigitalGoodsDistributionAdmin(admin.ModelAdmin):
    list_display = ['user', 'delivery_method']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['owner']
