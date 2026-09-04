from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import add_to_cart, branches_and_franchises, cart, checkout, register, shop

urlpatterns = [
    path("", branches_and_franchises, name="branches-and-franchises"),
    path("tienda/", shop, name="shop"),
    path("carrito/", cart, name="cart"),
    path("carrito/agregar/<int:product_id>/", add_to_cart, name="add-to-cart"),
    path("comprar/", checkout, name="checkout"),
    path("ingresar/", LoginView.as_view(template_name="music_pro/login.html", next_page="/tienda/"), name="login"),
    path("salir/", LogoutView.as_view(next_page="/tienda/"), name="logout"),
    path("registro/", register, name="register"),
]
