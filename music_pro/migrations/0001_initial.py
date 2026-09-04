from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="FranchiseInquiry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="nombre")),
                ("city", models.CharField(max_length=120, verbose_name="ciudad")),
                ("email", models.EmailField(max_length=254, verbose_name="correo")),
                ("message", models.TextField(verbose_name="mensaje")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="recibido")),
            ],
            options={
                "verbose_name": "solicitud de franquicia",
                "verbose_name_plural": "solicitudes de franquicia",
                "ordering": ["-created_at"],
            },
        ),
    ]
