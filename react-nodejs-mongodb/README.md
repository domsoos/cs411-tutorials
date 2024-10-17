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
