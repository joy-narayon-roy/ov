const { DataTypes } = require("sequelize");
const sequelize = require("../db"); // Adjust the path as needed

const Regs = sequelize.define(
  "Regs",
  {
    reg: {
      type: DataTypes.INTEGER,
      allowNull: false,
      primaryKey: true,
    },
    checked: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    valid: {
      type: DataTypes.BOOLEAN,
      defaultValue: false,
    },
    rawdata: {
      type: DataTypes.JSON,
      defaultValue: null,
    },
  },
  {
    tableName: "Regs", // Explicitly specify the table name to match your database
    timestamps: false, // Disable automatic `createdAt` and `updatedAt` fields
  }
);

module.exports = Regs;
