const { DataTypes } = require("sequelize");
const db = require("../db");

const Reg = db.define(
  "Regs",
  {
    reg: {
      type: DataTypes.NUMBER,
      primaryKey: true,
      allowNull: false,
    },
    data: {
      type: DataTypes.JSON,
      allowNull: true,
      defaultValue: null,
    },
    collected: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
  },
  {
    createdAt: false,
    updatedAt: false,
  }
);

const Config = db.define(
  "Config",
  {
    id: {
      type: DataTypes.STRING,
      allowNull: false,
      primaryKey: true,
    },
    start: {
      type: DataTypes.NUMBER,
      allowNull: false,
    },
    curr: {
      type: DataTypes.NUMBER,
      allowNull: false,
    },
    end: {
      type: DataTypes.NUMBER,
      allowNull: false,
    },
  },
  {
    createdAt: false,
    updatedAt: false,
  }
);

module.exports = {
  Reg,
  Config,
};
