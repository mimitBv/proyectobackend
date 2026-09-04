# Music Pro / proyectobackend

Proyecto Django para la gestion de sucursales, franquicias y solicitudes comerciales de Music Pro.

## Ejecutar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abre http://127.0.0.1:8000/.

El formulario de contacto guarda las solicitudes en SQLite y quedan disponibles en `/admin/` después de crear un superusuario con `python manage.py createsuperuser`.

## Estructura principal

- `music_pro/`: app Django, modelo, formulario, vistas y template de sucursales.
- `musicpro/`: configuración, URLs y entrada WSGI del proyecto.
- `pages/`: prototipos HTML organizados por módulo: storefront, catálogo, cuenta, checkout, administración y sucursales.
- `assets/images/`: capturas de pantalla del proyecto.
