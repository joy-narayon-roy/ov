const express = require('express');
const sqlite = require('sqlite');
const sqlite3 = require('sqlite3');

const app = express();
const port = 3000;

// Middleware to parse JSON bodies
app.use(express.json());

let db;

(async () => {
  try {
    // Open a database connection
    db = await sqlite.open({ filename: 'my-database.db', driver: sqlite3.Database });

    // Create a table
    await db.exec(`CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      email TEXT
    )`);

    // Start the Express server
    app.listen(port, () => {
      console.log(`Server is running on http://localhost:${port}`);
    });

  } catch (err) {
    console.error(err.message);
  }
})();

// Endpoint to get all users
app.get('/users', async (req, res) => {
  try {
    const users = await db.all('SELECT * FROM users');
    res.json(users);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Endpoint to get a user by ID
app.get('/users/:id', async (req, res) => {
  try {
    const user = await db.get('SELECT * FROM users WHERE id = ?', [req.params.id]);
    if (user) {
      res.json(user);
    } else {
      res.status(404).json({ error: 'User not found' });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Endpoint to create a new user
app.post('/users', async (req, res) => {
  try {
    const { name, email } = req.body;
    const result = await db.run('INSERT INTO users (name, email) VALUES (?, ?)', [name, email]);
    res.status(201).json({ id: result.lastID });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Endpoint to update a user
app.put('/users/:id', async (req, res) => {
  try {
    const { name, email } = req.body;
    const result = await db.run('UPDATE users SET name = ?, email = ? WHERE id = ?', [name, email, req.params.id]);
    if (result.changes === 0) {
      res.status(404).json({ error: 'User not found' });
    } else {
      res.json({ message: 'User updated' });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Endpoint to delete a user
app.delete('/users/:id', async (req, res) => {
  try {
    const result = await db.run('DELETE FROM users WHERE id = ?', [req.params.id]);
    if (result.changes === 0) {
      res.status(404).json({ error: 'User not found' });
    } else {
      res.json({ message: 'User deleted' });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
