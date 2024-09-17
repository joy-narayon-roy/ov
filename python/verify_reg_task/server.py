from flask import Flask

app = Flask(__name__)

regs = []


@app.get("/valid/<id>")
def uniq_check(id=None):
    if not id in regs:
        regs.append(id)
        return id, 200
    else:
        return "Not valid", 400


if __name__ == "__main__":
    app.run('0.0.0.0', 80, True, False)
