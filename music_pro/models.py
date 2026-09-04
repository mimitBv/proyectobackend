from django.db import models


class FranchiseInquiry(models.Model):
    name = models.CharField("nombre", max_length=120)
    city = models.CharField("ciudad", max_length=120)
    email = models.EmailField("correo")
    message = models.TextField("mensaje")
    created_at = models.DateTimeField("recibido", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "solicitud de franquicia"
        verbose_name_plural = "solicitudes de franquicia"

    def __str__(self):
        return f"{self.name} - {self.city}"


class Branch(models.Model):
    name = models.CharField("nombre", max_length=120)
    city = models.CharField("ciudad", max_length=120)
    address = models.CharField("dirección", max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        ordering = ["city"]
        verbose_name = "sucursal"
        verbose_name_plural = "sucursales"

    def __str__(self):
        return f"{self.name} - {self.city}"


class Product(models.Model):
    name = models.CharField("nombre", max_length=160)
    category = models.CharField("categoría", max_length=80)
    description = models.TextField("descripción")
    price = models.PositiveIntegerField("precio")
    stock = models.PositiveIntegerField("stock", default=0)
    icon = models.CharField("ícono", max_length=40, default="music_note")
    image = models.CharField("imagen", max_length=120, default="images/products/instrumentos.svg")
    active = models.BooleanField("activo", default=True)

    class Meta:
        ordering = ["category", "name"]
        verbose_name = "producto"
        verbose_name_plural = "productos"

    def __str__(self):
        return self.name


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("debit", "Tarjeta de débito"),
        ("credit", "Tarjeta de crédito"),
        ("transfer", "Transferencia bancaria"),
    ]
    DELIVERY_CHOICES = [("pickup", "Retiro en sucursal"), ("delivery", "Despacho a domicilio")]

    user = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="orders")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, verbose_name="sucursal")
    first_name = models.CharField("nombre", max_length=120)
    last_name = models.CharField("apellido", max_length=120)
    rut = models.CharField("RUT", max_length=12, blank=True)
    region = models.CharField("región", max_length=120, blank=True)
    commune = models.CharField("comuna", max_length=120, blank=True)
    billing_address = models.CharField("dirección de facturación", max_length=240, blank=True)
    property_type = models.CharField("tipo de vivienda", max_length=20, blank=True)
    delivery_comment = models.TextField("comentario para el repartidor", blank=True)
    delivery_type = models.CharField("modalidad", max_length=20, choices=DELIVERY_CHOICES)
    distance_km = models.PositiveIntegerField("distancia en km", default=0)
    shipping_cost = models.PositiveIntegerField("costo de envío", default=0)
    payment_method = models.CharField("medio de pago", max_length=20, choices=PAYMENT_CHOICES)
    total = models.PositiveIntegerField("total")
    created_at = models.DateTimeField("creado", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "pedido"
        verbose_name_plural = "pedidos"

    def __str__(self):
        return f"Pedido #{self.pk} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("cantidad")
    unit_price = models.PositiveIntegerField("precio unitario")
