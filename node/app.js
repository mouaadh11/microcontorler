const express = require('express');
const multer = require('multer');
const app = express();
const upload = multer({ dest: 'uploads/' });

app.post('/upload_csv', upload.single('file'), (req, res) => {
  // Set the appropriate response headers
  res.header('Content-Type', 'text/csv');
  res.header('Content-Disposition', `attachment; filename=${req.file.originalname}`);

  // Process the uploaded CSV file
  // ...

  // Send a response
  res.send('File uploaded successfully');
});

app.listen(3000, () => {
  console.log('Express server is running on port 3000');
});
