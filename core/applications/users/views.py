from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.views.generic import (
    UpdateView, TemplateView, RedirectView, DetailView
)
from allauth.account.views import SignupView
from core.applications.users.forms import CustomSignupForm
from core.applications.users.models import Account
from django.http import HttpResponseRedirect
from allauth.account.utils import send_email_confirmation
from core.applications.users.models import (
    User, Administrator, ContentManager, MarketingAndSales, CustomerSupportRepresentative,
    Accountant, HelpDeskTechnicalSupport, LiveChatSupport, AffiliatePartner, DigitalGoodsDistribution
)



class CustomSignupView(SignupView):
    form_class = CustomSignupForm
custom_signup_views = CustomSignupView.as_view()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        # return reverse("users:detail", kwargs={"pk": self.request.user.pk})
        return reverse("homeapp:home")

user_redirect_view = UserRedirectView.as_view()


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context
dashboard_view = DashboardView.as_view()


class ContentManagerAccount(SignupView):
    form_class = CustomSignupForm
    template_name = "account/content_manager.html"

    def form_valid(self, form):
        user = form.save(self.request)  # Use form.save() to get the user instance
        expertise_area = form.cleaned_data.get("expertise_area")
        
        # Get or create the associated account for the user
        account, created = Account.objects.get_or_create(owner=user)

        # Create the ContentManager instance with the associated account
        ContentManager.objects.create(user=user, account=account, expertise_area=expertise_area)

        # Send email confirmation
        send_email_confirmation(self.request, user)

        return HttpResponseRedirect("/accounts/confirm-email/")  # Redirect after successful signup

content_manager_account = ContentManagerAccount.as_view()


class AccountantAccount(SignupView):
    form_class = CustomSignupForm
    template_name = "account/accountant_signup.html"

    def form_valid(self, form):
        user = form.save(self.request)  # Use form.save() to get the user instance
        financial_software_used = form.cleaned_data.get("financial_software_used")
        
        # Get or create the associated account for the user
        account, created = Account.objects.get_or_create(owner=user)

        # Create the Accountant instance with the associated account
        Accountant.objects.create(user=user, account=account, financial_software_used=financial_software_used)

        # Send email confirmation
        send_email_confirmation(self.request, user)

        return HttpResponseRedirect("/accounts/confirm-email/")  # Redirect after successful signup

accountant_account = AccountantAccount.as_view()


class AdministratorAccount(SignupView):
    form_class = CustomSignupForm
    template_name = "account/administrator.html"

    def form_valid(self, form):
        user = form.save(self.request)  # Use form.save() to get the user instance
        department = form.cleaned_data.get("department")
        
        # Get or create the associated account for the user
        account, created = Account.objects.get_or_create(owner=user)

        # Create the Administrator instance with the associated account
        Administrator.objects.create(user=user, account=account, department=department)

        # Send email confirmation
        send_email_confirmation(self.request, user)

        return HttpResponseRedirect("/accounts/confirm-email/")  # Redirect after successful signup

administrator_account = AdministratorAccount.as_view()


