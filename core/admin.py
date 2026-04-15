from django.contrib import admin
from .models import ContactLead


@admin.register(ContactLead)
class ContactLeadAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "category", "subcategory", "created_at")
    list_filter = ("category", "subcategory", "created_at")
    search_fields = ("name", "phone", "email", "message")
