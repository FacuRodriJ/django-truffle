// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;


contract DocumentHashStorage {

    // Dirección de la cuenta del propietario del contrato
    address public owner;

    // Función constructora que se ejecuta al momento de desplegar el contrato
    constructor() {
        owner = msg.sender;
        addPresentation(0, 0, 0, "", new string[](0), new string[](0));
    }

    // Modificador que permite ejecutar una función solo al propietario del contrato
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    // Función que permite cambiar el propietario del contrato
    function changeOwner(address _newOwner) public onlyOwner {
        require(_newOwner != owner, "New owner must be different than current owner.");
        owner = _newOwner;
    }

    // Estructura que representa un Documento
    struct Document {
        string description;
        string hashId;
    }

    // Estructura que representa una Presentación
    struct Presentation {
        uint256 presentationDatetime;
        uint256 presentationNumber;
        uint256 year;
        uint256 period;
        string municipio;
        Document[] documents; // Lista de Documentos
    }

    // Contador de Presentaciones
    uint256 public presentationsCount = 0;

    // Mapping que almacena las Presentaciones, donde la clave es el id de la Presentación y el valor es el struct Presentación.
    mapping(uint256 => Presentation) public presentations;

    // Evento que se emite al agregar una nueva Presentación
    event PresentationAdded(
        uint256 indexed id,
        uint256 presentationDatetime,
        uint256 presentationNumber,
        uint256 year,
        uint256 period,
        string municipio,
        Document[] documents
    );

    // Función que permite agregar una nueva Presentación
    function addPresentation(
        uint256 _presentationNumber,
        uint256 _year,
        uint256 _period,
        string memory _municipio,
        string[] memory _description,
        string[] memory _hashIds
    ) public onlyOwner {
        require(_hashIds.length == _description.length, "Hashes and document descriptions must have the same length.");

        // Obtenemos la referencia a la Presentación que se va a agregar, utilizando el contador presentationsCount como id de la Presentación
        Presentation storage presentation = presentations[presentationsCount];

        presentation.presentationDatetime = block.timestamp;
        presentation.presentationNumber = _presentationNumber;
        presentation.year = _year;
        presentation.period = _period;
        presentation.municipio = _municipio;

        // Recorremos los hashes y descripciones de documentos para agregarlos a la Presentación
        for (uint i = 0; i < _hashIds.length; i++) {
            presentation.documents.push(Document(_description[i], _hashIds[i]));
        }

        // Emitimos el evento con los datos de la Presentación agregada
        emit PresentationAdded(
            presentationsCount,
            presentation.presentationDatetime,
            presentation.presentationNumber,
            presentation.year,
            presentation.period,
            presentation.municipio,
            presentation.documents
        );

        // Incrementamos el contador de Presentaciones para que el próximo id sea diferente
        presentationsCount++;
    }

    // Función que retorna los datos de una Presentación
    function getPresentationById(uint256 _presentationId) public view returns (
        uint256,
        uint256,
        uint256,
        uint256,
        string memory,
        Document[] memory
    ) {
        // Obtenemos la referencia a la Presentación que se va a obtener utilizando el id de la Presentación
        Presentation storage presentation = presentations[_presentationId];

        return (
            presentation.presentationDatetime,
            presentation.presentationNumber,
            presentation.year,
            presentation.period,
            presentation.municipio,
            presentation.documents
        );
    }
}
