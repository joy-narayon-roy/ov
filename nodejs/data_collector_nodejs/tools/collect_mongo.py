import pymongo
import sqlite3

def collect_from_mongo():
    client = pymongo.MongoClient("mongodb+srv://yeti:demoyeti420@main.i6nm9j1.mongodb.net/")
    db = client.get_database("nu_verifiy")
    coll = db.get_collection("valides")
    regs = list(coll.find())
    def map_def(val):
        return int(val['_id'])
    all_reg = list(map(map_def,regs))
    return all_reg
    # for reg in regs:
    #     print(int(reg['_id']))
def write_sqlite(val):
    crete_table = '''CREATE TABLE IF NOT EXISTS "Regs" (
	"reg"	INTEGER NOT NULL UNIQUE,
	"data"	JSON DEFAULT NULL,
	"collected"	BOOLEAN NOT NULL,
	PRIMARY KEY("reg")
    )'''
    conn = sqlite3.connect("./db/regs.db")
    curr = conn.cursor()
    curr.execute(crete_table)
    conn.commit()
    sql = "INSERT INTO Regs (reg, data, collected) VALUES (?, ?, ?)"
    for reg in val:
        curr.execute(sql,reg)
        print(reg) 
    # print(val)
    conn.commit()
    conn.close()


def main():
    regs = collect_from_mongo()
    def map_def(d):
        return (d,None,False)
    vals = list(map(map_def,regs))
    write_sqlite(vals)
    

if __name__ == "__main__":
    main()