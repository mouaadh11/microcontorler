// const express = require('express');
// const multer = require('multer');
 const fs = require('fs')
// const app = express();
// const upload = multer({ dest: 'uploads/' });
// app.use (express.json())
// app.post('/upload_csv', upload.single('sensor_data'), (req, res) => {
//   console.log("rani el dakhal")
//   // Set the appropriate response headers
//   // res.header('Content-Type', 'text/csv');
//   // res.header('Content-Disposition', `attachment; filename=${req.file.originalname}`);
//   console.log("csv file: ", req.body)
//   // fs.writeFile('data.csv', csvData, (err) => {
//   //   if (err) {
//   //     console.error(err);
//   //     res.status(500).send('Error saving CSV data');
//   //   }
//   // });
//   // Process the uploaded CSV file
//   // ...

//   // Send a response
//   res.send('File uploaded successfully');
// });

// app.listen(3000, () => {
//   console.log('Express server is running on port 3000');
// });
// Express.js code
var express = require('express');
var multer  = require('multer');
var upload = multer({ dest: 'uploads/' });

var app = express();
app.use (express.json())  // Middleware to parse text/plain request bodies

app.post('/upload', function (req, res) {
  fs.writeFile('./uploads/'+ req.body.file_name, req.body.file_body, function(err) {
    if(err) {
        console.log(err);
        res.status(500).send('Server error');
    } else {
        console.log("The file was saved!");
        res.send('File uploaded!');
    }
  });
});

app.listen(3000, function () {
  console.log('App listening on port 3000!');
});

