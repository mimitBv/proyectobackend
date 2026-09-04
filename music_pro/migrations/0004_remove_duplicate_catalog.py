from django.db import migrations


def remove_duplicates(apps, schema_editor):
    Branch = apps.get_model("music_pro", "Branch")
    Product = apps.get_model("music_pro", "Product")
    Branch.objects.filter(name__in=["Viña del Mar", "Concepción"]).delete()
    Product.objects.filter(name__in=["Guitarra eléctrica MP-Stage", "Micrófono dinámico Vocal Pro", "Audífonos Monitor MX"]).delete()


class Migration(migrations.Migration):
    dependencies = [("music_pro", "0003_seed_catalog")]
    operations = [migrations.RunPython(remove_duplicates, migrations.RunPython.noop)]
