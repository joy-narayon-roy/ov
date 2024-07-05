const mongoose = require("mongoose");
const Valide = mongoose.model("Valide", new mongoose.Schema({ _id: Number }));
async function main() {}

mongoose
  .connect("mongodb+srv://yeti:demoyeti420@main.i6nm9j1.mongodb.net/nu_verifiy")
  .then(async () => {
    await main();
  })
  .catch((e) => {
    console.log(e);
  })
  .finally(() => mongoose.connection.close());
