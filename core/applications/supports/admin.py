from django.contrib import admin

from core.applications.supports.models import Response
from core.applications.supports.models import Ticket

# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "customer", "assigned_to", "status", "created_at")


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("ticket", "user", "messages")
