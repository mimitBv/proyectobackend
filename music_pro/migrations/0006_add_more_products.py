from django.db import migrations


def add_products(apps, schema_editor):
    Product = apps.get_model("music_pro", "Product")
    products = [
        ("Piano digital Stage 88", "Teclados", "Teclado de 88 teclas con accion sensible y sonidos profesionales.", 599990, 6, "piano"),
        ("Teclado sintetizador Wave 61", "Teclados", "Sintetizador de 61 teclas para directo, estudio y composicion.", 429990, 7, "piano"),
        ("Bateria electronica Beat Kit", "Baterias", "Kit compacto con pads sensibles y modulo de sonidos integrado.", 489990, 5, "album"),
        ("Platillos Crash Bronze 16", "Baterias", "Platillo de bronce para un ataque brillante y definido.", 119990, 10, "album"),
        ("Bajo electrico MP-Classic", "Instrumentos", "Bajo de cuatro cuerdas con tono profundo para escenario.", 379990, 8, "music_note"),
        ("Amplificador de guitarra 40W", "Amplificacion", "Amplificador versatil con canal limpio y overdrive.", 189990, 9, "speaker"),
        ("Amplificador de bajo 100W", "Amplificacion", "Potencia y claridad para ensayos, salas y presentaciones.", 299990, 5, "speaker"),
        ("Pedal Overdrive Drive One", "Pedales", "Overdrive analogico para tonos calidos y con respuesta dinamica.", 79990, 14, "tune"),
        ("Pedal Delay Echo Time", "Pedales", "Delay digital con controles de tiempo, mezcla y repeticiones.", 94990, 11, "tune"),
        ("Multiefectos Guitar Lab", "Pedales", "Procesador con efectos, presets y afinador incorporado.", 219990, 6, "tune"),
        ("Mezcladora compacta Mix 8", "Audio profesional", "Mezcladora de ocho canales para ensayos y eventos pequeños.", 159990, 9, "graphic_eq"),
        ("Monitor de estudio Nearfield 5", "Monitoreo", "Monitor activo de cinco pulgadas para mezcla de precision.", 169990, 12, "speaker"),
        ("Par de monitores Studio 8", "Monitoreo", "Monitores activos para una escucha amplia y detallada.", 399990, 6, "speaker"),
        ("Microfono condensador Studio C1", "Micrófonos", "Microfono de condensador para voces, instrumentos y podcast.", 129990, 10, "mic"),
        ("Microfono inalambrico Stage", "Micrófonos", "Sistema inalambrico confiable para presentaciones en vivo.", 199990, 8, "mic"),
        ("Soporte de teclado reforzado", "Accesorios", "Soporte plegable y estable para teclados de distintos tamanos.", 49990, 20, "stand"),
        ("Atril profesional plegable", "Accesorios", "Atril metalico regulable para partituras y presentaciones.", 29990, 25, "menu_book"),
        ("Cable de instrumento 6 metros", "Accesorios", "Cable blindado para guitarra, bajo y otros instrumentos.", 19990, 30, "cable"),
        ("Set de cuerdas guitarra electrica", "Accesorios", "Cuerdas de acero con calibre versatil para guitarra electrica.", 12990, 35, "settings"),
        ("Afinador cromatico Clip Pro", "Accesorios", "Afinador compacto con pantalla clara y deteccion rapida.", 9990, 40, "music_note"),
    ]
    for name, category, description, price, stock, icon in products:
        Product.objects.get_or_create(
            name=name,
            defaults={
                "category": category,
                "description": description,
                "price": price,
                "stock": stock,
                "icon": icon,
                "active": True,
            },
        )


class Migration(migrations.Migration):
    dependencies = [("music_pro", "0005_order_commune_order_delivery_comment_and_more")]
    operations = [migrations.RunPython(add_products, migrations.RunPython.noop)]
