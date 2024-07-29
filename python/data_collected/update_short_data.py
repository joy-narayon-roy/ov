import sqlite3 as sql
import json

def db_conn():
    conn = sql.connect("./db/regs.db")
    curs = conn.cursor()
    curs.execute('''CREATE TABLE IF NOT EXISTS Valid_students ("reg"	INT NOT NULL,
	"name"	TEXT DEFAULT NULL,
	"subject"	TEXT DEFAULT NULL,
	"college"	TEXT DEFAULT NULL,
	"admission_reg"	INT DEFAULT NULL,
	"father"	TEXT DEFAULT NULL,
	"mother"	TEXT DEFAULT NULL,
	"img_url"	TEXT DEFAULT NULL,
	"session"	TEXT DEFAULT NULL,
	"img"	BLOB DEFAULT NULL,
	"gender"	TEXT DEFAULT NULL,
	PRIMARY KEY("reg"));''')
    conn.commit()
    return conn

def map_def(data):
    data = json.loads(data[0])
    student = data["student"]
    reg = int(student["reg_no"])
    name = student["name"]
    session = student["ac_session"]
    subject= student["subject"]["subject_name"]
    college = student["college"]["college_name"]
    father = student["father_name"]
    mother = student["mother_name"]
    addmition_reg = int(student["admission_roll"])
    img_url = student["photo_url"]
    gender = student["gender"]
    
    return (reg,name,gender,subject,college,addmition_reg,img_url,session,father,mother)

def get_data_from_sql(conn,limit = 100000):
    curs = conn.cursor()
    all_datas= []
    page  = 0
    while True:
        datas = curs.execute(f"SELECT data FROM Regs WHERE data NOT NULL LIMIT {limit} OFFSET {limit * page}").fetchall()
        if datas.__len__() == 0:break
        print("Page",page)
        all_datas+=datas
        page+=1
    new_datas = list(map(map_def,all_datas))
    return new_datas

def main():
    insert_sql = "INSERT OR IGNORE INTO Valid_students (reg,name,gender,subject,college,admission_reg,img_url,session,father,mother) VALUES (?,?,?,?,?,?,?,?,?,?);"
    conn = db_conn()
    datas = get_data_from_sql(conn)
    curs = conn.cursor()
    curs.executemany(insert_sql,datas)
    conn.commit()
    print(datas.__len__(),"Data inserted")
    
if __name__ == "__main__":
    main()