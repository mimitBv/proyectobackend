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
