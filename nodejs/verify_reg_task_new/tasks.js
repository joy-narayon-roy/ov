const sqlite3 = require("sqlite3");
const { open } = require("sqlite");

class Task {
  #load_task_sql;
  #checked_sql;
  constructor(limit = 10, cash_limit = 5, regs = []) {
    this.regs = regs;
    this.index = 0;
    this.begined = false;
    this.limit = limit;
    this.cash_limit = cash_limit;
    this.checked_cash = [];
    this.db = open({
      filename: "./db/test.db",
      driver: sqlite3.Database,
    });
    this.#load_task_sql = `SELECT * FROM Regs WHERE checked = 0 LIMIT ${this.limit}`;
  }

  async begin() {
    const db = await this.db;
    this.index = 0;
    this.regs = await db.all(this.#load_task_sql);
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
    const checked = this.checked_cash
      .filter((d) => d)
      .map((d) => d.reg)
      .join(",");
    const db = await this.db;
    await db.run(`UPDATE Regs SET checked = 1 WHERE reg IN(${checked})`);
    this.checked_cash = [];
    this.checked_cash.push(reg);
    return true;
  }

  async next() {
    const data = this.regs[this.index];
    this.index += 1;
    const updated = await this.update_checked(data);
    // console.log(updated);
    if (this.index > this.limit) {
      return null;
    }
    data.checked = 1;
    return data;
  }

  async this_is_valid(reg) {
    if (!reg) return null;
    const f = this.regs.find((item) => item.reg == reg);
    if (f) {
      f.valid = 1;
    }
    await (await this.db).run(`UPDATE Regs SET checked = 1 WHERE reg = ${reg}`);
    return f;
  }

  async db_close() {
    (await this.db).close();
  }
}
module.exports = Task;
