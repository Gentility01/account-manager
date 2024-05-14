from django.urls import path

from core.applications.users.views import accountant_account
from core.applications.users.views import administrator_account
from core.applications.users.views import content_manager_account
from core.applications.users.views import dashboard_view
from core.applications.users.views import user_detail_view
from core.applications.users.views import user_redirect_view
from core.applications.users.views import user_update_view

app_name = "users"
urlpatterns = [
    path(
        "signup/adminstrator-signup",
        view=administrator_account,
        name="administrator_account",
    ),
    path("dashboard", view=dashboard_view, name="dashboard_view"),
    path(
        "signup/content-manager",
        view=content_manager_account,
        name="content_manager_account",
    ),
    path("signup/accountant", view=accountant_account, name="accountant_account"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
]
