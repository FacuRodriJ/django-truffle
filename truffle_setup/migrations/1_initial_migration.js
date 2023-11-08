const DocumentHashStorage = artifacts.require("DocumentHashStorage");

module.exports = function (deployer) {
    deployer.deploy(DocumentHashStorage);
};