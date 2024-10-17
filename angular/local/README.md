# Tutorial #2.1: Local Angular, NodeJS with MongoDB

- Prereqs:
  - Make sure npm && node is installed:
  ```bash
  brew install npm
  brew install node
  ```
## Step 1: Create Project Directory
```bash
mkdir development && cd development
```  

## Step 2: Backend NodeJS with Express and CORS
- Initialize NodeJS Project:
```bash
mkdir backend && cd backend
npm init -y
```
- Install dependencies
```bash
npm install express cors body-parses mongoose
```

## Step 3: Create the Express server
- Create file named server.js in the *backend* folder

```javascript
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());

app.get('', (req, res) => {
  res.json({ message: "Hello from Node.js!" });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
```

## Step 4

