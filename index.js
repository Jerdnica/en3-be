const express = require('express');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const { ethers } = require('ethers');
const cors = require('cors');
const mysql = require('mysql2');
const { exec } = require('child_process');


require('dotenv').config();
const app = express();

const verifyToken = (req, res, next) => {
  const token = req.headers['authorization'];

  if (!token) {
    return res.status(403).json({ success: false, message: 'No token provided' });
  }

  jwt.verify(token, process.env.jwt_secret, (err, decoded) => {
    if (err) {
      return res.status(500).json({ success: false, message: 'Failed to authenticate token' });
    }
    
    req.userAddress = decoded.address;
    next();
  });
};

const formatDate = (timestamp) => {
  const date = new Date(timestamp);
  const yyyy = date.getFullYear();
  const mm = String(date.getMonth() + 1).padStart(2, '0');
  const dd = String(date.getDate()).padStart(2, '0');
  const hh = String(date.getHours()).padStart(2, '0');
  const min = String(date.getMinutes()).padStart(2, '0');
  const ss = String(date.getSeconds()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd} ${hh}:${min}:${ss}`;
};

const connection = mysql.createConnection({
  host: process.env.db_host, 
  user: process.env.db_user,
  password: process.env.db_password,
  database: process.env.db_database
});
connection.connect((err) => {
  if (err) throw err;
  console.log('Connected to the MySQL server.');
});

app.use(bodyParser.json());
app.use(cors({
  origin: 'http://localhost:5174/',
  credentials: true
}));

const nonces = {};

const createSmartContract = (ipfsUrl, title, amountNft, pricePerNft, donationAddr, donatationPercentage) => {
  // TODO

  return 'contract_adddrrrr';
}

app.post('/nonce', (req, res) => {
  console.log('lol')
  const { address } = req.body;
  const nonce = `Sign this message to log in: ${Date.now()}`;
  nonces[address] = nonce;
  res.json({ nonce });
});

app.post('/auth', async (req, res) => {
  const { address, message, signature } = req.body;
  const nonce = nonces[address];
  if (message !== nonce) {
    return res.status(400).send('Invalid nonce');
  }
  try {
    const signerAddress = ethers.verifyMessage(message, signature);
    if (signerAddress.toLowerCase() === address.toLowerCase()) {
      const token = jwt.sign({ address }, process.env.jwt_secret, { expiresIn: '1h' });
      delete nonces[address];
      res.json({ token });
    } else {
      res.status(401).send('Signature verification failed');
    }
  } catch (error) {
    res.status(500).send('Server error');
  }
});

app.post('/generate-image', verifyToken, async (req, res) => {
  const {
    description, 
    name, 
    location
  } = req.body;
  const pythonCommand = `./0_make_nft.py "#ff5733" "${location}" "${name}" "${description}" "sample.png"`;
  const activateEnvCommand = 'source path/to/your/env/bin/activate';
  const command = `${activateEnvCommand} && ${pythonCommand}`;

  exec(command, (error, stdout, stderr) => {
    if (error) {
        console.error(`Error executing command: ${error}`);
        return;
    }
    console.log(`stdout: ${stdout}`);
    console.error(`stderr: ${stderr}`);
  });
});


app.post('/create-event', verifyToken, async (req, res) => {
  const {
    description, 
    name, 
    startDate, 
    endDate, 
    location, 
    capacity,
    price,
    donationAddr,
    donatationPercentage,
    image,
    userAddress
  } = req.body;

  const contractAddr = createSmartContract('ipfsUrl', 'title', 'amountNft', 'pricePerNft', 'donationAddr', 'donatationPercentage');
  
  const query = `
    INSERT INTO events (
      owner_addr, contract_addr, description, name, start_date, end_date, location, capacity, price, donation_addr, donation_percentage, image
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
  `;

  const values = [
    userAddress, 
    contractAddr, 
    description, 
    name, 
    formatDate(startDate), 
    formatDate(endDate), 
    location, 
    capacity,
    price,
    donationAddr,
    donatationPercentage,
    image
  ];

  
    // ./0_upload_ipfs.py "Global, Worldwide" "The Great Meme Contest: " "We cordially invite you to part!" "./sample_images/output_nft_image.png"
    // `NAME="${name}" truffle compile' 
    // truffle console --network bscTestnet

    //let instance = await MyNFT.deployed();
    //let accounts = await web3.eth.getAccounts();

    //# Base URI, Total NFTs, Price per mint, Donation address, Donation percentage
    //let collectionId = await instance.createNFTCollection( "ipfs://QmPPWbX4H9xUcJWnNzKpV1Br5F4DLuv1bDmTQNZy2X5bUE/", 5, web3.utils.toWei('0.01', 'ether'), "0x142f9DE19A405a1E8B6b71811414110b33998b88", 50);

    //await instance.mintNFT(collectionId.logs[0].args.tokenId, { from: accounts[0], value: web3.utils.toWei('0.01', 'ether') });

  
  connection.query(query, values, (err, results) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ success: false, message: 'Database query failed' });
    }
    res.status(200).json({ success: true, message: 'Event created successfully' });
  });
});

app.get('/events', (req, res) => {
  const query = 'SELECT * FROM events';
  connection.query(query, (err, results) => {
    if (err) {
      console.error(err);
      return res.status(500).json({ success: false, message: 'Database query failed' });
    }
    res.status(200).json({ success: true, events: results });
  });
});

app.post('/join-event', verifyToken, (req, res) => {
  const {
    userAddress, 
    eventId
  } = req.body;
  // TODO: write to table user_events user_addr ;
});



const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
