from django.contrib import admin
from django.utils.html import format_html

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("preview", "title", "slug", "created_at")
    list_display_links = ("preview", "title")
    readonly_fields = ("image_preview", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "slug", "short_description", "description")
    ordering = ("title",)
    fieldsets = (
        ("Studio Service", {"fields": ("title", "slug", "short_description", "description")}),
        ("Cinematic Image", {"fields": ("image", "image_preview")}),
        ("System", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    @admin.display(description="Image")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:76px;height:52px;object-fit:cover;border-radius:8px;" />',
                obj.image.url,
            )
        return "No image"

    @admin.display(description="Current preview")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:420px;border-radius:14px;box-shadow:0 18px 50px rgba(0,0,0,.22);" />',
                obj.image.url,
            )
        return "Upload a service image to see the preview."
