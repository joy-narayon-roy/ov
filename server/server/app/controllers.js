const { Reg, Config } = require("../models");

function create_err(msg = "Some Error") {
  const e = new Error(msg);
  e.status = 400;
  return e;
}

/**
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
async function get_regs(req, res) {
  const { limit = 100, next = 1 } = req.query;
  if (limit && next) {
    const regs = await Reg.findAll({
      where: {},
      limit,
      offset: (next - 1) * limit,
    });
    return res.status(200).json(regs);
  }
  const regs = await Reg.findAll();
  return res.status(200).json(regs);
}

/**
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
async function get_reg(req, res, next) {
  try {
    const { reg } = req.params;
    if (!reg) {
      return res.status(400).json({ msg: "Provied a valid reg no." });
    }
    const reg_data = await Reg.findByPk(reg);
    if (!reg_data) {
      return res.status(200).json({});
    }
    res.status(200).json(reg_data.toJSON());
  } catch (e) {
    console.log(e);
    next(e);
  }
}

/**
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
async function update_reg(req, res, next) {
  try {
    const { reg } = req.params;
    const { data=null, collected } = req.body;

    if (!reg) {
      return res.status(400).json({ msg: "Provied a valid reg no." });
    }
    const reg_data = await Reg.findByPk(reg);

    reg_data.set({
      data: data ?? null,
      collected: collected ? collected : data ? true : false,
    });
    await reg_data.save();
    if (!reg_data) {
      return res.status(404).json({ msg: "Not found" });
    }
    res.status(200).json(reg_data.toJSON());
  } catch (e) {
    console.log(e);
    next(e);
  }
}

/**
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
async function get_configs(req, res, next) {
  try {
    const configs = await Config.findAll();
    res.status(200).json(configs);
  } catch (e) {
    next(e);
  }
}

/**
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
async function get_config_by_id(req, res, next) {
  try {
    const { id } = req.params;
    const configs = await Config.findByPk(id.toUpperCase());
    res.status(200).json(configs);
  } catch (e) {
    next(e);
  }
}

/**
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
async function get_config_next(req, res, next) {
  try {
    const { id } = req.params;
    const config = await Config.findByPk(id.toUpperCase());
    if (!config) {
      return res.status(404).json({ msg: "Not found" });
    }
    if (config.curr < config.end) {
      config.curr++;
      await config.save();
      return res.status(200).json({ ...config.toJSON(), done: false });
    }
    res.status(400).json({ done: true });
  } catch (e) {
    next(e);
  }
}

/**
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
async function create_config(req, res, next) {
  try {
    const { id, start, curr, end } = req.body;
    if (!id || !start || !end) {
      throw create_err("Provide valid data");
    }
    const new_config = await Config.create({
      id: id.toUpperCase(),
      start,
      curr: curr ?? start,
      end,
    });

    return res.status(200).json(new_config.toJSON());
  } catch (e) {
    next(e);
  }
}

/**
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
async function add_reg(req, res, next) {
  try {
    const { reg } = req.params;
    const created = await Reg.create({
      reg: reg,
    });
    res.status(200).json(created.toJSON());
  } catch (e) {
    if (e.errors) {
      return res.status(200).json({ msg: "OK" });
    }

    next(e);
  }
}

/**
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
async function add_bulk_reg(req, res, next) {
  try {
    const { regs } = req.body;
    if (!regs) {
      throw create_err("No dataa");
    }

    const bulkCreated = await Reg.bulkCreate(regs);
    res.status(200).json(bulkCreated);
  } catch (e) {
    if (e.errors) {
      return res.status(200).json({ msg: "OK" });
    }

    next(e);
  }
}

module.exports = {
  get_regs,
  get_reg,
  update_reg,
  get_configs,
  create_config,
  get_config_by_id,
  get_config_next,
  add_reg,
  add_bulk_reg,
};
