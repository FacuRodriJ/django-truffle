import datetime

from django.http import JsonResponse
from django.urls import reverse

from .models import Rendicion, Presentacion, Documento
from .web3_connector import get_contract, get_provider


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

        w3 = get_provider()
        contract = get_contract()
        contract.functions.addPresentation(presentacion.pk, presentacion.get_hash_list()).transact(
            {"from": w3.eth.accounts[0]})

        presentacion.save()
        return JsonResponse(
            {"status": "ok", "url": reverse("core:rendicion_list"),
             "message": "Presentación realizada con éxito, el hash utilizado es SHA256"})


def presentacion_post(request):
    if request.POST["action"] == "validar":
        presentacion = Presentacion.objects.get(pk=request.POST["pk"])
        contract = get_contract()
        hash_list = contract.functions.getPresentation(presentacion.pk).call()
        presentacion_hash_list = presentacion.get_hash_list()
        if hash_list == presentacion_hash_list:
            return JsonResponse(
                {"status": "ok", "url": reverse("core:presentacion_detail", kwargs={"pk": presentacion.pk})})
        else:
            return JsonResponse({"status": "error", "message": "Las presentaciones no coinciden"})


def validacion_post(request):
    if request.POST["action"] == "search_presentacion":
        presentacion = Presentacion.objects.get(pk=request.POST["pk"])
        contract = get_contract()
        hash_list = contract.functions.getPresentation(presentacion.pk).call()
        if hash_list:
            return JsonResponse({"status": "ok", "hash_list": hash_list})
        else:
            return JsonResponse({"status": "error", "message": "No existe presentación"})
