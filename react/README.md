# Tutorial #1: How to use Docker with React + NodeJS + MongoDB

## Prerequisites:
- Install Docker from : https://www.docker.com/products/docker-desktop/
- Commands:
- To Pull/Download an image:
  ```bash
  docker pull imagename
  ```

- Run a Docker container: 
  ```bash
  docker run -d -t –name containername imagename
  ```
- See running docker containers
  ```bash
  docker ps
  ``` 
- Connect to the container shell
  ```bash
  docker exec -it containername bash
  ``` 
- To Exit shell:
  ```bash
  exit
  ```

## Step 1: Create Project Directory
```bash
mkdir development && cd development
mkdir frontend && mkdir backend
```

## Step 2: Pull the images
```bash
docker pull node
docker pull mongodb
```

## Step 3: Initialize Node.js project inside Docker containers
- Backend Initialization in development directory
  - For Linux:
  ```bash
  docker run --rm -v "$(pwd)/backend":/usr/src/app -w /usr/src/app node:18-alpine npm init -y
  ```
  - For Windows:
  ```bash
  docker run --rm -v "%cd%/backend":/usr/src/app -w /usr/src/app node:18-alpine npm init -y
  ```
- Install Express in backend:
  - For Linux:  
  ```bash
  docker run --rm -v "$(pwd)/backend":/usr/src/app -w /usr/src/app node:18-alpine npm install express
  ```
  - For Windows:
  ```bash
  docker run --rm -v "%cd%/backend":/usr/src/app -w /usr/src/app node:18-alpine npm install express
  ```
- Create React App in frontend
  - For Linux:
  ```bash
  docker run --rm -v "$(pwd)/frontend":/usr/src/app -w /usr/src/app node:18-alpine npx create-react-app .
  ```
  - For Windows:
  ```bash
  docker run --rm -v "%cd%/frontend":/usr/src/app -w /usr/src/app node:18-alpine npx create-react-app .
  ```

## Step 4: Write Application Code
- Create `backend/index.js`:
```javascript
const express = require('express');
const app = express();
const PORT = 5000;
app.get('/api', (req, res) => {
 res.send('Hello from the backend!');
});
app.get('/', (req, res) => {
 res.send('Hello from Backend');
});
app.listen(PORT, () => {
 console.log(`Backend is running on port ${PORT}`);
});
```
- Modify `frontend/src/App.js`:
```javascript
import React, { useState, useEffect } from 'react';


function App() {
 const [message, setMessage] = useState('');
 const [loading, setLoading] = useState(true);  // For loading state
 const [error, setError] = useState(null);      // For error handling


 useEffect(() => {
   fetch('http://localhost:5000')  // Fetch from backend
     .then(response => {
       if (!response.ok) {
         throw new Error('Network response was not ok');
       }
       return response.text();
     })
     .then(data => {
       setMessage(data);
       setLoading(false);  // Data loaded successfully
     })
     .catch(error => {
       setError(error.message);
       setLoading(false);  // Error occurred, stop loading
     });
 }, []);


 if (loading) {
   return <div>Loading...</div>;
 }
if (error) {
   return <div>Error: {error}</div>;
 }


 return (
   <div className="App">
     <h1>{message}</h1>
   </div>
 );
}
export default App;
```
- Add a proxy setting to `frontend/package.json`:
```json
"proxy": "http://backend:5000",
```

## Step 5: Docker Setup
- Create `backend/dockerfile`:
```dockerfile
FROM node:18-alpine


WORKDIR /usr/src/app


COPY package*.json ./
RUN npm install


COPY . .


EXPOSE 5000


CMD ["node", "index.js"]
```
- Create `frontend/Dockerfile`:
```dockerfile
FROM node:14-alpine


WORKDIR /usr/src/app


COPY package*.json ./
RUN npm install


COPY . .


EXPOSE 3000


CMD ["npm", "start"]
```
- Create `development/docker-compose.yml`:
```yml
services:
 backend:
   build: ./backend
   ports:
     - '5000:5000'
   volumes:
     - ./backend:/usr/src/app
     - /usr/src/app/node_modules
   networks:
     - app-network


 frontend:
   build: ./frontend
   ports:
     - '3000:3000'
   volumes:
     - ./frontend:/usr/src/app
     - /usr/src/app/node_modules
   depends_on:
     - backend
   networks:
     - app-network


networks:
 app-network:
   driver: bridge
```
- Now, inside `development` directory, build the Docker images for both services by running: 
```bash
docker-compose up --build
```
- To exit you can `Ctrl + C`


## Step 6: Test Backend + Frontend locally
- Visit [http://localhost:5000/api](http://localhost:5000/api) to confirm the backend is working
- Visit [http://localhost:3000](http://localhost:3000) to confirm the frontend is working

Note: the text has been modified with h1 heading!



## Congratluations, you are now fetching data from the backend


