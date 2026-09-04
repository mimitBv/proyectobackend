from django.contrib import admin

from .models import Branch, FranchiseInquiry, Order, OrderItem, Product


@admin.register(FranchiseInquiry)
class FranchiseInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "email", "created_at")
    search_fields = ("name", "city", "email")
    list_filter = ("created_at",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "address")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "active")
    list_filter = ("category", "active")
    search_fields = ("name", "category")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "branch", "total", "payment_method", "created_at")
    list_filter = ("payment_method", "delivery_type", "created_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "unit_price")
