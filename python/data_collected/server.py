from flask import Flask, jsonify, request
import sqlite3
import json
app = Flask(__name__)

db_conn = sqlite3.connect("./db/regs.db",60,check_same_thread=False)
db_cursor = db_conn.cursor() 

@app.route("/insertreg/<int:reg>")
def insert_reg(reg):
    conn = sqlite3.connect("./db/regs.db")
    curs = conn.cursor()
    curs.execute(
        'INSERT OR IGNORE INTO Regs(reg,collected) VALUES (?,0)', (reg,))
    conn.commit()
    conn.close()
    return str(reg), 200


@app.route("/api/all")
def get_all_data():
    limit = request.args.get('limit', default=10, type=int) or 10
    page = request.args.get('page', default=0, type=int) or 0
    offset = page * limit
    
    data = db_cursor.execute(
        f"SELECT * FROM Regs WHERE data NOT NULL ORDER BY reg ASC LIMIT {limit} OFFSET {offset}").fetchall()
    data = list(map(lambda d:(d[0],json.loads(d[1])),data))
    
    return jsonify(data)

@app.route("/api/valid/student")
def get_valid_student():
    limit = request.args.get('limit', default=100, type=int)
    page = request.args.get('page', default=0, type=int) or 0
    subject = request.args.get('subject', default=None, type=str)
    college = request.args.get('college', default=None, type=str)
    
    
    
    offset = page * limit
    print(query)
    datas = db_cursor.execute(f"SELECT * FROM Valid_students {query} LIMIT {limit} OFFSET {offset}").fetchall()
    return jsonify(datas)


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
    app.run(debug=True, host="0.0.0.0", port=8200)
