from django.db import migrations
from django.db.models import Value
from django.db.models.functions import Replace


def swap_product_image_paths(apps, schema_editor):
    Product = apps.get_model("music_pro", "Product")
    Product.objects.filter(image__startswith="mockups/").update(
        image=Replace("image", Value("mockups/"), Value("products/"))
    )


class Migration(migrations.Migration):
    dependencies = [("music_pro", "0010_use_mockup_product_images")]
    operations = [migrations.RunPython(swap_product_image_paths, migrations.RunPython.noop)]