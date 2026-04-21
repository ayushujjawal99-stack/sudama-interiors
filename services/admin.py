from django.contrib import admin
from .models import Service, ServiceCategory, ServiceImage, ServiceSection


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "slug")
    list_filter = ("category",)
    search_fields = ("name", "slug", "short_description", "meta_title")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ServiceSection)
class ServiceSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "service", "order")
    list_filter = ("service__category", "service")
    search_fields = ("title", "content", "service__name")
    ordering = ("service__name", "order")


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ("service", "alt_text")
    list_filter = ("service__category", "service")
    search_fields = ("alt_text", "service__name")
