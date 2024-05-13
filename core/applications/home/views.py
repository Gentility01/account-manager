from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect



# Create your views here.

class HomeView(TemplateView):
    template_name = "pages/home.html"



class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = reverse_lazy('login')  # Assuming 'login' is the name of the login URL pattern

    def dispatch(self, request, *args, **kwargs):
        if not request.user.administrator_profile.exists():
            # If the user is not an administrator, redirect them to another page
            return redirect(reverse_lazy('not_administrator'))  # Assuming 'not_administrator' is the name of the URL pattern for the page
        return super().dispatch(request, *args, **kwargs)