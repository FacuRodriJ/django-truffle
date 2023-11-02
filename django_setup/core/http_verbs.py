import datetime

from django.http import JsonResponse
from django.urls import reverse

from .models import Rendicion, Presentacion, DocumentoRendicion


def rendicion_get(self, request, *args, **kwargs):
    return 0


def rendicion_post(request):
    if request.POST["action"] == "delete":
        DocumentoRendicion.objects.get(pk=request.POST["pk"]).delete()
        return JsonResponse({"status": "ok"})
    if request.POST["action"] == "presentar":
        presentacion = Presentacion.objects.get(pk=request.POST["pk"])
        if presentacion.documentorendicion_set.count() == 0:
            return JsonResponse({"status": "error", "message": "No hay documentos cargados"})
        presentacion.estado = True
        presentacion.fecha_presentacion = datetime.date.today()
        presentacion.save()
        return JsonResponse({"status": "ok", "url": reverse("core:rendicion_list")})
