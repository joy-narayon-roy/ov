const sqlite3 = require("sqlite3");
const { open } = require("sqlite");

class Task {
  constructor(limit = 10, cash_limit = 5, regs = []) {
    this.regs = regs;
    this.index = 0;
    this.begined = false;
    this.limit = limit;
    this.cash_limit = cash_limit;
    this.checked_cash = [];
    this.db_path =
      process.env.MODE == "T" ? "./db/test.db" : "./db/ov_reg_rendom.db";
    this.db = open({
      filename: this.db_path,
      driver: sqlite3.Database,
    });
  }

  async begin(limit = 10, cash_limit = 5, start = false, end = false) {
    const db = await this.db;
    this.limit = limit;
    this.cash_limit = cash_limit;
    this.index = 0;
    this.regs = await db.all(
      `SELECT reg,checked,valid FROM Regs WHERE checked = 0 LIMIT ${this.limit}`
    );
    console.log(`DB Path : ${this.db_path}`);
    this.begined = true;
  }

  get_all_tasked() {
    return this.regs;
  }

  get_curr() {
    return this.regs[this.index];
  }

  async update_checked(reg) {
    if (this.checked_cash.length < this.cash_limit) {
      this.checked_cash.push(reg);
      return false;
    }
    const checked_arr = this.checked_cash.filter((d) => d).map((d) => d.reg);
    const checked = checked_arr.join(",");
    const db = await this.db;
    await db.run(`UPDATE Regs SET checked = 1 WHERE reg IN(${checked})`);
    console.log(checked_arr);
    this.checked_cash = [];
    this.checked_cash.push(reg);
    return true;
  }

  async next() {
    const data = this.regs[this.index];
    if (!data) {
      return null;
    }
    data.index = this.index;
    this.index += 1;
    const updated = await this.update_checked(data);
    // console.log(updated);
    if (this.index > this.limit) {
      return null;
    }
    data.checked = 1;
    return data;
  }

  async this_is_valid(reg, ind, rawdata = null) {
    if (!reg) return null;
    let f;
    if (!ind) {
      f = this.regs.find((item) => item.reg == reg);
    } else {
      f = this.regs[ind];
      if (f.reg != reg) {
        const err = new Error(
          `Index not matched.\n reg = ${reg}\n ${ind}. reg = ${f.reg}`
        );
        err.status = 400;
        throw err;
      }
    }
    if (f) {
      f.valid = 1;
    }
    if (rawdata) {
      await (
        await this.db
      ).run(
        `UPDATE Regs SET checked = 1,valid = 1 AND rawdata = ${rawdata} WHERE reg = ${reg}`
      );
      return f;
    }

    await (
      await this.db
    ).exec(`UPDATE Regs SET checked = 1,valid = 1 WHERE reg = ${reg}`);
    return f;
  }

  async db_close() {
    const checked = this.checked_cash
      .filter((d) => d)
      .map((d) => d.reg)
      .join(",");
    const db = await this.db;
    await db.run(`UPDATE Regs SET checked = 1 WHERE reg IN(${checked})`);
    // console.log(this.checked_cash);
    await db.close();
    (await this.db).close();
  }
}
const tasks = new Task();
module.exports = tasks;
