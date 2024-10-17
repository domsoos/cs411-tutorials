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


# Database Development using MongoDB with Docker
## Step 1: Install `mongodb` package in `development` directory:
- For Linux:
```bash
docker run --rm -v "$(pwd)/backend":/usr/src/app -w /usr/src/app node:14-alpine npm install mongodb
```
- For Windows:
```bash
docker run --rm -v "%cd%/backend":/usr/src/app -w /usr/src/app node:14-alpine npm install mongodb
```
## Step 2: Install axios packages in development directory:
- For Linux:
```bash
docker run --rm -v "$(pwd)/frontend":/usr/src/app -w /usr/src/app node:14-alpine npm install axios
```
- For Windows:
```bash
docker run --rm -v "%cd%/frontend":/usr/src/app -w /usr/src/app node:14-alpine npm install axios
```

## Step 3: Add MongoDB service in `docker-compose.yml`
- Add the db service as dependency, make sure the backend service looks like this:
```yml
services:
 backend:
   build: ./backend
   ports:
     - '5000:5000'
   depends_on:
     - db
   networks:
     - app-network
```
- Replace the following:
```yml
networks:
 app-network:
   driver: bridge  
```
- with:
```yml
db:
   image: mongo:4.4
   ports:
     - '27017:27017'
   volumes:
     - mongo-data:/data/db
   networks:
     - app-network

networks:
 app-network:
   driver: bridge

volumes:
 mongo-data:
```

## Step 4: MongoDB dependency + adding proxy
- The `frontend/package.json` should look like this:
```json
 "dependencies": {
   "@testing-library/jest-dom": "^5.17.0",
   "@testing-library/react": "^13.4.0",
   "@testing-library/user-event": "^13.5.0",
   "axios": "^1.7.7",
   "react": "^18.3.1",
   "react-dom": "^18.3.1",
   "react-scripts": "5.0.1",
   "web-vitals": "^2.1.4",
   "mongodb": "^6.9.0" // add this line
 },
 "proxy": "http://backend:5000",
```

## Step 5: Update the backend code
- In `backend/index.js` to use MongoDB:
```javascript
const express = require('express');
const { MongoClient } = require('mongodb');
const app = express();
const port = 5000;


const mongoURL = 'mongodb://db:27017';
const client = new MongoClient(mongoURL);


app.get('/', (req, res) => {
 res.send('Hello from Backend');
});


app.get('/api', async (req, res) => {
 try {
   await client.connect();
   const database = client.db('testdb');
   const collection = database.collection('testcol');


   const doc = { message: 'Hello from MongoDB!' };
   await collection.insertOne(doc);


   const result = await collection.findOne(doc);
   res.send(result.message);
 } catch (err) {
   console.error(err);
   res.status(500).send('Error connecting to database');
 } finally {
   await client.close();
 }
});


app.listen(port, () => {
 console.log(`Backend server is running on port ${port}`);
});
```

- Add a `.gitignore` file in the `backend` directory:
```gitignore
node_modules
Npm-debug.log
```

## Step 6: Rebuild Docker containers
- In `development` directory execute:
```bash
docker-compose down
docker-compose up -–build
```

## Step 7: Verify connectivity between Frontend and Backend
- Enter the frontend container’s shell:
  ```bash
  docker-compose exec frontend sh
  ```
- Quickly install curl
  ```bash
  apk add curl
  ```
- Use curl to test the connection to the backend:
  ```bash
  curl http://backend:5000/api
  ```
- Should display the string: Hello from MongoDB!
  ```bash
  exit
  ```
## Step 8: Test the application
- Access the frontend by visiting  [http://localhost:3000](http://localhost:3000) or [http://localhost:3000/api](http://localhost:3000/api) to see:

- Access the backend:
  - Notice the difference between different paths:
  - Visit [http://localhost:5000/](http://localhost:5000/) to view:

  
  - Visit [http://localhost:5000/api](http://localhost:5000/api) to view:


## Congratulations! You are now fetching data using MongoDB and displaying it in the front end!





