from django.urls import path

from core.applications.supports.views import CreateFAQ
from core.applications.supports.views import DeleteFAQViews
from core.applications.supports.views import EditFAQViews
from core.applications.supports.views import FAQListView
from core.applications.supports.views import HELPOrFAQPage
from core.applications.supports.views import TicketDetailView
from core.applications.supports.views import TicketListView

app_name = "support"
urlpatterns = [
    path("tickets", TicketListView.as_view(), name="ticket_list"),
    path("<int:pk>/", TicketDetailView.as_view(), name="ticket_detail"),
    path("create-faq", CreateFAQ.as_view(), name="create_faq"),
    path("edit-faq/<int:pk>/", EditFAQViews.as_view(), name="edit_faq"),
    path("delete-faq/<int:pk>/", DeleteFAQViews.as_view(), name="delete_faq"),
    path("faq-list", FAQListView.as_view(), name="faq_list"),
    path("help", HELPOrFAQPage.as_view(), name="helppage"),
]
