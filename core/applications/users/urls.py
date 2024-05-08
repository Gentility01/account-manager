from django.urls import path

from core.applications.users.views import user_detail_view, user_redirect_view, user_update_view, custom_signup_views


app_name = "users"
urlpatterns = [
    path("accounts/signup/custom", view=custom_signup_views, name="custom_signup"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
]
