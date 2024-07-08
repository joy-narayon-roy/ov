from flask import Flask, jsonify, request
import sqlite3
import json
app = Flask(__name__)


@app.route('/api/student/login', methods=['GET', 'POST'])
def home():
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
    app.run(debug=True, port=8080)
