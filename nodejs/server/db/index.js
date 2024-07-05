const { Sequelize } = require("sequelize");

const DB_PATH = "./db/database.db";
const DB_TEST_PATH = "./db/test.db";

const db = new Sequelize({
  dialect: "sqlite",
  storage: DB_TEST_PATH,
  logging: false,
});

module.exports = db;
