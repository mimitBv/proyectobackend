from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import FranchiseInquiryForm


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
