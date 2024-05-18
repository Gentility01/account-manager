from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.forms import EmailField
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Accountant
from .models import Administrator
from .models import AffiliatePartner
from .models import ContentManager
from .models import CustomerSupportRepresentative
from .models import DigitalGoodsDistribution
from .models import HelpDeskTechnicalSupport
from .models import LiveChatSupport
from .models import MarketingAndSales
from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class CustomSignupBaseForm(SignupForm):
    """
    Base form for custom signup forms.
    """
    name = CharField(max_length=255, label="Name", required=True)
    phone_no = CharField(max_length=20, label="Phone number", required=False)
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form fields
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your username"},
        )
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your email"},
        )
        self.fields["phone_no"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your phone number"},
        )
        self.fields["country"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Select your country"},
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter your password"},
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm your password"},
        )


class UserSignupForm(CustomSignupBaseForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class CustomSignupForm(CustomSignupBaseForm):
    """
    Custom form for handling additional profile data during signup.
    """

    # Define user types as a class variable
    USER_TYPES = {
        "administrator": Administrator,
        "customer_support_representative": CustomerSupportRepresentative,
        "content_manager": ContentManager,
        "marketing_and_sales": MarketingAndSales,
        "accountant": Accountant,
        "help_desk_technical_support": HelpDeskTechnicalSupport,
        "live_chat_support": LiveChatSupport,
        "affiliate_partner": AffiliatePartner,
        "digital_goods_distribution": DigitalGoodsDistribution,
    }

    user_type = CharField(
        max_length=50,
        required=True,
    )  # Add a field to select user type

    department = CharField(max_length=100, required=False)
    expertise_area = CharField(max_length=255, required=False)
    marketing_strategy = CharField(widget=Textarea, required=False)
    financial_software_used = CharField(max_length=100, required=False)
    technical_skills = CharField(widget=Textarea, required=False)
    languages_spoken = CharField(max_length=100, required=False)
    affiliate_code = CharField(max_length=20, required=False)
    delivery_method = CharField(max_length=50, required=False)

    class InvalidUserTypeValidationError(ValidationError):
        message = "Invalid user type"

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")
        if user_type not in self.USER_TYPES:
            raise self.InvalidUserTypeValidationError
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        profile_data = self.cleaned_data

        profile_class = self.USER_TYPES.get(profile_data["user_type"])
        if profile_class:
            profile_class.objects.create(user=user, **profile_data)

        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when a user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
