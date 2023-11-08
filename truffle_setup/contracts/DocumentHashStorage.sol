// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;


contract DocumentHashStorage {

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    function changeOwner(address _newOwner) public onlyOwner {
        require(_newOwner != owner, "New owner must be different than current owner.");
        owner = _newOwner;
    }

    struct Document {
        string hashId;
        uint256 timestamp;
    }

    // Mapeo que relaciona el id de una Presentación con un array de Documentos
    mapping(uint256 => Document[]) public documents;

    function addPresentation(uint256 _presentationId, string[] memory _hashIds) public onlyOwner {
        for (uint256 i = 0; i < _hashIds.length; i++) {
            documents[_presentationId].push(Document(_hashIds[i], block.timestamp));
        }
    }

    function getPresentation(uint256 _presentationId) public view returns (string[] memory) {
        string[] memory hashIds = new string[](documents[_presentationId].length);
        for (uint256 i = 0; i < documents[_presentationId].length; i++) {
            hashIds[i] = documents[_presentationId][i].hashId;
        }
        return hashIds;
    }


}
