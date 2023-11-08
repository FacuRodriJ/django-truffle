import json
import os

from web3 import Web3


def get_provider():
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    return w3


def get_contract():
    w3 = get_provider()
    current_directory = os.path.dirname(os.path.abspath(__file__))
    relative_path = "../../truffle_setup/build/contracts/DocumentHashStorage.json"
    contract_path = os.path.join(current_directory, relative_path)
    with open(contract_path, "r") as f:
        datastore_json = f.read()
    datastore_abi = json.loads(datastore_json)["abi"]
    contract_address = '0xE675C87fBb126baf2f80B690eCdDDF4Fc7edB6A1'
    contract = w3.eth.contract(address=contract_address, abi=datastore_abi)
    return contract
