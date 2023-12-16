from django.urls import reverse
from django.views.generic import ListView, FormView, DetailView

from .forms import DocumentoForm
from .http_verbs import rendicion_post
from .models import Rendicion, Presentacion


class RendicionListView(ListView):
    """
    Vista de Listado de Rendiciones
    """

    model = Rendicion
    template_name = "rendicion_list.html"
    context_object_name = "rendiciones"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Rendiciones Municipales"
        return context


class RendicionDetailView(DetailView):
    """
    Vista de Detalle de Rendicion
    """

    model = Rendicion
    template_name = "rendicion_detail.html"
    context_object_name = "rendicion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalle de Rendición Municipal"
        context["presentaciones"] = self.object.presentacion_set.filter(estado=True).order_by("-nro_presentacion")
        return context


class RendicionFormView(FormView):
    """
    Vista del Formulario de Rendición
    """

    template_name = "rendicion_form.html"
    form_class = DocumentoForm

    def get_success_url(self):
        return reverse("rendicion_form", kwargs={"pk": self.kwargs["pk"]})

    def get(self, request, *args, **kwargs):
        rendicion = Rendicion.objects.get(pk=self.kwargs["pk"])
        if rendicion.presentacion_set.count() == 0:
            presentacion = Presentacion(rendicion=rendicion, nro_presentacion=1)
            presentacion.save()
        elif rendicion.presentacion_set.last().estado:
            nro_presentacion = rendicion.presentacion_set.last().nro_presentacion + 1
            presentacion = Presentacion(rendicion=rendicion, nro_presentacion=nro_presentacion)
            presentacion.save()
        else:
            presentacion = rendicion.presentacion_set.filter(estado=False).last()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Formulario de Rendición Municipal"
        context["presentacion"] = Presentacion.objects.filter(rendicion=self.kwargs["pk"]).last()
        return context

    def form_valid(self, form):
        rendicion = Rendicion.objects.get(pk=self.kwargs["pk"])
        form.instance.presentacion = rendicion.presentacion_set.last()
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if "action" in request.POST:
            return rendicion_post(request)
        return super().post(request, *args, **kwargs)


class PresentacionDetailView(DetailView):
    """
    Vista de Detalle de Presentacion
    """

    model = Presentacion
    template_name = "presentacion_detail.html"
    context_object_name = "presentacion"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Detalle de Presentación"
        return context
