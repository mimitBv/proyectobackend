from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("music_pro", "0011_swap_product_image_paths")]
    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("received", "Nueva compra"),
                    ("preparing", "En preparación"),
                    ("dispatched", "Despachado"),
                    ("completed", "Completado"),
                ],
                default="received",
                max_length=20,
                verbose_name="estado",
            ),
        ),
    ]
