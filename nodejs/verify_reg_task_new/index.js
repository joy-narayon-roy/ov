const express = require("express");
const sqlite3 = require("sqlite3").verbose();

const app = express();
const port = 3000;

app.use([express.json(), express.urlencoded({ extends: true })]);

// Connect to SQLite database
const db = new sqlite3.Database("./db/test.db", (err) => {
  if (err) {
    console.error(err.message);
  } else {
    console.log("Connected to the SQLite database.");
  }
});

// Create users table
db.run(`CREATE TABLE IF NOT EXISTS "Regs" (
	"reg"	INTEGER NOT NULL,
	"checked"	BOOLEAN DEFAULT 0,
	"valid"	BOOLEAN DEFAULT 0,
	"rawdata"	TEXT DEFAULT NULL,
	PRIMARY KEY("reg")
)`);

// CRUD routes

// Create a new user
app.post("/users", (req, res) => {
  const { name, email } = req.body;
  db.run(
    `INSERT INTO users (name, email) VALUES (?, ?)`,
    [name, email],
    function (err) {
      if (err) {
        res.status(400).json({ error: err.message });
      } else {
        res.json({ id: this.lastID });
      }
    }
  );
});

// Read all users
app.get("/regs", (req, res) => {
  db.all(`SELECT * FROM users`, [], (err, rows) => {
    if (err) {
      res.status(400).json({ error: err.message });
    } else {
      res.json({ users: rows });
    }
  });
});

// Read a single user by ID
app.get("/users/:id", (req, res) => {
  const { id } = req.params;
  db.get(`SELECT * FROM users WHERE id = ?`, [id], (err, row) => {
    if (err) {
      res.status(400).json({ error: err.message });
    } else {
      res.json({ user: row });
    }
  });
});

// Update a user
app.put("/users/:id", (req, res) => {
  const { id } = req.params;
  const { name, email } = req.body;
  db.run(
    `UPDATE users SET name = ?, email = ? WHERE id = ?`,
    [name, email, id],
    function (err) {
      if (err) {
        res.status(400).json({ error: err.message });
      } else {
        res.json({ updated: this.changes });
      }
    }
  );
});

// Delete a user
app.delete("/users/:id", (req, res) => {
  const { id } = req.params;
  db.run(`DELETE FROM users WHERE id = ?`, [id], function (err) {
    if (err) {
      res.status(400).json({ error: err.message });
    } else {
      res.json({ deleted: this.changes });
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});

// Close the database connection when the Node process ends
process.on("SIGINT", () => {
  db.close((err) => {
    if (err) {
      console.error(err.message);
    }
    console.log("Closed the database connection.");
    process.exit(0);
  });
});
