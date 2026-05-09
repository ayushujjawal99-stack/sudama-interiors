from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from services.models import Service


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        services = Service.objects.order_by("title")
        context["services"] = services
        context["featured_services"] = services[:4]
        return context


class AboutView(TemplateView):
    template_name = "about.html"


def contact(request):
    if request.method == "POST":
        messages.success(
            request,
            "Your consultation request has been received. Our studio will connect with you shortly.",
        )
        return redirect("contact")

    return render(request, "contact.html", {"services": Service.objects.order_by("title")})
