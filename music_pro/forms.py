import re

from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import FranchiseInquiry, Order


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


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Nombre", max_length=120)
    last_name = forms.CharField(label="Apellido", max_length=120)
    email = forms.EmailField(label="Correo")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1", "password2"]


class CheckoutForm(forms.Form):
    first_name = forms.CharField(label="Nombre", max_length=120)
    last_name = forms.CharField(label="Apellido", max_length=120)
    rut = forms.CharField(label="RUT", max_length=12, required=False, help_text="Ejemplo: 12.345.678-9")
    branch = forms.ModelChoiceField(label="Sucursal de origen", queryset=None)
    delivery_type = forms.ChoiceField(label="Entrega", choices=Order.DELIVERY_CHOICES)
    region = forms.CharField(label="Región", max_length=120, required=False)
    commune = forms.CharField(label="Comuna", max_length=120, required=False)
    billing_address = forms.CharField(label="Dirección de facturación", max_length=240, required=False)
    property_type = forms.ChoiceField(label="Casa o departamento", choices=[("house", "Casa"), ("apartment", "Departamento")], required=False)
    delivery_comment = forms.CharField(label="Comentario para el repartidor (opcional)", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 3}))
    distance_km = forms.IntegerField(label="Distancia en kilómetros", min_value=0, max_value=1000, required=False)
    payment_method = forms.ChoiceField(label="Medio de pago", choices=Order.PAYMENT_CHOICES)

    def __init__(self, *args, **kwargs):
        from .models import Branch

        super().__init__(*args, **kwargs)
        self.fields["branch"].queryset = Branch.objects.all()
        text_class = "field"
        select_class = "field"
        for field_name in ["first_name", "last_name", "rut", "region", "commune", "billing_address", "distance_km"]:
            self.fields[field_name].widget.attrs["class"] = text_class
        for field_name in ["branch", "delivery_type", "property_type", "payment_method"]:
            self.fields[field_name].widget.attrs["class"] = select_class
        self.fields["delivery_comment"].widget.attrs["class"] = text_class

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("delivery_type") == "delivery":
            required_delivery_fields = {
                "rut": "El RUT es obligatorio para despacho.",
                "region": "La región es obligatoria para despacho.",
                "commune": "La comuna es obligatoria para despacho.",
                "billing_address": "La dirección es obligatoria para despacho.",
                "property_type": "Indica si es casa o departamento.",
            }
            for field_name, error in required_delivery_fields.items():
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, error)
            rut = cleaned_data.get("rut", "").replace(".", "").replace("-", "").upper()
            if rut and not re.fullmatch(r"\d{7,8}[0-9K]", rut):
                self.add_error("rut", "Ingresa un RUT válido, por ejemplo 12.345.678-9.")
            if cleaned_data.get("distance_km") is None:
                self.add_error("distance_km", "Indica la distancia desde la sucursal para calcular el envío.")
        return cleaned_data
