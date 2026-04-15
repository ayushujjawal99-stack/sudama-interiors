from django import forms

from .models import ContactLead
from services.models import Service, ServiceCategory


class ContactLeadForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=ServiceCategory.objects.order_by("name"),
        empty_label="Select category",
        required=True,
    )
    subcategory = forms.ModelChoiceField(
        queryset=Service.objects.none(),
        empty_label="Select subcategory",
        required=True,
    )

    class Meta:
        model = ContactLead
        fields = ("name", "phone", "email", "category", "subcategory", "message")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["subcategory"].queryset = Service.objects.none()

        category_id = self.data.get("category") or self.initial.get("category")
        if category_id:
            try:
                self.fields["subcategory"].queryset = Service.objects.filter(
                    category_id=int(category_id)
                ).order_by("name")
            except (TypeError, ValueError):
                self.fields["subcategory"].queryset = Service.objects.none()
        elif self.instance.pk and self.instance.category_id:
            self.fields["subcategory"].queryset = Service.objects.filter(
                category=self.instance.category
            ).order_by("name")

    def clean_name(self):
        value = (self.cleaned_data.get("name") or "").strip()
        if not value:
            raise forms.ValidationError("Full name is required.")
        return value

    def clean_phone(self):
        value = (self.cleaned_data.get("phone") or "").strip()
        if not value:
            raise forms.ValidationError("Phone number is required.")
        return value

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        subcategory = cleaned_data.get("subcategory")

        if category is None:
            self.add_error("category", "Please select a category.")
        if subcategory is None:
            self.add_error("subcategory", "Please select a subcategory.")
        elif category and subcategory.category_id != category.id:
            self.add_error("subcategory", "Selected subcategory does not match the category.")

        return cleaned_data
