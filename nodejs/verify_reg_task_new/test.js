const sqlite3 = require("sqlite3");
const { open } = require("sqlite");

async function openDb() {
  return open({
    filename: "example.db",
    driver: sqlite3.Database,
  });
}

async function main() {

  const db = await openDb();

  // Create a table
  await db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      email TEXT
    );
  `);

  // Insert data
  await db.run(
    `
    INSERT INTO users (name, email) 
    VALUES (?, ?);
  `,
    ["John Doe", "john.doe@example.com"]
  );

  // Query data
  const rows = await db.all("SELECT * FROM users");
  console.log(rows);

  // Update data
  await db.run(
    `
    UPDATE users 
    SET email = ? 
    WHERE name = ?;
  `,
    ["john.updated@example.com", "John Doe"]
  );

  // Delete data
  await db.run(
    `
    DELETE FROM users 
    WHERE name = ?;
  `,
    ["John Doe"]
  );

  // Close the database
  await db.close();
}

main().catch((err) => {
  console.error("Error:", err);
});
