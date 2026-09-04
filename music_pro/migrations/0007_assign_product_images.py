from django.db import migrations, models


def assign_images(apps, schema_editor):
    Product = apps.get_model("music_pro", "Product")
    category_images = {
        "Instrumentos": "images/products/instrumentos.svg",
        "Teclados": "images/products/teclados.svg",
        "Baterias": "images/products/baterias.svg",
        "Amplificacion": "images/products/amplificacion.svg",
        "Pedales": "images/products/pedales.svg",
        "Audio profesional": "images/products/audio.svg",
        "Monitoreo": "images/products/audio.svg",
        "Micrófonos": "images/products/microfonos.svg",
        "Accesorios": "images/products/accesorios.svg",
    }
    for category, image in category_images.items():
        Product.objects.filter(category=category).update(image=image)


class Migration(migrations.Migration):
    dependencies = [("music_pro", "0006_add_more_products")]
    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.CharField(default="images/products/instrumentos.svg", max_length=120, verbose_name="imagen"),
        ),
        migrations.RunPython(assign_images, migrations.RunPython.noop),
    ]