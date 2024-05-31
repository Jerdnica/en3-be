const HDWalletProvider = require('@truffle/hdwallet-provider');
const fs = require('fs');
const mnemonic = fs.readFileSync(".secret").toString().trim();

module.exports = {
  networks: {
    bsc: {
      provider: () => new HDWalletProvider(mnemonic, `https://bsc-dataseed.binance.org/`),
      network_id: 56,       // BSC Mainnet ID
      confirmations: 10,    // # of confs to wait between deployments. (default: 0)
      timeoutBlocks: 200,  // # of blocks before a deployment times out  (minimum/default: 50)
      skipDryRun: true     // Skip dry run before migrations? (default: false for public nets )
    },
  },
  compilers: {
    solc: {
      version: "0.8.0",
    },
  },
};
