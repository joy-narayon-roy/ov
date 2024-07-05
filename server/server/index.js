const express = require("express");
const app = express();
const cors = require("cors");
const logger = require("morgan");
const db = require("./db");

const routes = require("./app/routes");

app.use([
  cors(),
  express.json({ limit: "500mb" }),
  express.urlencoded({ extended: true }),
  logger("dev"),
]);

app.use(routes);

app.use((err, req, res, next) => {
  if (err.status) {
    res.status(500).json({
      msg: err.message,
    });
  } else {
    // console.log(err);
    console.log(err.message);
    res.status(500).json({ msg: err.message ?? "Error" });
  }
});

db.sync()
  .then(() => {
    console.log("DB Connected");
    app.listen(8080, (err) => {
      if (err) {
        console.log(err);
        console.log("Server error");
      } else {
        console.log("http://localhost:8080");
      }
    });
  })
  .catch((e) => {
    console.log(e);
    console.log("DB Error");
  });
