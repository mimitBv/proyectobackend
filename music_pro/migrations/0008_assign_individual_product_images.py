from django.db import migrations


PRODUCT_IMAGES = {
    "Guitarra eléctrica MP-Stage": "images/products/guitarra-electrica-mp-stage.svg",
    "Guitarra electrica MP-Stage": "images/products/guitarra-electrica-mp-stage.svg",
    "Interfaz de audio Studio 4": "images/products/interfaz-audio-studio-4.svg",
    "Micrófono dinámico Vocal Pro": "images/products/microfono-dinamico-vocal-pro.svg",
    "Microfono dinamico Vocal Pro": "images/products/microfono-dinamico-vocal-pro.svg",
    "Audífonos Monitor MX": "images/products/audifonos-monitor-mx.svg",
    "Audifonos Monitor MX": "images/products/audifonos-monitor-mx.svg",
    "Piano digital Stage 88": "images/products/piano-digital-stage-88.svg",
    "Teclado sintetizador Wave 61": "images/products/teclado-sintetizador-wave-61.svg",
    "Bateria electronica Beat Kit": "images/products/bateria-electronica-beat-kit.svg",
    "Platillos Crash Bronze 16": "images/products/platillos-crash-bronze-16.svg",
    "Bajo electrico MP-Classic": "images/products/bajo-electrico-mp-classic.svg",
    "Amplificador de guitarra 40W": "images/products/amplificador-guitarra-40w.svg",
    "Amplificador de bajo 100W": "images/products/amplificador-bajo-100w.svg",
    "Pedal Overdrive Drive One": "images/products/pedal-overdrive-drive-one.svg",
    "Pedal Delay Echo Time": "images/products/pedal-delay-echo-time.svg",
    "Multiefectos Guitar Lab": "images/products/multiefectos-guitar-lab.svg",
    "Mezcladora compacta Mix 8": "images/products/mezcladora-compacta-mix-8.svg",
    "Monitor de estudio Nearfield 5": "images/products/monitor-estudio-nearfield-5.svg",
    "Par de monitores Studio 8": "images/products/par-monitores-studio-8.svg",
    "Microfono condensador Studio C1": "images/products/microfono-condensador-studio-c1.svg",
    "Microfono inalambrico Stage": "images/products/microfono-inalambrico-stage.svg",
    "Soporte de teclado reforzado": "images/products/soporte-teclado-reforzado.svg",
    "Atril profesional plegable": "images/products/atril-profesional-plegable.svg",
    "Cable de instrumento 6 metros": "images/products/cable-instrumento-6-metros.svg",
    "Set de cuerdas guitarra electrica": "images/products/set-cuerdas-guitarra-electrica.svg",
    "Afinador cromatico Clip Pro": "images/products/afinador-cromatico-clip-pro.svg",
}


def assign_images(apps, schema_editor):
    Product = apps.get_model("music_pro", "Product")
    for name, image in PRODUCT_IMAGES.items():
        Product.objects.filter(name=name).update(image=image)


class Migration(migrations.Migration):
    dependencies = [("music_pro", "0007_assign_product_images")]
    operations = [migrations.RunPython(assign_images, migrations.RunPython.noop)]
