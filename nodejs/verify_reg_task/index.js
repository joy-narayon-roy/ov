require("dotenv").config();
const express = require("express");
const morgan = require("morgan");
const db = require("./db");
const Regs = require("./app/models");
const task = require("./app/task");
const router = require("./app/router");
const { Op } = require("sequelize");

const app = express();

app.use([
  morgan("tiny"),
  express.json({ limit: "100mb" }),
  express.urlencoded({ extended: true }),
  router,
]);

const PORT = process.env.PORT || 1000;

async function main() {
  try {
    const LIMIT = process.env.MODE == "T" ? 5 : (50000*3);
    // const LIMIT = process.env.MODE == "T" ? 5 : 3830;
    const START_TASK = Number(process.env.START_TASK)
    const END_TASK = Number(process.env.END_TASK)

    const regs = await Regs.findAll({
      where: {
        checked: false,
        reg: { [Op.gte]: START_TASK, [Op.lt]: END_TASK },
      },
      limit: LIMIT,
    });
    task.begin(regs);

    console.log(`${regs.length} - Task asigned`);
  } catch (e) {
    console.log(e);
  }
}

db.sync()
  .then(async () => {
    await main();
    console.log("DB Connected");
    app.listen(PORT, (e) => {
      if (e) {
        console.log(e);
        console.log("Server start failed");
      } else {
        console.log(`http://localhost:${PORT}`);
      }
    });
  })

  .catch((e) => {
    console.log(e);
    console.log("Failed to connect db");
  });

