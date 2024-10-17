const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());

app.use(cors({
  origin: 'http://localhost:4200',
  methods: ['GET', 'POST'],
  credentials: true
}));


// Example API
app.get('', (req, res) => {
  res.json({ message: "Hello from Node.js!" });
});

app.get('/api/data', (req, res) => {
  res.json({ message: "Hello from Node.js!" });
});

app.post('/api/data', (req, res) => {
  const newData = req.body;
  console.log(newData);
  res.json({ message: 'Data received successfully' });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

