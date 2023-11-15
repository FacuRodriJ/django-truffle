import datetime

from django.http import JsonResponse
from django.urls import reverse
from web3.logs import IGNORE

from .models import Presentacion, Documento
from .web3_connector import get_contract, get_provider, owner_adress


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

        tx_hash = contract.functions.addPresentation(
            presentacion.nro_presentacion,
            presentacion.rendicion.anio,
            presentacion.rendicion.periodo,
            presentacion.rendicion.municipio.nombre,
            presentacion.get_hash_list(),
            presentacion.get_tipo_documento_list(),
        ).transact({"from": owner_adress()})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        data_transaction = contract.events.PresentationAdded().process_receipt(tx_receipt, errors=IGNORE)[0]
        presentacion.save()
        return JsonResponse({
            "status": "ok",
            "url": reverse("core:rendicion_list"),
            "blockHash": data_transaction["blockHash"].hex(),
            "blockNumber": data_transaction["blockNumber"],
            "transactionHash": data_transaction["transactionHash"].hex(),
            "presentacionId": data_transaction["args"]["presentacionId"]
        })
