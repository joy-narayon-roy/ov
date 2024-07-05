from flask import Flask, request,  jsonify
import sqlite3
import json

app = Flask(__name__)
TASK_LIMIT = 5
DB_PATH = "./db/test.db"


class Tasks:
    def __init__(self, task_limit, db_path) -> None:
        self.__count = 0
        self.all = []
        self.db_path = db_path
        self.__task_limit = task_limit
        self.__conn = sqlite3.connect(self.db_path)
        self.__db = self.__conn.cursor()
        self.all = self.__db.execute(
            f"SELECT reg,collected FROM Regs WHERE collected=0 LIMIT {self.__task_limit}").fetchall()
        self.__conn.close()
        # print(self.all)

    def next(self):
        last = self.__count

        if self.__count >= self.__task_limit:
            return None

        self.__count += 1
        return f'{self.all[last][0]},{last}'

    def this_is_valid(self, reg: int, index: int, mdata):
        data = self.all[index]
        self.all[index] = (data[0], 1)
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute(
            '''UPDATE Regs SET collected = ?, data = ? WHERE reg = ?''', (True, json.dumps(mdata), reg))
        conn.commit()
        conn.close()

        return "OK"

    def json(self):
        def c_json(data):
            return {
                "reg": data[0],
                "collected": bool(data[1]),
            }
        return list(map(c_json, self.all))


tasks = Tasks(task_limit=TASK_LIMIT, db_path=DB_PATH)


@app.route("/c", methods=['GET'])
def get_count_curr():
    return jsonify(tasks.json()), 200


@app.route("/c/n", methods=['GET'])
def get_count_next():
    data = tasks.next()
    if not data:
        return str(None), 400
    return str(data), 200


@app.route("/v/<int:reg>/<int:ind>", methods=["POST"])
def post_verify(reg, ind):
    data = request.form["data"]
    tasks.this_is_valid(reg, ind, data)
    return "OK",200


@app.route("/ok", methods=["GET"])
def server_ok():
    return jsonify({"msg": "OK", "state": True}), 200


if __name__ == '__main__':
    app.run(debug=False)
