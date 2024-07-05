from tinydb import TinyDB
from pymongo import MongoClient

# mongodb = MongoClient(
#     "mongodb+srv://yeti:demoyeti420@main.i6nm9j1.mongodb.net/nu_verifiy")
db = TinyDB("./db/ov.regs.json")
# mongo_regs = list(mongodb["nu_verifiy"]["valides"].find())

# regs = []
# for reg in mongo_regs:
#     reg_str = int(reg["_id"])
#     # print(reg_str)
#     regs.append({"reg": reg_str, "data": None, "collected": False})
    # regs.append({int(reg["_id"]): {reg: int(reg["_id"])}})

students = db.table("students")
# students.insert_multiple(regs)
# print(regs)
print(students.all())
