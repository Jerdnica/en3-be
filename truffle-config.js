const HDWalletProvider = require('@truffle/hdwallet-provider');
const fs = require('fs');
const mnemonic = fs.readFileSync(".secret").toString().trim();

module.exports = {
  networks: {
    bscTestnet: {
      provider: () => new HDWalletProvider(mnemonic, `https://data-seed-prebsc-1-s1.binance.org:8545`),
      network_id: 97,
      gas: 8000000, // Increase gas limit
      gasPrice: 10e9, // 10 Gwei
      confirmations: 5,
      timeoutBlocks: 50, // Increase timeout blocks
      networkCheckTimeout: 1000000, // Increase network check timeout
      skipDryRun: true
    }
  },
  compilers: {
    solc: {
      version: "0.8.20"
    }
  }
};