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
    branch = forms.ModelChoiceField(label="Sucursal de origen", queryset=None)
    delivery_type = forms.ChoiceField(label="Entrega", choices=Order.DELIVERY_CHOICES)
    billing_address = forms.CharField(label="Dirección de facturación", max_length=240, required=False)
    distance_km = forms.IntegerField(label="Distancia en kilómetros", min_value=0, max_value=1000, required=False)
    payment_method = forms.ChoiceField(label="Medio de pago", choices=Order.PAYMENT_CHOICES)

    def __init__(self, *args, **kwargs):
        from .models import Branch

        super().__init__(*args, **kwargs)
        self.fields["branch"].queryset = Branch.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("delivery_type") == "delivery":
            if not cleaned_data.get("billing_address"):
                self.add_error("billing_address", "La dirección de facturación es obligatoria para despacho.")
            if cleaned_data.get("distance_km") is None:
                self.add_error("distance_km", "Indica la distancia desde la sucursal para calcular el envío.")
        return cleaned_data
