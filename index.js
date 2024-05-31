const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Hello, World!');
});

app.post('/events', (req, res) => {
  const event = req.body;
  res.status(201).send(`Event created with name: ${event.name}`);
});

app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
