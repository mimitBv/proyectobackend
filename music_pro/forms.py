from django import forms

from .models import FranchiseInquiry


class FranchiseInquiryForm(forms.ModelForm):
    class Meta:
        model = FranchiseInquiry
        fields = ["name", "city", "email", "message"]
        input_class = "w-full rounded-lg border border-outline-variant bg-surface-container-low px-3 py-2.5 text-on-surface placeholder:text-on-surface-variant focus:border-primary focus:outline-none"
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Tu nombre", "class": input_class}),
            "city": forms.TextInput(attrs={"placeholder": "Tu ciudad", "class": input_class}),
            "email": forms.EmailInput(attrs={"placeholder": "correo@ejemplo.com", "class": input_class}),
            "message": forms.Textarea(attrs={"placeholder": "Cuéntanos qué quieres abrir...", "rows": 4, "class": input_class}),
        }
