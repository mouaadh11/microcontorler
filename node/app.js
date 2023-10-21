const express = require("express");
const bodyParser = require("body-parser");

const app = express();
const port = 3000; // Use your desired port

app.use(bodyParser.json());

app.post("/data", (req, res) => {
  const data = req.body;
  console.log("Received data:", data);

  // Process and save the data as needed

  res.status(200).send("Data received successfully");
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});