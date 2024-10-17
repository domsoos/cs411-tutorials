// backend/index.js

//import express from 'express';

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

