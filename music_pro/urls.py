from django.urls import path

from .views import branches_and_franchises

urlpatterns = [
    path("", branches_and_franchises, name="branches-and-franchises"),
]
