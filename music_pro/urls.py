from django.urls import path

from .views import (
    add_to_cart,
    branches_and_franchises,
    cart,
    checkout,
    decrease_cart_quantity,
    home,
    login_view,
    logout_view,
    register,
    remove_from_cart,
    shop,
)

urlpatterns = [
    path("", home, name="home"),
    path("sucursales-franquicias/", branches_and_franchises, name="branches-and-franchises"),
    path("tienda/", shop, name="shop"),
    path("carrito/", cart, name="cart"),
    path("carrito/agregar/<int:product_id>/", add_to_cart, name="add-to-cart"),
    path("carrito/eliminar/<int:product_id>/", remove_from_cart, name="remove-from-cart"),
    path("carrito/restar/<int:product_id>/", decrease_cart_quantity, name="decrease-cart-quantity"),
    path("comprar/", checkout, name="checkout"),
    path("ingresar/", login_view, name="login"),
    path("salir/", logout_view, name="logout"),
    path("registro/", register, name="register"),
]
