import requests as req


def verify(reg):
    res = req.post("http://regicard.nu.edu.bd/verification.php",
                   {"reg": reg})
    res.raise_for_status()
    return f'{res.content}'.find("<table>") > 0


def get_config(id):
    res = req.get(f'http://localhost:8080/config/{id}')
    res.raise_for_status()
    return Config(res.json())


class Config:
    __REMOTE = "http://localhost:8080"
    __id = None

    def __init__(self, config) -> None:
        self.__id = config["id"]
        self.start = config["start"]
        self.curr = config["curr"]
        self.end = config["end"]

    def next(self):
        res = req.get(f'{self.__REMOTE}/config/{self.__id}/next')
        res.raise_for_status()
        self.curr = res.json()["curr"]
        return self.curr

    def this_valid_reg(self, reg):
        res = req.post(f'{self.__REMOTE}/reg/{reg}')
        res.raise_for_status()
