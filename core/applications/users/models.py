from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, CASCADE
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from .managers import UserManager
from core.utils.models import UIDTimeBasedModel
import auto_prefetch

class User(UIDTimeBasedModel, AbstractUser):
    """
    Default custom user model for Acctmarket.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore
    phone_no = CharField(_("Phone number"), max_length=20, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Account(UIDTimeBasedModel):
    owner = auto_prefetch.ForeignKey(
        User, related_name="owned_accounts", on_delete=models.CASCADE, verbose_name=_("Account Owner")
    )

    class Meta(UIDTimeBasedModel.Meta):
        verbose_name_plural = "Accounts"


class BaseProfile(UIDTimeBasedModel):
    """
    Base class for different types of profiles associated with users.
    """
    user = auto_prefetch.ForeignKey(
        User, on_delete=models.CASCADE, related_name="%(class)s_profiles", verbose_name=_("User")
    )
    account = auto_prefetch.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name=_("Account"), related_name="%(class)s_profiles"
    )

    class Meta(UIDTimeBasedModel.Meta):
        abstract = True


class Administrator(BaseProfile):
    """
    Represents an administrator associated with an account.
    """
    department = models.CharField(_("Department"), max_length=100)

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Administrators"


class CustomerSupportRepresentative(BaseProfile):
    """
    Represents a customer support representative associated with an account.
    """
    department = models.CharField(_("Department"), max_length=100)

   

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Customer Support Representatives"


class ContentManager(BaseProfile):
    """
    Represents a content manager associated with an account.
    """
    expertise_area = models.CharField(_("Expertise Area"), max_length=255)

   

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Content Managers"


class MarketingAndSales(BaseProfile):
    """
    Represents a marketing and sales personnel associated with an account.
    """
    marketing_strategy = models.TextField(_("Marketing Strategy"))

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Marketing and Sales"


class Accountant(BaseProfile):
    """
    Represents an accountant associated with an account.
    """
    financial_software_used = models.CharField(_("Financial Software Used"), max_length=100)

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Accountants"


class HelpDeskTechnicalSupport(BaseProfile):
    """
    Represents a technical support personnel associated with an account.
    """
    technical_skills = models.TextField(_("Technical Skills"))

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Help Desk Technical Supports"


class LiveChatSupport(BaseProfile):
    """
    Represents a live chat support personnel associated with an account.
    """
    languages_spoken = models.CharField(_("Languages Spoken"), max_length=100)

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Live Chat Supports"


class AffiliatePartner(BaseProfile):
    """
    Represents an affiliate partner associated with an account.
    """
    affiliate_code = models.CharField(_("Affiliate Code"), max_length=20)

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Affiliate Partners"


class DigitalGoodsDistribution(BaseProfile):
    """
    Represents digital goods distribution associated with an account.
    """
    delivery_method = models.CharField(_("Delivery Method"), max_length=50)

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Digital Goods Distributions"