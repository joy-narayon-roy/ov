class Task {
  constructor(regs = []) {
    this.regs = regs;
    this.index = 0;
    this.begined = false;
  }

  begin(regs = []) {
    this.regs = regs;
    this.index = 0;
    this.begined = true;
  }

  get_all_tasked() {
    return this.regs;
  }

  get_curr() {
    return this.regs[this.index];
  }

  next() {
    const data = this.regs[this.index];
    this.index += 1;
    return data;
  }
}

const task = new Task();

module.exports = task;
