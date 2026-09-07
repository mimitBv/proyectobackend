import re

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=120)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


class FranchiseInquiryForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=120)
    city = forms.CharField(label="Ciudad", max_length=120)
    email = forms.EmailField(label="Correo")
    message = forms.CharField(label="Mensaje", widget=forms.Textarea(attrs={"rows": 4}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_class = "w-full rounded-lg border border-outline-variant bg-surface-container-low px-3 py-2.5 text-on-surface placeholder:text-on-surface-variant focus:border-primary focus:outline-none"
        for field_name in ["name", "city", "email", "message"]:
            self.fields[field_name].widget.attrs["class"] = input_class


class RegisterForm(forms.Form):
    first_name = forms.CharField(label="Nombre", max_length=120)
    last_name = forms.CharField(label="Apellido", max_length=120)
    email = forms.EmailField(label="Correo")
    username = forms.CharField(label="Nombre de usuario", max_length=120)
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        return cleaned_data


class CheckoutForm(forms.Form):
    BRANCH_CHOICES = [
        ("santiago-centro", "Santiago Centro"),
        ("providencia", "Providencia"),
        ("valparaiso", "Valparaíso"),
    ]
    DELIVERY_CHOICES = [("pickup", "Retiro en sucursal"), ("delivery", "Despacho a domicilio")]
    PAYMENT_CHOICES = [("debit", "Tarjeta de débito"), ("credit", "Tarjeta de crédito"), ("transfer", "Transferencia bancaria")]

    first_name = forms.CharField(label="Nombre", max_length=120)
    last_name = forms.CharField(label="Apellido", max_length=120)
    rut = forms.CharField(
        label="RUT",
        max_length=10,
        required=False,
        help_text="Usa solo dígitos y un guion. Ejemplo: 12345678-9",
        widget=forms.TextInput(
            attrs={
                "inputmode": "numeric",
                "pattern": r"[0-9]{7,8}-[0-9]",
                "placeholder": "12345678-9",
            }
        ),
    )
    branch = forms.ChoiceField(label="Sucursal de origen", choices=BRANCH_CHOICES)
    delivery_type = forms.ChoiceField(label="Entrega", choices=DELIVERY_CHOICES)
    region = forms.CharField(label="Región", max_length=120, required=False)
    commune = forms.CharField(label="Comuna", max_length=120, required=False)
    billing_address = forms.CharField(label="Dirección de facturación", max_length=240, required=False)
    property_type = forms.ChoiceField(label="Casa o departamento", choices=[("house", "Casa"), ("apartment", "Departamento")], required=False)
    delivery_comment = forms.CharField(label="Comentario para el repartidor (opcional)", max_length=500, required=False, widget=forms.Textarea(attrs={"rows": 3}))
    payment_method = forms.ChoiceField(label="Medio de pago", choices=PAYMENT_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_class = "field"
        select_class = "field"
        for field_name in ["first_name", "last_name", "rut", "region", "commune", "billing_address"]:
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
            rut = cleaned_data.get("rut", "")
            if rut and not re.fullmatch(r"\d{7,8}-\d", rut):
                self.add_error("rut", "Ingresa solo dígitos y un guion, por ejemplo 12345678-9.")
        return cleaned_data
