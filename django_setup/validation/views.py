import datetime

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
from web3.logs import IGNORE
from web3 import exceptions


class ValidacionView(TemplateView):
    template_name = "validacion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Validación"
        return context

    def post(self, request, *args, **kwargs):
        if "action" in request.POST:
            data = {}
            w3 = settings.WEB3_CONNECTION
            contract = settings.WEB3_CONTRACT
            try:
                if request.POST["action"] == "searchByPresentationID":
                    id = int(request.POST["id"])
                    presentacion = contract.functions.getPresentationByCount(id).call()
                    # Fecha de uint solidity a datetime
                    data["FechaPresentacion"] = datetime.datetime.fromtimestamp(
                        presentacion[0]
                    )
                    data["NroPresentacion"] = presentacion[1]
                    data["Anio"] = presentacion[2]
                    data["Periodo"] = presentacion[3]
                    data["Municipio"] = presentacion[4]
                    data["Documentos"] = presentacion[5]
                    data["Hashes"] = presentacion[6]
                elif request.POST["action"] == "searchByTransactionHash":
                    tx_hash = request.POST["hash"]
                    tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
                    data_transaction = contract.events.PresentationAdded().process_receipt(
                        tx_receipt, errors=IGNORE
                    )[0]
                    data["Presentacion ID"] = data_transaction["args"]["presentationCount"]
                    data["Hash del Bloque"] = data_transaction["blockHash"].hex()
                    data["Nro del Bloque"] = data_transaction["blockNumber"]
                    data["Dirección del Contrato"] = data_transaction["address"]
                return JsonResponse({"status": "ok", "data": data})
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
        return JsonResponse({"status": "error", "message": "No se ha enviado una acción"})
