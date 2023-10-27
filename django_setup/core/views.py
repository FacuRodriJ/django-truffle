from django.shortcuts import render
from django.views.generic.list import ListView

from .models import Rendicion


class RendicionListView(ListView):
    """
    Vista de Listado de Rendiciones
    """

    model = Rendicion
    template_name = "rendicion_list.html"
    context_object_name = "rendiciones"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Rendiciones"
        return context
