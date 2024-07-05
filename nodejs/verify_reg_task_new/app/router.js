const router = require("express").Router();
const task = require("./task");
const Regs = require("./models");

router.get("/v/t/next", async (req, res) => {
  try {
    const next_task = task.next();
    if (!next_task) {
      return res.status(400).json({ msg: "Task done" });
    }
    next_task.set({
      checked: true,
    });
    await next_task.save();
    res.status(200).json(next_task);
  } catch (e) {
    console.log(e);
    res.status(500).send("err");
  }
});

router.get("/v/t/all", async (req, res) => {
  try {
    const next_task = task.get_all_tasked().map((data) => data.toJSON());
    if (!next_task) {
      return res.status(400).json({ msg: "Task done" });
    }

    res.status(200).json(next_task);
  } catch (e) {
    console.log(e);
    res.status(500).send("err");
  }
});

router.get("/v/:reg", async (req, res) => {
  try {
    const { reg } = req.params;
    const reg_data = await Regs.findByPk(reg);
    if (!reg_data) {
      return res.status(200).send("OK");
    }
    reg_data.set({
      valid: true,
    });
    await reg_data.save();
    res.status(200).send(reg_data);
  } catch (e) {
    console.log(e);
    res.status(500).send("Err");
  }
});
// router.get("/", async () => {});
// router.get("/", async () => {});

module.exports = router;
