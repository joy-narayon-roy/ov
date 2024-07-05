const express = require("express");
require("dotenv").config();
const morgan = require("morgan");
const Task = require("./tasks");
const app = express();
const task = new Task();
// app.task = task;

function create_err(status, msg) {
  const err = new Error(msg);
  err.status = status;
  return err;
}

app.get("/health", (req, res) => {
  res.status(200).json({ msg: "All Ok", ok: true });
});

app.get("/t/all", async (req, res) => {
  try {
    const tasks = task.get_all_tasked();
    return res.status(200).json(tasks);
  } catch (e) {
    next(e);
  }
});

app.get("/t/next", async (req, res, next) => {
  try {
    const curr_task = await task.next();
    if (!curr_task) {
      throw create_err(400, "Tasks checked");
    }
    return res.status(200).send(`${curr_task.reg}`);
  } catch (e) {
    next(e);
  }
});

app.get("/t/v/:reg", async (req, res, next) => {
  try {
    const { reg } = req.params;
    const v = await task.this_is_valid(reg);
    res.status(200).send(v);
    console.log(v);
  } catch (e) {
    next(e);
  }
});

app.use([morgan("tiny"), express.json(), express.urlencoded()]);
app.use((err, req, res, next) => {
  if (err.status) {
    res.status(err.status).send(err.message);
  } else {
    res.status(500).send("Server error.");
  }

  console.log(err);
});
const PORT = process.env.PORT || 2000;

task
  .begin()
  .then(() => {
    app.listen(PORT, (err) => {
      if (err) {
        console.log(err);
        console.log("Server Error");
      } else {
        console.log(`Server start http://localhost:${PORT}`);
        console.log(`Server start http://localhost:${PORT}/health`);
        console.log(`Server start http://localhost:${PORT}/alltask`);
        console.log(`Server start http://localhost:${PORT}/t/next`);
      }
    });
  })
  .catch(() => {
    console.log("Tasked failed");
  });

process.on("SIGINT", () => {
  console.log("Received SIGINT. Exiting gracefully...");
  process.exit(0);
});
