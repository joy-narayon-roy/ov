import requests as req

SERVER_ADDRESS = "http://103.113.200.45:8006/api/student/login"
def get_reg_data(reg: int):
    form_data = {
        "username": str(reg),
        "password": "123456",
        "recaptcha-v3": "undefined"
    }
    res = req.post(SERVER_ADDRESS, data=form_data,timeout=3600)
    res.raise_for_status()
    return json.dumps(res.json())

print(get_reg_data(2222566100))
