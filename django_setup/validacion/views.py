import datetime

from django.views.generic import TemplateView
from django.http import JsonResponse
from django.conf import settings
from web3.logs import IGNORE


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
            if request.POST["action"] == "searchByPresentationID":
                id = int(request.POST["id"])
                presentacion = contract.functions.getPresentationById(id).call()
                # Fecha de uint solidity a datetime
                data["Fecha de presentacion"] = datetime.datetime.fromtimestamp(
                    presentacion[0]
                )
                data["Nro. Presentacion"] = presentacion[1]
                data["Año"] = presentacion[2]
                data["Periodo"] = presentacion[3]
                data["Municipio"] = presentacion[4]
                list_document = presentacion[5]
                for i in range(len(list_document)):
                    data[
                        "Documento " + str(i + 1) + " (Tipo Doc. + Hash256)"
                    ] = list_document[i]
            elif request.POST["action"] == "searchByTransactionHash":
                tx_hash = request.POST["hash"]
                tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
                data_transaction = contract.events.PresentationAdded().process_receipt(
                    tx_receipt, errors=IGNORE
                )[0]
                data["Presentacion ID"] = data_transaction["args"]["presentacionId"]
                data["Block Hash"] = data_transaction["blockHash"].hex()
                data["Block Number"] = data_transaction["blockNumber"]
                data["Contract Address"] = data_transaction["address"]
            return JsonResponse({"status": "ok", "data": data})
