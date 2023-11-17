// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;


contract DocumentHashStorage {

    address public owner; // Dirección de la cuenta del propietario del contrato

    constructor() {
        // Función que se ejecuta al momento de desplegar el contrato
        owner = msg.sender;
        addPresentation(0, 0, 0, "", new string[](0), new string[](0));
    }

    modifier onlyOwner() {
        // Modificador que permite ejecutar una función solo al propietario del contrato
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    function changeOwner(address _newOwner) public onlyOwner {
        // Función que permite cambiar el propietario del contrato
        require(_newOwner != owner, "New owner must be different than current owner.");
        owner = _newOwner;
    }

    struct Documento {
        // Estructura que representa un Documento
        string tipo_documento;
        string hashId; // Hash del Documento
    }

    struct Presentacion {
        // Estructura que representa una Presentación
        uint256 fecha_presentacion;
        uint nro_presentacion;
        uint anio;
        uint periodo;
        string munipicio;
        Documento[] documentos; // Lista de Documentos
    }

    uint256 public presentacionesCount = 0; // Contador de Presentaciones

    mapping(uint256 => Presentacion) public presentaciones;
    // Mapping que almacena las Presentaciones, donde la clave es el id de la Presentación y el valor es el struct Presentación.
    // El id de la Presentación se asigna automáticamente al momento de agregar una nueva Presentación utilizando el contador presentacionesCount.

    event PresentationAdded(
    // Evento que se emite al agregar una nueva Presentación
    // El evento nos permite obtener los datos de la Presentación agregada desde el back-end
        uint256 presentacionId,
        uint256 fecha_presentacion,
        uint nro_presentacion,
        uint anio,
        uint periodo,
        string munipicio,
        Documento[] documentos
    );

    function addPresentation(
    // Función que permite agregar una nueva Presentación
        uint _nro_presentacion,
        uint _anio,
        uint _periodo,
        string memory _munipicio,
        string[] memory _tipos_documentos,
        string[] memory _hashIds
    ) public onlyOwner {
        require(_hashIds.length == _tipos_documentos.length, "Hashes and document types must have the same length.");
        // Verificamos que la cantidad de hashes y tipos de documentos sea la misma

        Presentacion storage presentacion = presentaciones[presentacionesCount];
        // Obtenemos la referencia a la Presentación que se va a agregar, utilizando el contador presentacionesCount como id de la Presentación
        // storage (memoria persistente del contrato)

        presentacion.fecha_presentacion = block.timestamp;
        presentacion.nro_presentacion = _nro_presentacion;
        presentacion.anio = _anio;
        presentacion.periodo = _periodo;
        presentacion.munipicio = _munipicio;

        for (uint i = 0; i < _hashIds.length; i++) {
            // Recorremos los hashes y tipos de documentos para agregarlos a la Presentación
            presentacion.documentos.push(Documento(_tipos_documentos[i], _hashIds[i]));
        }

        emit PresentationAdded(
        // Emitimos el evento con los datos de la Presentación agregada
            presentacionesCount,
            presentacion.fecha_presentacion,
            presentacion.nro_presentacion,
            presentacion.anio,
            presentacion.periodo,
            presentacion.munipicio,
            presentacion.documentos
        );
        presentacionesCount++; // Incrementamos el contador de Presentaciones para que el próximo id sea diferente
    }

    function getPresentation(uint256 _presentacionId) public view returns (
    // Función que retorna los datos de una Presentación
        uint256,
        uint,
        uint,
        uint,
        string memory,
        Documento[] memory
    ) {
        Presentacion memory presentacion = presentaciones[_presentacionId];
        // Obtenemos la referencia a la Presentación que se va a obtener utilizando el id de la Presentación
        // memory (memoria volátil del contrato)
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
