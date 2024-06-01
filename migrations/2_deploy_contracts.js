const MyNFT = artifacts.require("MyNFT");

module.exports = function (deployer) {
  const name = "DynamicCollectionName"; // Replace with your desired collection name
  const symbol = "DCN"; // Replace with your desired collection symbol
  deployer.deploy(MyNFT, name, symbol);
};
