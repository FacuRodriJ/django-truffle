// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;


contract DocumentHashStorage {

    address public owner;

    constructor() {
        owner = msg.sender;
        addPresentation(0, 0, 0, "", new string[](0), new string[](0));
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    function changeOwner(address _newOwner) public onlyOwner {
        require(_newOwner != owner, "New owner must be different than current owner.");
        owner = _newOwner;
    }

    struct Documento {
        string tipo_documento;
        string hashId;
    }

    struct Presentacion {
        uint256 fecha_presentacion;
        uint nro_presentacion;
        uint anio;
        uint periodo;
        string munipicio;
        Documento[] documentos;
    }

    uint256 public presentacionesCount = 0;

    mapping(uint256 => Presentacion) public presentaciones;

    event PresentationAdded(
        uint256 presentacionId,
        uint256 fecha_presentacion,
        uint nro_presentacion,
        uint anio,
        uint periodo,
        string munipicio,
        Documento[] documentos
    );

    function addPresentation(
        uint _nro_presentacion,
        uint _anio,
        uint _periodo,
        string memory _munipicio,
        string[] memory _tipos_documentos,
        string[] memory _hashIds
    ) public onlyOwner {
        require(_hashIds.length == _tipos_documentos.length, "Hashes and document types must have the same length.");

        Presentacion storage presentacion = presentaciones[presentacionesCount];

        presentacion.fecha_presentacion = block.timestamp;
        presentacion.nro_presentacion = _nro_presentacion;
        presentacion.anio = _anio;
        presentacion.periodo = _periodo;
        presentacion.munipicio = _munipicio;

        for (uint i = 0; i < _hashIds.length; i++) {
            presentacion.documentos.push(Documento(_tipos_documentos[i], _hashIds[i]));
        }

        emit PresentationAdded(
            presentacionesCount,
            presentacion.fecha_presentacion,
            presentacion.nro_presentacion,
            presentacion.anio,
            presentacion.periodo,
            presentacion.munipicio,
            presentacion.documentos
        );
        presentacionesCount++;
    }

    function getPresentation(uint256 _presentacionId) public view returns (
        uint256,
        uint,
        uint,
        uint,
        string memory,
        Documento[] memory
    ) {
        Presentacion memory presentacion = presentaciones[_presentacionId];
        return (
            presentacion.fecha_presentacion,
            presentacion.nro_presentacion,
            presentacion.anio,
            presentacion.periodo,
            presentacion.munipicio,
            presentacion.documentos
        );
    }
}
