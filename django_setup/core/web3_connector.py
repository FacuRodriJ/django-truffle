import json
import os

from web3 import Web3


def connector():
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    current_directory = os.path.dirname(os.path.abspath(__file__))
    relative_path = "../../truffle_setup/build/contracts/DocumentHashStorage.json"
    contract_path = os.path.join(current_directory, relative_path)
    with open(contract_path, "r") as f:
        datastore_json = f.read()
    datastore_abi = json.loads(datastore_json)["abi"]
    contract_address = '0x378380eFE0f8cd4a0835cc7e3Cb7e23515D2bBCa'
    contract = w3.eth.contract(address=contract_address, abi=datastore_abi)
    return w3, contract


def get_owner_adress():
    return '0xfA6d1e9E3a56c18700775DBaB3d890D6DB12ce93'
