from django.db import migrations


def seed_catalog(apps, schema_editor):
    Branch = apps.get_model("music_pro", "Branch")
    Product = apps.get_model("music_pro", "Product")
    branches = [
        ("Santiago Centro", "Santiago", "Av. Libertador Bernardo O'Higgins 1400", -33.4489, -70.6693),
        ("Vina del Mar", "Vina del Mar", "Mall Marina / Paseo de la Playa", -33.0153, -71.5500),
        ("Concepcion", "Concepcion", "Centro comercial y operativo", -36.8201, -73.0444),
    ]
    for name, city, address, latitude, longitude in branches:
        Branch.objects.get_or_create(
            name=name,
            defaults={"city": city, "address": address, "latitude": latitude, "longitude": longitude},
        )

    products = [
        ("Guitarra electrica MP-Stage", "Instrumentos", "Cuerpo solido, sonido definido y acabado profesional.", 349990, 12, "music_note"),
        ("Interfaz de audio Studio 4", "Audio profesional", "Cuatro entradas para grabacion y produccion musical.", 229990, 8, "graphic_eq"),
        ("Microfono dinamico Vocal Pro", "Microfonos", "Captura vocal clara para escenario y estudio.", 89990, 20, "mic"),
        ("Audifonos Monitor MX", "Monitoreo", "Respuesta equilibrada para mezcla y escucha critica.", 69990, 15, "headphones"),
    ]
    for name, category, description, price, stock, icon in products:
        Product.objects.get_or_create(
            name=name,
            defaults={"category": category, "description": description, "price": price, "stock": stock, "icon": icon},
        )


def remove_catalog(apps, schema_editor):
    apps.get_model("music_pro", "Product").objects.all().delete()
    apps.get_model("music_pro", "Branch").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("music_pro", "0002_branch_order_product_orderitem")]
    operations = [migrations.RunPython(seed_catalog, remove_catalog)]
