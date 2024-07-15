require("dotenv").config();
const express = require("express");
const morgan = require("morgan");
const db = require("./db");
const Regs = require("./app/models");
const task = require("./app/task");
const router = require("./app/router");
const { Op } = require("sequelize");

const app = express();

const PORT = process.env.PORT || 1000;

async function main() {
  try {
    const limit = process.env.TASK_LIMIT ? Number(process.env.TASK_LIMIT) : 10;
    // const LIMIT = process.env.MODE == "T" ? 5 : 50000 * 1;
    // const LIMIT = process.env.MODE == "T" ? 5 : 3830;
    // const START_TASK = Number(process.env.START_TASK);
    // const END_TASK = Number(process.env.END_TASK);

    const regs = await Regs.findAll({
      where: {
        checked: false,
        // reg: { [Op.gte]: START_TASK, [Op.lt]: END_TASK },
      },
      limit: limit,
    });
    task.begin(regs);

    console.log(`${process.env.MODE} - Mode`);
    console.log(`${regs.length} - Task asigned`);
  } catch (e) {
    console.log(e);
  }
}

app.use([
  morgan("tiny"),
  express.json(),
  express.urlencoded({ extended: true }),
]);

app.use(router);

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
