from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, FormView
from django.urls import reverse_lazy, reverse
from django import forms
from django.http import JsonResponse

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
        context["title"] = "Listado de Rendiciones"
        return context


class DocumentoRendicionForm(forms.ModelForm):
    """
    Formulario de Presentaciones
    """

    class Meta:
        model = DocumentoRendicion
        fields = ["archivo", "documento_requerido"]
        widgets = {
            "archivo": forms.FileInput(attrs={"class": "form-control"}),
            "documento_requerido": forms.Select(attrs={"class": "form-select"}),
        }


class PresentacionFormView(FormView):
    """
    Vista de Presentación de Rendiciones
    """

    template_name = "presentacion_form.html"
    form_class = DocumentoRendicionForm

    def get_success_url(self):
        return reverse("rendicion_form", kwargs={"pk": self.kwargs["pk"]})

    def dispatch(self, request, *args, **kwargs):
        # Se obtiene la rendicion
        rendicion = Rendicion.objects.get(pk=self.kwargs["pk"])
        if rendicion.presentacion_set.count() == 0 or rendicion.presentacion_set.filter(estado=False).count() == 0:
            # Se crea la presentacion
            presentacion = Presentacion(rendicion=rendicion, nro_presentacion=1)
            presentacion.save()
        # Si la ultima presentacion esta presentada se debe crear una nueva presentacion
        elif rendicion.presentacion_set.last().estado:
            # Se crea la presentacion
            presentacion = Presentacion(rendicion=rendicion,
                                        nro_presentacion=rendicion.presentacion_set.last().nro_presentacion + 1)
            presentacion.save()
        elif not rendicion.presentacion_set.last().estado:
            # Se obtiene la ultima presentacion con estado "En Carga"
            presentacion = rendicion.presentacion_set.filter(estado=False).last()
        # Guardar en la variable necesario para poder usarlo en el template
        request.presentacion = presentacion
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Presentación de Rendición"
        context["presentacion"] = self.request.presentacion
        return context

    def form_valid(self, form):
        form.instance.presentacion = self.request.presentacion
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        # Si se preciona el boton "Eliminar" se elimina el archivo
        if request.POST["action"] == "delete":
            DocumentoRendicion.objects.get(pk=request.POST["pk"]).delete()
            return JsonResponse({"status": "ok"})
        return super().post(request, *args, **kwargs)
