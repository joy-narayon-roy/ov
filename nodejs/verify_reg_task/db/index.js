const { Sequelize } = require("sequelize");

const DB_PATH = "./db/ov_reg_rendom.db";
const TEST_DB_PATH = "./db/test.db";

const db = new Sequelize({
  dialect: "sqlite",
  storage: process.env.MODE == "T" ? TEST_DB_PATH : DB_PATH,
  logging: false,
});

module.exports = db;
