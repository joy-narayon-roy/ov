const { DataTypes } = require("sequelize");
const db = require("../db");
const Reg = db.define("Reg", {
  reg: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    allowNull: false,
  },
  data: {
    type: DataTypes.JSON,
    allowNull: true,
    defaultValue: null,
  },
});

module.exports = Reg;
