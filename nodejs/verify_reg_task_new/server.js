require("dotenv").config();
const express = require("express");
const morgan = require("morgan");
const tasks = require("./tasks");

const { Mutex } = require("async-mutex");
const mutex = new Mutex();

const app = express();
app.use([
  global_error,
  express.json({ limit: "100mb" }),
  express.text(),
  express.urlencoded({ extended: true }),
  morgan("dev"),
]);

function create_err(status, msg) {
  const err = new Error(msg);
  err.status = status;
  return err;
}

app.get("/health", (req, res) => {
  return res.status(200).json({ msg: "All Ok", ok: true });
});

app.get("/t/all", async (req, res, next) => {
  try {
    const all_tasks = tasks.get_all_tasked();
    return res.status(200).json(all_tasks);
  } catch (e) {
    next(e);
  }
});

// app.get("/t/next", async (req, res, next) => {
//   try {
//     const curr_task = await tasks.next();
//     if (!curr_task) {
//       throw create_err(400, "Tasks checked");
//     }
//     return res.status(200).json(curr_task);
//   } catch (e) {
//     next(e);
//   }
// });


app.get("/t/next", async (req, res) => {
  const release = await mutex.acquire();
  try {
    const db = await tasks.db;
    let reg = await db.all(`SELECT reg FROM Regs WHERE checked = 0 LIMIT 1`);

    if (reg.length < 1) {
      return res.status(400).send("No reg found");
    }

    reg = reg[0].reg;

    // Update using parameterized query to prevent SQL injection
    await db.exec(`UPDATE Regs SET checked = 1 WHERE reg = ?`, [reg]);

    res.status(200).send(`${reg}`);
  } catch (error) {
    console.error("Error processing request:", error);
    res.status(500).send("Internal Server Error");
  } finally {
    release();
  }
});

app.get("/t/v/:reg/:ind", async (req, res, next) => {
  try {
    const { reg, ind } = req.params;
    const v = await tasks.this_is_valid(reg, ind, null);
    return res.status(200).send(v);
  } catch (e) {
    next(e);
  }
});

app.post("/run/exe", async (req, res) => {
  try {
    const { sql_str } = req.body;
    if (!sql_str) {
      return res.status(400).send("Provide valid sql str");
    }
    const db = await tasks.db;
    const db_res = await db.all(sql_str);
    res.status(200).json(db_res);
  } catch (e) {
    res.status(500).send("server error");
    console.log(e);
  }
});

function global_error(err, req, res, next) {
  if (err.status) {
    return res.status(err.status).send(err.message);
  } else {
    console.log(err);
    return res.status(500).send("Server Error.");
  }
}

const {
  PORT = 1000,
  TASK_LIMIT = 5,
  CASH_LIMIT = 5,
  START = false,
  END = false,
} = process.env;

tasks.begin(TASK_LIMIT, CASH_LIMIT, START, END).then(() => {
  console.log(tasks.get_all_tasked().length, "Tasks loaded.");
  console.log("Mode", process.env.MODE);
  app.listen(PORT, (err) => {
    if (err) {
      print(err);
      console.log(err);
      console.log(`Server failed`);
    } else {
      console.log(`Server started http://localhost:${PORT}`);
    }
  });
});

process.on("SIGINT", async () => {
  console.log("Bye");
  await tasks.db_close();
  process.exit(1);
});
