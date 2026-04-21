from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import ContactLeadForm
from .site_content import (
    fallback_product_cards,
    fallback_service_cards,
    product_groups_from_queryset,
    service_groups_from_queryset,
)
from services.models import ServiceCategory
from products.models import ProductCategory


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        service_categories = (
            ServiceCategory.objects
            .prefetch_related("services")
            .order_by("name")
        )
        product_categories = (
            ProductCategory.objects
            .prefetch_related("products")
            .order_by("name")
        )

        service_groups = service_groups_from_queryset(service_categories)
        product_groups = product_groups_from_queryset(product_categories)

        ctx["service_groups"] = service_groups or fallback_service_cards()
        ctx["product_groups"] = product_groups or fallback_product_cards()
        return ctx


def contact(request):
    if request.method == "POST":
        form = ContactLeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Thank you. Your enquiry has been received and our team will contact you shortly.",
            )
            return redirect("contact")
    else:
        form = ContactLeadForm()

    service_groups = service_groups_from_queryset(
        ServiceCategory.objects.prefetch_related("services").order_by("name")
    )
    product_groups = product_groups_from_queryset(
        ProductCategory.objects.prefetch_related("products").order_by("name")
    )

    context = {
        "form": form,
        "service_groups": service_groups or fallback_service_cards(),
        "product_groups": product_groups or fallback_product_cards(),
    }

    return render(request, "contact.html", context)
