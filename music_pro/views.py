from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CheckoutForm, FranchiseInquiryForm, RegisterForm
from .models import Branch, Order, OrderItem, Product


def home(request):
    return render(request, "music_pro/home.html")


def branches_and_franchises(request):
    if request.method == "POST":
        form = FranchiseInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Solicitud recibida. El equipo de Music Pro te contactará pronto.")
            return redirect("branches-and-franchises")
    else:
        form = FranchiseInquiryForm()

    return render(request, "music_pro/sucursales.html", {"form": form})


def shop(request):
    return render(request, "music_pro/shop.html", {"products": Product.objects.filter(active=True)})


def add_to_cart(request, product_id):
    with transaction.atomic():
        product = get_object_or_404(Product.objects.select_for_update(), pk=product_id, active=True)
        if product.stock < 1:
            messages.error(request, f"{product.name} no tiene stock disponible.")
            return redirect(request.POST.get("next") or reverse("shop"))
        product.stock -= 1
        product.save(update_fields=["stock"])
    cart = request.session.get("cart", {})
    product_key = str(product.pk)
    cart[product_key] = cart.get(product_key, 0) + 1
    request.session["cart"] = cart
    messages.success(request, f"{product.name} fue agregado al carrito.", extra_tags="cart-added")
    return redirect(request.POST.get("next") or reverse("shop"))


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_key = str(product_id)
    quantity = cart.pop(product_key, 0)
    if quantity:
        Product.objects.filter(pk=product_id).update(stock=F("stock") + quantity)
        request.session["cart"] = cart
        messages.success(request, "Producto eliminado y stock restaurado.")
    return redirect("cart")


def decrease_cart_quantity(request, product_id):
    cart = request.session.get("cart", {})
    product_key = str(product_id)
    quantity = cart.get(product_key, 0)
    if quantity:
        if quantity == 1:
            del cart[product_key]
        else:
            cart[product_key] = quantity - 1
        Product.objects.filter(pk=product_id).update(stock=F("stock") + 1)
        request.session["cart"] = cart
        messages.success(request, "Una unidad fue retirada del carrito.")
    return redirect("cart")


def cart(request):
    cart_data = request.session.get("cart", {})
    products = Product.objects.filter(pk__in=cart_data.keys(), active=True)
    items = [{"product": product, "quantity": cart_data.get(str(product.pk), 0)} for product in products]
    subtotal = sum(item["product"].price * item["quantity"] for item in items)
    available_products = Product.objects.filter(active=True, stock__gt=0).exclude(pk__in=cart_data.keys())[:6]
    return render(
        request,
        "music_pro/cart.html",
        {"items": items, "subtotal": subtotal, "available_products": available_products},
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("shop")
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("shop")
    return render(request, "music_pro/register.html", {"form": form})


@login_required
def checkout(request):
    cart_data = request.session.get("cart", {})
    products = Product.objects.filter(pk__in=cart_data.keys(), active=True)
    items = [{"product": product, "quantity": cart_data.get(str(product.pk), 0)} for product in products]
    subtotal = sum(item["product"].price * item["quantity"] for item in items)
    if not items:
        return redirect("shop")
    form = CheckoutForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        distance = 0
        shipping = 0 if data["delivery_type"] == "pickup" else 3990
        order = Order.objects.create(
            user=request.user,
            branch=data["branch"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            rut=data.get("rut", ""),
            region=data.get("region", ""),
            commune=data.get("commune", ""),
            billing_address=data.get("billing_address", ""),
            property_type=data.get("property_type", ""),
            delivery_comment=data.get("delivery_comment", ""),
            delivery_type=data["delivery_type"],
            distance_km=distance,
            shipping_cost=shipping,
            payment_method=data["payment_method"],
            total=subtotal + shipping,
        )
        OrderItem.objects.bulk_create([
            OrderItem(order=order, product=item["product"], quantity=item["quantity"], unit_price=item["product"].price)
            for item in items
        ])
        request.session["cart"] = {}
        messages.success(request, f"Pedido #{order.pk} creado correctamente.")
        return redirect("shop")
    return render(request, "music_pro/checkout.html", {"form": form, "items": items, "subtotal": subtotal})
