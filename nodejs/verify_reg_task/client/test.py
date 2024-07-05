import requests as req

def verify(reg):
    res = req.post("http://regicard.nu.edu.bd/verification.php",
                   {"reg": reg})
    res.raise_for_status()
    file = open(f'./html/{reg}.html', 'w')
    file.write(res.text)
    file.close()
    return f'{res.content}'.find("<table>") > 0
print(verify("22237352131"))