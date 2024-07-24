import sqlite3 as sql
class Context:
    def __init__(self) -> None:
        self.__connection = sql.connect("./db/ov_reg_rendom.db",check_same_thread=False,timeout=60)
        self.__cursor = self.__connection.cursor()
    
    def get_regs(self,limit=1,offset=None):
        regs = self.__cursor.execute(f'SELECT reg FROM Regs WHERE checked = 0 LIMIT {limit} OFFSET {offset}')
data_contest = Context()