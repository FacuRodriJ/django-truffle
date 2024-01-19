const PresentationStorage = artifacts.require("PresentationStorage");

module.exports = function (deployer) {
    deployer.deploy(PresentationStorage);
};