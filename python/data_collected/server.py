from flask import Flask, jsonify, request
import sqlite3
import json
app = Flask(__name__)


@app.route("/insertreg/<int:reg>")
def insert_reg(reg):
    conn = sqlite3.connect("./db/regs.db")
    curs = conn.cursor()
    curs.execute('INSERT OR IGNORE INTO Regs(reg,collected) VALUES (?,0)',(reg,))
    conn.commit()
    conn.close()
    return str(reg), 200


@app.route('/test/api/student/login', methods=['GET', 'POST'])
def test_server():
    reg = int(request.form.get("username"))
    if not reg:
        return jsonify({"msg": "Provide valid username"}), 400
    # if reg % 2 == 1:
    #     return jsonify([]), 404
    conn = sqlite3.connect("./db/regs.db")
    curs = conn.cursor()
    data = curs.execute(
        f"SELECT data FROM Regs WHERE reg = {reg}").fetchone()[0]
    if isinstance(data, str):
        data = json.loads(data)

    if data.__len__() > 0:
        return jsonify(data), 200
    else:
        return jsonify(data), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=8200)
