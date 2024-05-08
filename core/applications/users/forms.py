from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField, CharField, Textarea
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import (
    User,
    Administrator,
    CustomerSupportRepresentative,
    ContentManager,
    MarketingAndSales,
    Accountant,
    HelpDeskTechnicalSupport,
    LiveChatSupport,
    AffiliatePartner,
    DigitalGoodsDistribution,
)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize form fields
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your email"})
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Enter your password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirm your password"})


class UserSignupForm(CustomSignupBaseForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    pass


class CustomSignupForm(CustomSignupBaseForm):
    """
    Custom form for handling additional profile data during signup.
    """

    user_type = CharField(max_length=50, required=True)  # Add a field to select user type

    department = CharField(max_length=100, required=False)
    expertise_area = CharField(max_length=255, required=False)
    marketing_strategy = CharField(widget=Textarea, required=False)
    financial_software_used = CharField(max_length=100, required=False)
    technical_skills = CharField(widget=Textarea, required=False)
    languages_spoken = CharField(max_length=100, required=False)
    affiliate_code = CharField(max_length=20, required=False)
    delivery_method = CharField(max_length=50, required=False)

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get("user_type")
        if user_type not in ["administrator", "customer_support_representative", "content_manager", "accountant", ...]:
            raise ValidationError("Invalid user type")
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        profile_data = self.cleaned_data

        # Create profile instance based on user's role
        if profile_data["user_type"] == "administrator":
            Administrator.objects.create(user=user, department=profile_data.get("department"))
        elif profile_data["user_type"] == "customer_support_representative":
            CustomerSupportRepresentative.objects.create(user=user, department=profile_data.get("department"))
        elif profile_data["user_type"] == "content_manager":
            ContentManager.objects.create(user=user, expertise_area=profile_data.get("expertise_area"))
        elif profile_data["user_type"] == "marketing_and_sales":
            MarketingAndSales.objects.create(user=user, marketing_strategy=profile_data.get("marketing_strategy"))
        elif profile_data["user_type"] == "accountant":
            Accountant.objects.create(user=user, financial_software_used=profile_data.get("financial_software_used"))
        elif profile_data["user_type"] == "help_desk_technical_support":
            HelpDeskTechnicalSupport.objects.create(user=user, technical_skills=profile_data.get("technical_skills"))
        elif profile_data["user_type"] == "live_chat_support":
            LiveChatSupport.objects.create(user=user, languages_spoken=profile_data.get("languages_spoken"))
        elif profile_data["user_type"] == "affiliate_partner":
            AffiliatePartner.objects.create(user=user, affiliate_code=profile_data.get("affiliate_code"))
        elif profile_data["user_type"] == "digital_goods_distribution":
            DigitalGoodsDistribution.objects.create(user=user, delivery_method=profile_data.get("delivery_method"))

        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when a user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
