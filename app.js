// Citations: https://www.geeksforgeeks.org/steps-to-create-an-express-js-application/

import fetch from "node-fetch";
import express from 'express';

const app = express();
const PORT = process.env.PORT || 13800;

// Starting server
app.listen(PORT, (error) =>{
  console.log(`Server Running on port ${PORT}`);
});

// Middleware
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(async (req, res, next) => {
  if (process.env.FORWARDING_ADDRESS == undefined) {
    next()
  } else {
    let status = undefined
    if (req.method == 'GET') {
      const request = await fetch('http://' + process.env.FORWARDING_ADDRESS + req.url, {
        headers: {'Content-Type': 'application/json'},
        method: req.method,
      }).then((response) => {
        status = response.status
        return response.json();
      })
      return res.status(status).json(request)
    }
    else if (req.method == 'DELETE') {
      const request = await fetch('http://' + process.env.FORWARDING_ADDRESS + req.url, {
        headers: {'Content-Type': 'application/json'},
        method: req.method,
      }).then((response) => {
        status = response.status
        return response.json();
      })
      return res.status(status).json(request)
    }
    else if (req.method == 'PUT') {
      // console.log(req.body)
      const request = await fetch('http://' + process.env.FORWARDING_ADDRESS + req.url, {
        headers: {'Content-Type': 'application/json'},
        method: req.method,
        body: JSON.stringify(req.body)
        // body: JSON.stringify({key : req.body.key, val : req.body.val})
      }).then((response) => {
        status = response.status
        return response.json();
      })
      return res.status(status).json(request)
    }
  }
})


// Key value Store
const store = new Map();

// Route Get
app.get('/kvs', (req, res)=>{
  // console.log("In get")
  const key = req.query.key
  // If query parameter not there
  // console.log(key)
  if (!key) {
    // console.log("No key value found")
    return res.status(400).json({"error": "bad GET"})
  } 
  // If store does not have the key
  if (!store.has(key)) {
    // console.log("Store does not have key")
    return res.status(404).json({"error": "not found"})
  }
  // console.log("return of message")
  return res.status(200).json({"val": store.get(key)})
});

// Route for delete
app.delete('/kvs', (req, res)=>{
  const key = req.query.key
  // If query parameter not there
  if (!key) {
    return res.status(400).json({"error": "bad DELETE"})
  } 
  // If store does not have the key
  if (!store.has(key)) {
    return res.status(404).json({"error": "not found"})
  }
  const prev = store.get(key)
  store.delete(key)
  // console.log(store)
  return res.status(200).json({"prev": prev})
});


// Route for put
app.put('/kvs', (req, res)=>{
  // console.log(req.body)
  const key = req.body.key
  const val = req.body.val
  // console.log(key, val)
  // Check if request has body key and value
  if (!key || !val) {
    return res.status(400).json({"error": "bad PUT"})
  }
  // Check if key or value is proper length
  if (key.length > 200 || val.length > 200) {
    return res.status(400).json({"error": "key or val too long"})
  }
  // If new key
  if (!store.has(key)) {
    store.set(key, val)
    return res.status(201).json({"replaced": false})
  }
  // Key already exists
  const prev = store.get(key)
  store.set(key, val)
  return res.status(200).json({"replaced": true, "prev": prev})
});
