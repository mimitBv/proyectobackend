from types import SimpleNamespace

from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CheckoutForm, FranchiseInquiryForm, LoginForm, RegisterForm

PRODUCTS = [
    SimpleNamespace(id=1, name="Piano digital Stage 88", category="Teclados", description="Teclado de 88 teclas con acción sensible y sonidos profesionales.", price=599990, stock=6, image="products/piano digital stage 88.png", active=True),
    SimpleNamespace(id=2, name="Teclado sintetizador Wave 61", category="Teclados", description="Sintetizador de 61 teclas para directo, estudio y composición.", price=429990, stock=7, image="products/teclado sintetizador wave 61.png", active=True),
    SimpleNamespace(id=3, name="Bateria electronica Beat Kit", category="Baterias", description="Kit compacto con pads sensibles y módulo de sonidos integrado.", price=489990, stock=5, image="products/bateria electronica beat kit.png", active=True),
    SimpleNamespace(id=4, name="Platillos Crash Bronze 16", category="Baterias", description="Platillo de bronce para un ataque brillante y definido.", price=119990, stock=10, image="products/platillos crash bronze 16.png", active=True),
    SimpleNamespace(id=5, name="Bajo electrico MP-Classic", category="Instrumentos", description="Bajo de cuatro cuerdas con tono profundo para escenario.", price=379990, stock=8, image="products/bajo electrico mp-classic.png", active=True),
    SimpleNamespace(id=6, name="Amplificador de guitarra 40W", category="Amplificacion", description="Amplificador versátil con canal limpio y overdrive.", price=189990, stock=9, image="products/amplificador de bajo 40 W.png", active=True),
    SimpleNamespace(id=7, name="Amplificador de bajo 100W", category="Amplificacion", description="Potencia y claridad para ensayos, salas y presentaciones.", price=299990, stock=5, image="products/amplificador de bajo 100W.png", active=True),
    SimpleNamespace(id=8, name="Pedal Overdrive Drive One", category="Pedales", description="Overdrive analógico para tonos cálidos y con respuesta dinámica.", price=79990, stock=14, image="products/pedal onedrive drive one.png", active=True),
    SimpleNamespace(id=9, name="Pedal Delay Echo Time", category="Pedales", description="Delay digital con controles de tiempo, mezcla y repeticiones.", price=94990, stock=11, image="products/pedal delay echo time.png", active=True),
    SimpleNamespace(id=10, name="Multiefectos Guitar Lab", category="Pedales", description="Procesador con efectos, presets y afinador incorporado.", price=219990, stock=6, image="products/multiefectos guitar lab.png", active=True),
    SimpleNamespace(id=11, name="Mezcladora compacta Mix 8", category="Audio profesional", description="Mezcladora de ocho canales para ensayos y eventos pequeños.", price=159990, stock=9, image="products/mezcladora compacta mix 8.png", active=True),
    SimpleNamespace(id=12, name="Monitor de estudio Nearfield 5", category="Monitoreo", description="Monitor activo de cinco pulgadas para mezcla de precisión.", price=169990, stock=12, image="products/monitor de estudiio nearfield 5.png", active=True),
    SimpleNamespace(id=13, name="Par de monitores Studio 8", category="Monitoreo", description="Monitores activos para una escucha amplia y detallada.", price=399990, stock=6, image="products/par de monitores estudio 8.png", active=True),
    SimpleNamespace(id=14, name="Microfono condensador Studio C1", category="Micrófonos", description="Micrófono de condensador para voces, instrumentos y podcast.", price=129990, stock=10, image="products/microfono condensador Studio C1.png", active=True),
    SimpleNamespace(id=15, name="Microfono inalambrico Stage", category="Micrófonos", description="Sistema inalámbrico confiable para presentaciones en vivo.", price=199990, stock=8, image="products/microfono inalambrico stage.png", active=True),
    SimpleNamespace(id=16, name="Soporte de teclado reforzado", category="Accesorios", description="Soporte plegable y estable para teclados de distintos tamaños.", price=49990, stock=20, image="products/soporte de teclado reforzado.png", active=True),
    SimpleNamespace(id=17, name="Atril profesional plegable", category="Accesorios", description="Atril metálico regulable para partituras y presentaciones.", price=29990, stock=25, image="products/atril profesional plegable.png", active=True),
    SimpleNamespace(id=18, name="Cable de instrumento 6 metros", category="Accesorios", description="Cable blindado para guitarra, bajo y otros instrumentos.", price=19990, stock=30, image="products/cable de instrumento 6 metros.png", active=True),
    SimpleNamespace(id=19, name="Set de cuerdas guitarra electrica", category="Accesorios", description="Cuerdas de acero con calibre versátil para guitarra eléctrica.", price=12990, stock=35, image="products/set de cuerdas de guitarra.png", active=True),
    SimpleNamespace(id=20, name="Afinador cromatico Clip Pro", category="Accesorios", description="Afinador compacto con pantalla clara y detección rápida.", price=9990, stock=40, image="products/afinador cromatico clip pro.png", active=True),
    SimpleNamespace(id=21, name="Interfaz de audio Studio 4", category="Audio profesional", description="Cuatro entradas para grabación y producción musical.", price=229990, stock=8, image="products/interfaz de audio studio 4.png", active=True),
    SimpleNamespace(id=22, name="Microfono dinamico Vocal Pro", category="Microfonos", description="Captura vocal clara para escenario y estudio.", price=89990, stock=20, image="products/microfono dinamico vocal pro.png", active=True),
    SimpleNamespace(id=23, name="Audifonos Monitor MX", category="Monitoreo", description="Respuesta equilibrada para mezcla y escucha crítica.", price=69990, stock=15, image="products/audifonos monitor mx.png", active=True),
    SimpleNamespace(id=24, name="Guitarra electrica MP-Stage", category="Instrumentos", description="Cuerpo sólido, sonido definido y acabado profesional.", price=349990, stock=12, image="products/guitarra electrica mp-stage.png", active=True),
]


def _product_by_id(product_id):
    for product in PRODUCTS:
        if str(product.id) == str(product_id):
            return product
    return None


def _cart_items(request):
    cart = request.session.get("cart", {})
    items = []
    subtotal = 0
    for product in PRODUCTS:
        quantity = cart.get(str(product.id), 0)
        if quantity:
            items.append({"product": product, "quantity": quantity})
            subtotal += product.price * quantity
    return cart, items, subtotal


def _available_products(cart):
    available = []
    for product in PRODUCTS:
        if product.stock > 0 and str(product.id) not in cart:
            available.append(product)
    return available[:6]


def home(request):
    return render(request, "music_pro/home.html")


def admin_dashboard(request):
    if not request.session.get("demo_user", {}).get("is_admin"):
        messages.error(request, "Debes iniciar sesión como administrador para acceder.")
        return redirect("home")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "stock":
            messages.success(request, "Demo admin: el cambio de stock se simula sin base de datos.")
        elif action == "order-status":
            messages.success(request, "Demo admin: el estado del pedido se actualiza en memoria.")
        return redirect("admin-dashboard")

    return render(
        request,
        "music_pro/admin_dashboard.html",
        {
            "products": PRODUCTS[:12],
            "orders": [
                {"pk": 101, "user": {"username": "demo_cliente"}, "branch": {"name": "Santiago Centro"}, "status": "received", "total": 699000},
                {"pk": 102, "user": {"username": "demo_vendedor"}, "branch": {"name": "Providencia"}, "status": "dispatched", "total": 899000},
            ],
            "franchise_inquiries": [
                {"name": "Ana", "city": "Valparaíso", "email": "ana@ejemplo.com"},
                {"name": "Luis", "city": "Concepción", "email": "luis@ejemplo.com"},
            ],
            "product_count": len(PRODUCTS),
            "low_stock_count": sum(1 for product in PRODUCTS if product.stock <= 3),
            "new_order_count": 2,
            "dispatch_count": 1,
            "franchise_count": 2,
            "status_choices": [("received", "Recibido"), ("dispatched", "Despachado"), ("completed", "Completado")],
        },
    )


def branches_and_franchises(request):
    if request.method == "POST":
        form = FranchiseInquiryForm(request.POST)
        if form.is_valid():
            messages.success(request, "Solicitud recibida. El equipo de Music Pro te contactará pronto.")
            return redirect("branches-and-franchises")
    else:
        form = FranchiseInquiryForm()

    return render(request, "music_pro/sucursales.html", {"form": form})


def shop(request):
    return render(request, "music_pro/shop.html", {"products": PRODUCTS})


def add_to_cart(request, product_id):
    product = _product_by_id(product_id)
    if product is None or not product.active:
        messages.error(request, "El producto no está disponible.")
        return redirect(request.POST.get("next") or reverse("shop"))

    cart = request.session.get("cart", {})
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    request.session["cart"] = cart
    messages.success(request, f"{product.name} fue agregado al carrito.", extra_tags="cart-added")
    return redirect(request.POST.get("next") or reverse("shop"))


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    messages.success(request, "Producto eliminado del carrito.")
    return redirect("cart")


def decrease_cart_quantity(request, product_id):
    cart = request.session.get("cart", {})
    product_key = str(product_id)
    quantity = cart.get(product_key, 0)
    if quantity:
        if quantity <= 1:
            del cart[product_key]
        else:
            cart[product_key] = quantity - 1
    request.session["cart"] = cart
    messages.success(request, "Una unidad fue retirada del carrito.")
    return redirect("cart")


def cart(request):
    cart_data, items, subtotal = _cart_items(request)
    return render(
        request,
        "music_pro/cart.html",
        {"items": items, "subtotal": subtotal, "available_products": _available_products(cart_data)},
    )


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        if username == "admin" and password == "admin123":
            request.session["demo_user"] = {
                "username": "admin",
                "first_name": "Administrador",
                "last_name": "",
                "email": "admin@musicpro.demo",
                "is_admin": True,
            }
            messages.success(request, "Administrador autenticado correctamente.")
            return redirect("admin-dashboard")

        request.session["demo_user"] = {
            "username": username,
            "first_name": username,
            "last_name": "",
            "email": "",
            "is_admin": False,
        }
        messages.success(request, "Demo de sesión iniciada correctamente.")
        return redirect("shop")
    return render(request, "music_pro/login.html", {"form": form})


def logout_view(request):
    request.session.pop("demo_user", None)
    request.session.pop("is_admin", None)
    messages.success(request, "Sesión finalizada.")
    return redirect("shop")


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        request.session["demo_user"] = {
            "username": form.cleaned_data["username"],
            "first_name": form.cleaned_data["first_name"],
            "last_name": form.cleaned_data["last_name"],
            "email": form.cleaned_data["email"],
        }
        messages.success(request, "Cuenta demo creada correctamente.")
        return redirect("shop")
    return render(request, "music_pro/register.html", {"form": form})


def checkout(request):
    cart_data, items, subtotal = _cart_items(request)
    if not items:
        return redirect("shop")

    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        shipping = 0 if data["delivery_type"] == "pickup" else 3990
        request.session["cart"] = {}
        messages.success(request, "Pedido demo confirmado correctamente.")
        return redirect("shop")

    return render(request, "music_pro/checkout.html", {"form": form, "items": items, "subtotal": subtotal})
