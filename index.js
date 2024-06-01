const express = require('express');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const { ethers } = require('ethers');
const cors = require('cors');
require('dotenv').config();
const app = express();


app.use(bodyParser.json());
app.use(cors({
  origin: 'http://localhost:5174/',
  credentials: true
}));

console.log(process.env.metamask_seed);

const JWT_SECRET = 'my_jwt_secret_lmao';
const nonces = {};

app.post('/nonce', (req, res) => {
  console.log('lol')
  const { address } = req.body;
  const nonce = `Sign this message to log in: ${Date.now()}`;
  nonces[address] = nonce;
  res.json({ nonce });
});

app.post('/auth', async (req, res) => {
  console.log(req.body);
  const { address, message, signature } = req.body;
  const nonce = nonces[address];
  if (message !== nonce) {
    return res.status(400).send('Invalid nonce');
  }
  try {
    const signerAddress = ethers.verifyMessage(message, signature);
    if (signerAddress.toLowerCase() === address.toLowerCase()) {
      const token = jwt.sign({ address }, JWT_SECRET, { expiresIn: '1h' });
      delete nonces[address];
      res.json({ token });
    } else {
      res.status(401).send('Signature verification failed');
    }
  } catch (error) {
    res.status(500).send('Server error');
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
