import requests as req
import json
res = req.post("http://localhost:8100/t/v/22225612772/2",
               json={"data": "I am tje"})
