// require("dotenv").config();
const express = require("express");
const morgan = require("morgan");
const { Sequelize, DataTypes, Model } = require("sequelize");

const DB_PATH = "./db/regs.db";
const TASK_LIMIT = 50000;

// const DB_PATH = "./db/test.db";
// const TASK_LIMIT = 10;

const sequelize = new Sequelize("database", "username", "password", {
  dialect: "sqlite",
  storage: DB_PATH,
  logging: false,
});

class Regs extends Model {}

Regs.init(
  {
    reg: {
      type: DataTypes.INTEGER,
      allowNull: false,
      unique: true,
      primaryKey: true,
    },
    data: {
      type: DataTypes.JSON,
      defaultValue: null,
    },
    collected: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
    },
  },
  {
    sequelize,
    modelName: "Regs",
    tableName: "Regs",
    timestamps: false,
  }
);

const app = express();

class Tasks {
  constructor(limit) {
    this.all = [];
    this.count = 0;
    this.limit = limit;
  }
  async begin() {
    this.all = await Regs.findAll({
      where: {
        collected: false,
      },
      limit: this.limit,
    });
  }

  async next() {
    const last = this.all[this.count];
    const index = this.count;
    this.count++;
    if (this.count > this.limit) {
      return null;
    }
    last.set("collected", true);
    await last.save();
    return [last.reg, index];
  }

  toJSON() {
    return this.all;
  }
}

const tasks = new Tasks(TASK_LIMIT);

app.use([
  morgan("dev"),
  express.urlencoded({ extends: true, limit: "500mb" }),
  express.json({ limit: "500mb" }),
]);

app.get("/", async (req, res) => {
  try {
    res.status(200).json(tasks.toJSON());
  } catch (e) {
    console.log(e);
    res.status(400).send("WTF");
  }
});

app.get("/ok", (req, res) => {
  res.status(200).json({ state: true, msg: "ALL OK" });
});

app.get("/c/n", async (req, res) => {
  const next = await tasks.next();
  if (next) {
    return res.status(200).send(`${next[0]}, ${next[1]}`);
  }
  res.status(400).json(null);
});

app.post("/v/:reg/:index", async (req, res) => {
  const { reg, index } = req.params;
  const { data } = req.body;

  if (!req) {
    return res.status(400).json(null);
  }

  const reg_data = await Regs.findByPk(reg);
  if (!reg_data) {
    return res.status(400).send(`${reg}`);
  }
  tasks.all[Number(index)].data = data;
  reg_data.set("data", data);
  await reg_data.save();
  res.status(200).json(reg_data);
});

const PORT = 8200;

sequelize
  .sync()
  .then(async () => {
    console.log("DB Connected");

    await tasks.begin();
    console.log(tasks.all.length, "Task loaded");
    app.listen(PORT, (err) => {
      if (err) {
        console.log(err);
        console.log("Server failed.");
      } else {
        console.log(`http://localhost:${PORT}`);
      }
    });
  })
  .catch((e) => {
    console.log(e);
    console.log("Faild to connecte DB");
  });
