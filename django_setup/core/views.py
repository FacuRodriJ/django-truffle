import datetime
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import ListView, FormView, DetailView

from .forms import DocumentoRendicionForm
from .models import Rendicion, Presentacion, DocumentoRendicion


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
        context["presentaciones"] = self.object.presentacion_set.filter(estado=True)
        return context


class RendicionFormView(FormView):
    """
    Vista del Formulario de Rendicion
    """

    template_name = "rendicion_form.html"
    form_class = DocumentoRendicionForm

    def get_success_url(self):
        return reverse("core:rendicion_form", kwargs={"pk": self.kwargs["pk"]})

    def get(self, request, *args, **kwargs):
        # Se obtiene la rendicion
        rendicion = Rendicion.objects.get(pk=self.kwargs["pk"])
        if rendicion.presentacion_set.count() == 0:
            # Se crea la presentacion
            presentacion = Presentacion(rendicion=rendicion, nro_presentacion=1)
            presentacion.save()
        # Si la ultima presentacion esta presentada se debe crear una nueva presentacion
        elif rendicion.presentacion_set.last().estado:
            # Se crea la presentacion
            presentacion = Presentacion(rendicion=rendicion,
                                        nro_presentacion=rendicion.presentacion_set.last().nro_presentacion + 1)
            presentacion.save()
        else:
            # Se obtiene la ultima presentacion con estado "En Carga"
            presentacion = rendicion.presentacion_set.filter(estado=False).last()
        # Guardar en la variable necesario para poder usarlo en el template
        request.presentacion = presentacion
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Formulario de Rendición Municipal"
        context["presentacion"] = self.request.presentacion
        return context

    def form_valid(self, form):
        rendicion = Rendicion.objects.get(pk=self.kwargs["pk"])
        form.instance.presentacion = rendicion.presentacion_set.last()
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        # Si se preciona el boton "Eliminar" se elimina el archivo
        if "action" in request.POST:
            if request.POST["action"] == "delete":
                DocumentoRendicion.objects.get(pk=request.POST["pk"]).delete()
                return JsonResponse({"status": "ok"})
            if request.POST["action"] == "presentar":
                # Se obtiene la presentacion
                presentacion = Presentacion.objects.get(pk=request.POST["pk"])
                # Se cambia el estado de la presentacion
                presentacion.estado = True
                presentacion.fecha_presentacion = datetime.date.today()
                presentacion.save()
                return JsonResponse({"status": "ok", "url": reverse("core:rendicion_list")})
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
