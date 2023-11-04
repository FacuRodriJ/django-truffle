import datetime

from django.http import JsonResponse
from django.urls import reverse
from web3 import Web3

from .models import Rendicion, Presentacion, Documento


def rendicion_get(self, request, *args, **kwargs):
    return 0


def rendicion_post(request):
    if request.POST["action"] == "delete":
        Documento.objects.get(pk=request.POST["pk"]).delete()
        return JsonResponse({"status": "ok"})
    if request.POST["action"] == "presentar":
        presentacion = Presentacion.objects.get(pk=request.POST["pk"])
        if presentacion.documento_set.count() == 0:
            return JsonResponse({"status": "error", "message": "No hay documentos cargados"})
        presentacion.estado = True
        presentacion.fecha_presentacion = datetime.date.today()
        # presentacion.save()
        w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
        print(w3.is_connected())

        rendicion = {
            "id": presentacion.rendicion.id,
            "fecha": presentacion.rendicion.fecha.strftime("%d/%m/%Y"),
            "monto": presentacion.rendicion.monto,
            "nro_presentacion": presentacion.nro_presentacion,
            "fecha_presentacion": presentacion.fecha_presentacion.strftime("%d/%m/%Y"),
            "estado": presentacion.estado,
            "documentos": []
        }

        return JsonResponse({"status": "ok", "url": reverse("core:rendicion_list")})
