from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CheckoutForm, FranchiseInquiryForm, RegisterForm
from .models import Branch, Order, OrderItem, Product


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
    product = get_object_or_404(Product, pk=product_id, active=True)
    cart = request.session.get("cart", {})
    product_key = str(product.pk)
    cart[product_key] = min(cart.get(product_key, 0) + 1, product.stock)
    request.session["cart"] = cart
    messages.success(request, f"{product.name} agregado al carrito.")
    return redirect(request.POST.get("next") or reverse("shop"))


def cart(request):
    cart_data = request.session.get("cart", {})
    products = Product.objects.filter(pk__in=cart_data.keys(), active=True)
    items = [{"product": product, "quantity": cart_data.get(str(product.pk), 0)} for product in products]
    subtotal = sum(item["product"].price * item["quantity"] for item in items)
    return render(request, "music_pro/cart.html", {"items": items, "subtotal": subtotal})


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
        distance = data.get("distance_km") or 0
        shipping = 0 if data["delivery_type"] == "pickup" else 3500 + (distance * 500)
        order = Order.objects.create(
            user=request.user,
            branch=data["branch"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            billing_address=data.get("billing_address", ""),
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
