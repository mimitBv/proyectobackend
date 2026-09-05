from django.db import migrations
from django.db.models import Value
from django.db.models.functions import Replace


def move_product_images_to_mockups(apps, schema_editor):
    Product = apps.get_model("music_pro", "Product")
    Product.objects.filter(image__startswith="images/products/").update(
        image=Replace("image", Value("images/products/"), Value("mockups/"))
    )


class Migration(migrations.Migration):
    dependencies = [("music_pro", "0009_assign_backend_product_images")]
    operations = [migrations.RunPython(move_product_images_to_mockups, migrations.RunPython.noop)]