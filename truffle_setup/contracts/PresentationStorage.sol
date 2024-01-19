// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;


contract PresentationStorage {

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

    // Estructura que representa una Presentación
    struct Presentation {
        uint256 presentationDatetime;
        uint256 presentationNumber;
        uint256 year;
        uint256 period;
        string municipio;
        string[] fileDescriptions; // Descripción de los archivos
        string[] fileHashes; // Hashes de los archivos
        // El elemento i de fileDescriptions corresponde con el elemento i de fileHashes
    }

    // Contador de Presentaciones, se utiliza para generar el ID de cada Presentación
    uint256 public presentationsCount = 0;

    // Lista que almacena las Presentaciones
    Presentation[] public presentationsList;

    // Evento que se emite al agregar una nueva Presentación
    event PresentationAdded(uint256 indexed presentationCount);

    // Función que permite agregar una nueva Presentación
    function addPresentation(
        uint256 _presentationNumber,
        uint256 _year,
        uint256 _period,
        string memory _municipio,
        string[] memory _descriptions,
        string[] memory _hashIds
    ) public onlyOwner {
        require(_hashIds.length == _descriptions.length, "Hashes and document descriptions must have the same length.");

        // Agregamos la Presentación al array
        presentationsList.push(Presentation({
            presentationDatetime: block.timestamp,
            presentationNumber: _presentationNumber,
            year: _year,
            period: _period,
            municipio: _municipio,
            fileDescriptions: _descriptions,
            fileHashes: _hashIds
        }));

        // Emitimos el evento con el contador de Presentaciones
        emit PresentationAdded(presentationsCount);

        // Incrementamos el contador de Presentaciones para que el próximo ID sea diferente
        presentationsCount++;
    }

    // Función que retorna los datos de una Presentación
    function getPresentationByCount(uint256 _presentationCount) public view returns (
        uint256,
        uint256,
        uint256,
        uint256,
        string memory,
        string[] memory,
        string[] memory
    ) {
        // Obtenemos la Presentación del array
        Presentation memory presentation = presentationsList[_presentationCount];

        return (
            presentation.presentationDatetime,
            presentation.presentationNumber,
            presentation.year,
            presentation.period,
            presentation.municipio,
            presentation.fileDescriptions,
            presentation.fileHashes
        );
    }
}
