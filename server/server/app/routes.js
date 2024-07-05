const router = require("express").Router();
const controller = require("./controllers");

router.get("/config/:id/next", controller.get_config_next);
router.get("/config/:id", controller.get_config_by_id);
router.post("/config", controller.create_config);
router.get("/configs", controller.get_configs);

// Regs
router.get("/regs", controller.get_regs);
router.get("/reg/:reg", controller.get_reg)
router.patch("/reg/:reg", controller.update_reg)
router.post("/reg/:reg", controller.add_reg);
// router.post("/regs", controller.add_bulk_reg);

module.exports = router;
