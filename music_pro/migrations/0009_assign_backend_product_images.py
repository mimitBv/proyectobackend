from django.db import migrations


PRODUCT_IMAGES = {
    "Afinador cromatico Clip Pro": "images/products/afinador cromatico clip pro.png",
    "Atril profesional plegable": "images/products/atril profesional plegable.png",
    "Cable de instrumento 6 metros": "images/products/cable de instrumento 6 metros.png",
    "Set de cuerdas guitarra electrica": "images/products/set de cuerdas de guitarra.png",
    "Soporte de teclado reforzado": "images/products/soporte de teclado reforzado.png",
    "Amplificador de bajo 100W": "images/products/amplificador de bajo 100W.png",
    "Amplificador de guitarra 40W": "images/products/amplificador de bajo 40 W.png",
    "Interfaz de audio Studio 4": "images/products/interfaz de audio studio 4.png",
    "Mezcladora compacta Mix 8": "images/products/mezcladora compacta mix 8.png",
    "Bateria electronica Beat Kit": "images/products/bateria electronica beat kit.png",
    "Platillos Crash Bronze 16": "images/products/platillos crash bronze 16.png",
    "Bajo electrico MP-Classic": "images/products/bajo electrico mp-classic.png",
    "Guitarra electrica MP-Stage": "images/products/guitarra electrica mp-stage.png",
    "Microfono dinamico Vocal Pro": "images/products/microfono dinamico vocal pro.png",
    "Microfono condensador Studio C1": "images/products/microfono condensador Studio C1.png",
    "Microfono inalambrico Stage": "images/products/microfono inalambrico stage.png",
    "Audifonos Monitor MX": "images/products/audifonos monitor mx.png",
    "Monitor de estudio Nearfield 5": "images/products/monitor de estudiio nearfield 5.png",
    "Par de monitores Studio 8": "images/products/par de monitores estudio 8.png",
    "Multiefectos Guitar Lab": "images/products/multiefectos guitar lab.png",
    "Pedal Delay Echo Time": "images/products/pedal delay echo time.png",
    "Pedal Overdrive Drive One": "images/products/pedal onedrive drive one.png",
    "Piano digital Stage 88": "images/products/piano digital stage 88.png",
    "Teclado sintetizador Wave 61": "images/products/teclado sintetizador wave 61.png",
}


def assign_images(apps, schema_editor):
    Product = apps.get_model("music_pro", "Product")
    for name, image in PRODUCT_IMAGES.items():
        Product.objects.filter(name=name).update(image=image)


class Migration(migrations.Migration):
    dependencies = [("music_pro", "0008_assign_individual_product_images")]
    operations = [migrations.RunPython(assign_images, migrations.RunPython.noop)]