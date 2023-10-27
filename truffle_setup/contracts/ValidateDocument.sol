// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract ValidateDocument {

  address public owner;

  constructor() {
    // Set the contract owner to the address who deployed the contract
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
}
