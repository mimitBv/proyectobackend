from django.contrib import admin

from .models import FranchiseInquiry


@admin.register(FranchiseInquiry)
class FranchiseInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "email", "created_at")
    search_fields = ("name", "city", "email")
    list_filter = ("created_at",)
